from enum import Enum, auto
from typing import Dict

import structlog
from fastapi import Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services.voluntario import VoluntarioService
from ..services.faq import FaqService
from ..models.voluntario import Voluntario

# Inicializa o logger para este módulo
logger = structlog.get_logger(__name__)


class State(Enum):
    START = auto()
    WAITING_NAME = auto()
    WAITING_KNOWLEDGE = auto()
    WAITING_LOCATION = auto()
    WAITING_HOBBIES = auto()
    PERSISTING_DATA = auto()
    READY_TO_CHAT = auto()


_user_states: Dict[str, Dict] = {}


def parse_knowledge_to_dict(text: str) -> Dict[str, str]:
    """
    Função de parsing simplificada para extrair conhecimentos de um texto.
    """
    skills = [skill.strip().lower() for skill in text.split(",")]
    knowledge_dict = {}
    if skills and skills[0]:
        knowledge_dict[skills[0]] = "avançado"
        for skill in skills[1:]:
            knowledge_dict[skill] = "intermediário"
    return knowledge_dict


class PerfilChatFSM:
    """
    Máquina de Estados Finitos para gerenciar o fluxo de onboarding e delegar para o FAQ.
    """

    def __init__(
        self,
        voluntario_service: VoluntarioService = Depends(),
        faq_service: FaqService = Depends(),
        db: Session = Depends(get_db)
    ):
        self.voluntario_service = voluntario_service
        self.faq_service = faq_service
        self.db = db

    def handle_message(self, session_id: str, message: str) -> str:
        """Processa a mensagem do usuário com base no estado atual da conversa."""
        log = logger.bind(session_id=session_id)

        if session_id not in _user_states:
            log.info("fsm.session.new", message="Nova sessão detectada, verificando perfil existente.")
            perfil_existente = self.voluntario_service.repository.get_by_session_id(self.db, session_id)
            if perfil_existente:
                _user_states[session_id] = {"state": State.READY_TO_CHAT, "data": {}}
                log.info("fsm.onboarding.skip", message="Perfil existente encontrado, pulando para o modo de chat.")
            else:
                _user_states[session_id] = {"state": State.START, "data": {}}
                log.info("fsm.onboarding.start", message="Nenhum perfil encontrado, iniciando onboarding.")

        current_state = _user_states[session_id]["state"]
        log = log.bind(current_state=current_state.name)
        log.info("fsm.message.received", user_message=message)

        if current_state == State.READY_TO_CHAT:
            log.info("fsm.delegation.faq", message="Delegando para o serviço de FAQ.")
            answer = self.faq_service.get_answer_for_question(question_text=message)
            return answer or "Não encontrei uma resposta para sua pergunta. Tente de outra forma."

        response = self._handle_onboarding_message(session_id, message, current_state, log)
        return response

    def _handle_onboarding_message(self, session_id: str, message: str, current_state: State, log: structlog.BoundLogger) -> str:
        """Lógica de tratamento de mensagens durante o onboarding."""
        
        next_state = None
        response = "Desculpe, não entendi o estado atual da conversa."

        if current_state == State.START:
            next_state = State.WAITING_NAME
            response = "Olá! Sou o assistente de cadastro de voluntários. Para começarmos, qual é o seu nome?"

        elif current_state == State.WAITING_NAME:
            _user_states[session_id]["data"]["nome"] = message
            next_state = State.WAITING_KNOWLEDGE
            response = f"Prazer, {message}! Quais são seus conhecimentos? (Ex: Python, SQL, Design)"

        elif current_state == State.WAITING_KNOWLEDGE:
            _user_states[session_id]["data"]["conhecimentos"] = parse_knowledge_to_dict(message)
            next_state = State.WAITING_LOCATION
            response = "Entendido. Onde você mora? (Cidade/Estado)"

        elif current_state == State.WAITING_LOCATION:
            _user_states[session_id]["data"]["local"] = message
            next_state = State.WAITING_HOBBIES
            response = "Legal! E para descontrair, quais são seus hobbies?"

        elif current_state == State.WAITING_HOBBIES:
            _user_states[session_id]["data"]["hobbies"] = message
            next_state = State.PERSISTING_DATA
            log.info("fsm.onboarding.persisting", message="Coleta de dados concluída. Persistindo perfil.")
            
            user_data = _user_states[session_id]["data"]
            self.voluntario_service.persistir_perfil_voluntario(
                session_id=session_id,
                nome=user_data["nome"],
                local=user_data["local"],
                hobbies=user_data["hobbies"],
                conhecimentos=user_data["conhecimentos"]
            )
            
            next_state = State.READY_TO_CHAT
            response = "Tudo certo! Seu perfil foi salvo. Agora você pode fazer suas perguntas."

        if next_state:
            log.info("fsm.state.transition", from_state=current_state.name, to_state=next_state.name)
            _user_states[session_id]["state"] = next_state

        return response
