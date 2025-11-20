from enum import Enum, auto
from typing import Dict, Any

import structlog
from fastapi import Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services.voluntario import VoluntarioService
from ..services.faq import FaqService
from ..repositories.conversation_state import ConversationStateRepository

logger = structlog.get_logger(__name__)

class State(Enum):
    START = auto()
    WAITING_NAME = auto()
    WAITING_KNOWLEDGE = auto()
    WAITING_LOCATION = auto()
    WAITING_HOBBIES = auto()
    READY_TO_CHAT = auto()

def parse_knowledge_to_dict(text: str) -> Dict[str, str]:
    skills = [skill.strip().lower() for skill in text.split(",")]
    knowledge_dict = {}
    if skills and skills[0]:
        knowledge_dict[skills[0]] = "avançado"
        for skill in skills[1:]:
            knowledge_dict[skill] = "intermediário"
    return knowledge_dict

class PerfilChatFSM:
    def __init__(
        self,
        voluntario_service: VoluntarioService = Depends(),
        faq_service: FaqService = Depends(),
        state_repo: ConversationStateRepository = Depends(),
        db: Session = Depends(get_db),
    ):
        self.voluntario_service = voluntario_service
        self.faq_service = faq_service
        self.state_repo = state_repo
        self.db = db

    def _get_or_create_state(self, session_id: str) -> (State, Dict[str, Any]):
        log = logger.bind(session_id=session_id)
        conversation_state = self.state_repo.get_by_session_id(self.db, session_id)

        if conversation_state:
            return State[conversation_state.state], conversation_state.data

        log.info("fsm.session.new", message="Nova sessão detectada, verificando perfil existente.")
        perfil_existente = self.voluntario_service.repository.get_by_session_id(self.db, session_id)
        
        if perfil_existente:
            log.info("fsm.onboarding.skip", message="Perfil existente encontrado, pulando para o modo de chat.")
            new_state = State.READY_TO_CHAT
            new_data = {}
        else:
            log.info("fsm.onboarding.start", message="Nenhum perfil encontrado, iniciando onboarding.")
            new_state = State.START
            new_data = {}
        
        self.state_repo.save_or_update(self.db, session_id, new_state.name, new_data)
        return new_state, new_data

    def handle_message(self, session_id: str, message: str) -> str:
        current_state, data = self._get_or_create_state(session_id)
        log = logger.bind(session_id=session_id, current_state=current_state.name)
        log.info("fsm.message.received", user_message=message)

        if current_state == State.READY_TO_CHAT:
            log.info("fsm.delegation.faq", message="Delegando para o serviço de FAQ.")
            return self.faq_service.get_answer_for_question(question_text=message)

        return self._handle_onboarding_message(session_id, message, current_state, data, log)

    def _handle_onboarding_message(self, session_id: str, message: str, current_state: State, data: Dict[str, Any], log: structlog.BoundLogger) -> str:
        next_state = None
        response = "Desculpe, não entendi o estado atual da conversa."

        if current_state == State.START:
            next_state = State.WAITING_NAME
            response = "Olá! Sou o assistente de cadastro de voluntários. Para começarmos, qual é o seu nome?"
        elif current_state == State.WAITING_NAME:
            data["nome"] = message
            next_state = State.WAITING_KNOWLEDGE
            response = f"Prazer, {message}! Quais são seus conhecimentos? (Ex: Python, SQL, Design)"
        elif current_state == State.WAITING_KNOWLEDGE:
            data["conhecimentos"] = parse_knowledge_to_dict(message)
            next_state = State.WAITING_LOCATION
            response = "Entendido. Onde você mora? (Cidade/Estado)"
        elif current_state == State.WAITING_LOCATION:
            data["local"] = message
            next_state = State.WAITING_HOBBIES
            response = "Legal! E para descontrair, quais são seus hobbies?"
        elif current_state == State.WAITING_HOBBIES:
            data["hobbies"] = message
            log.info("fsm.onboarding.persisting", message="Coleta de dados concluída. Persistindo perfil.")
            
            self.voluntario_service.persistir_perfil_voluntario(
                session_id=session_id,
                nome=data["nome"],
                local=data["local"],
                hobbies=data["hobbies"],
                conhecimentos=data["conhecimentos"],
            )
            
            next_state = State.READY_TO_CHAT
            response = "Tudo certo! Seu perfil foi salvo. Agora você pode fazer suas perguntas."

        if next_state:
            log.info("fsm.state.transition", from_state=current_state.name, to_state=next_state.name)
            self.state_repo.save_or_update(self.db, session_id, next_state.name, data)

        return response
