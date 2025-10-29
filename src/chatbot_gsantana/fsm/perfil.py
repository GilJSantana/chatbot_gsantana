from enum import Enum, auto
from typing import Dict

from fastapi import Depends
from sqlalchemy.orm import Session

from ..services.voluntario import VoluntarioService, get_voluntario_service
from ..services.faq import FaqService, get_faq_service  # Importa o serviço de FAQ


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
    Máquina de Estados Finitos para gerenciar
    o fluxo de onboarding e delegar para o FAQ.
    """

    def __init__(self, voluntario_service: VoluntarioService, faq_service: FaqService):
        """
        O construtor recebe as instâncias dos serviços
        necessários (Injeção de Dependência).
        """
        self.voluntario_service = voluntario_service
        self.faq_service = faq_service

    def handle_message(self, session_id: str, message: str, db: Session) -> str:
        """Processa a mensagem do usuário com base no estado atual da conversa."""
        if session_id not in _user_states:
            # Verifica se o perfil já existe no banco para evitar o onboarding repetido
            perfil_existente = self.voluntario_service.repository.get_by_session_id(
                db, session_id
            )
            if perfil_existente:
                _user_states[session_id] = {"state": State.READY_TO_CHAT, "data": {}}
            else:
                _user_states[session_id] = {"state": State.START, "data": {}}

        current_state = _user_states[session_id]["state"]

        if current_state == State.READY_TO_CHAT:
            # Onboarding concluído, delega para o serviço de FAQ
            answer = self.faq_service.get_answer_for_question(
                db=db, question_text=message
            )
            return (
                answer
                or "Não encontrei uma resposta "
                "para sua pergunta. Tente de outra forma."
            )

        # Lógica do onboarding (estados anteriores)
        if current_state == State.START:
            _user_states[session_id]["state"] = State.WAITING_NAME
            return (
                "Olá! Sou o assistente de cadastro "
                "de voluntários. Para começarmos, qual é o seu nome?"
            )

        elif current_state == State.WAITING_NAME:
            _user_states[session_id]["data"]["nome"] = message
            _user_states[session_id]["state"] = State.WAITING_KNOWLEDGE
            return (
                f"Prazer, {message}! Quais são "
                f"seus conhecimentos? (Ex: Python, SQL, Design)"
            )

        elif current_state == State.WAITING_KNOWLEDGE:
            _user_states[session_id]["data"]["conhecimentos"] = parse_knowledge_to_dict(
                message
            )
            _user_states[session_id]["state"] = State.WAITING_LOCATION
            return "Entendido. Onde você mora? (Cidade/Estado)"

        elif current_state == State.WAITING_LOCATION:
            _user_states[session_id]["data"]["local"] = message
            _user_states[session_id]["state"] = State.WAITING_HOBBIES
            return "Legal! E para descontrair, quais são seus hobbies?"

        elif current_state == State.WAITING_HOBBIES:
            _user_states[session_id]["data"]["hobbies"] = message
            _user_states[session_id]["state"] = State.PERSISTING_DATA

            user_data = _user_states[session_id]["data"]
            self.voluntario_service.persistir_perfil_voluntario(
                db=db,
                session_id=session_id,
                nome=user_data["nome"],
                local=user_data["local"],
                hobbies=user_data["hobbies"],
                conhecimentos=user_data["conhecimentos"],
            )

            _user_states[session_id]["state"] = State.READY_TO_CHAT
            return (
                "Tudo certo! Seu perfil foi salvo. "
                "Agora você pode fazer suas perguntas."
            )

        return "Desculpe, não entendi o estado atual da conversa."


def get_fsm(
    vol_service: VoluntarioService = Depends(get_voluntario_service),
    faq_service_instance: FaqService = Depends(get_faq_service),
) -> PerfilChatFSM:
    """
    Dependência do FastAPI que cria
    e fornece uma instância de PerfilChatFSM
    com todas as suas dependências.
    """
    return PerfilChatFSM(
        voluntario_service=vol_service, faq_service=faq_service_instance
    )
