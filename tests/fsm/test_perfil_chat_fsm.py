from unittest.mock import MagicMock, ANY
import pytest
from sqlalchemy.orm import Session

from chatbot_gsantana.fsm.perfil import PerfilChatFSM, State
from chatbot_gsantana.services.voluntario import VoluntarioService
from chatbot_gsantana.services.faq import FaqService
from chatbot_gsantana.repositories.voluntario import VoluntarioRepository
from chatbot_gsantana.repositories.faq import FaqRepository
from chatbot_gsantana.repositories.conversation_state import ConversationStateRepository
from chatbot_gsantana.models.conversation_state import ConversationState as ConversationStateModel

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_voluntario_repo():
    return MagicMock(spec=VoluntarioRepository)

@pytest.fixture
def mock_faq_repo():
    return MagicMock(spec=FaqRepository)

@pytest.fixture
def mock_state_repo():
    return MagicMock(spec=ConversationStateRepository)

@pytest.fixture
def mock_voluntario_service(mock_voluntario_repo, mock_db_session):
    service = MagicMock(spec=VoluntarioService)
    service.repository = mock_voluntario_repo
    service.db = mock_db_session
    return service

@pytest.fixture
def mock_faq_service(mock_faq_repo, mock_db_session):
    service = MagicMock(spec=FaqService)
    service.repository = mock_faq_repo
    service.db = mock_db_session
    return service

@pytest.fixture
def fsm(mock_voluntario_service, mock_faq_service, mock_state_repo, mock_db_session):
    return PerfilChatFSM(
        voluntario_service=mock_voluntario_service,
        faq_service=mock_faq_service,
        state_repo=mock_state_repo,
        db=mock_db_session
    )

def test_fsm_full_onboarding_flow_and_delegation(fsm, mock_state_repo, mock_voluntario_service, mock_faq_service):
    session_id = "test_session_fsm_1"
    
    # 1. Primeira mensagem: Inicia o onboarding
    mock_voluntario_service.repository.get_by_session_id.return_value = None
    mock_state_repo.get_by_session_id.return_value = None
    fsm.handle_message(session_id, "Olá")
    mock_state_repo.save_or_update.assert_called_with(ANY, session_id, State.WAITING_NAME.name, ANY)

    # 2. Segunda mensagem: Envia o nome
    mock_state_repo.get_by_session_id.return_value = ConversationStateModel(session_id=session_id, state=State.WAITING_NAME.name, data={})
    fsm.handle_message(session_id, "Carlos")
    mock_state_repo.save_or_update.assert_called_with(ANY, session_id, State.WAITING_KNOWLEDGE.name, {"nome": "Carlos"})

    # ... e assim por diante para os outros passos ...
    mock_state_repo.get_by_session_id.return_value = ConversationStateModel(session_id=session_id, state=State.WAITING_KNOWLEDGE.name, data={"nome": "Carlos"})
    fsm.handle_message(session_id, "Python, SQL")
    
    mock_state_repo.get_by_session_id.return_value = ConversationStateModel(session_id=session_id, state=State.WAITING_LOCATION.name, data={"nome": "Carlos", "conhecimentos": {"python": "avançado", "sql": "intermediário"}})
    fsm.handle_message(session_id, "São Paulo/SP")

    # Último passo do onboarding
    mock_state_repo.get_by_session_id.return_value = ConversationStateModel(session_id=session_id, state=State.WAITING_HOBBIES.name, data={"nome": "Carlos", "conhecimentos": {"python": "avançado", "sql": "intermediário"}, "local": "São Paulo/SP"})
    response = fsm.handle_message(session_id, "Leitura")
    
    assert "perfil foi salvo" in response
    mock_voluntario_service.persistir_perfil_voluntario.assert_called_once()
    mock_state_repo.save_or_update.assert_called_with(ANY, session_id, State.READY_TO_CHAT.name, ANY)

    # Delegação para o FAQ
    mock_state_repo.get_by_session_id.return_value = ConversationStateModel(session_id=session_id, state=State.READY_TO_CHAT.name, data={})
    question = "Qual o horário de funcionamento?"
    expected_answer = "O horário é das 9h às 18h."
    mock_faq_service.get_answer_for_question.return_value = expected_answer
    
    response = fsm.handle_message(session_id, question)
    
    mock_faq_service.get_answer_for_question.assert_called_once_with(question_text=question)
    assert response == expected_answer

def test_fsm_skips_onboarding_if_profile_exists(fsm, mock_state_repo, mock_voluntario_service, mock_faq_service):
    session_id = "existing_user_session"
    
    # Simula que o perfil já existe e o estado da conversa ainda não foi criado
    mock_voluntario_service.repository.get_by_session_id.return_value = MagicMock()
    mock_state_repo.get_by_session_id.return_value = None

    question = "Qual o endereço?"
    expected_answer = "Nosso endereço é Rua Exemplo, 123."
    mock_faq_service.get_answer_for_question.return_value = expected_answer

    response = fsm.handle_message(session_id, question)

    # Verifica se o estado foi diretamente para READY_TO_CHAT
    mock_state_repo.save_or_update.assert_called_with(ANY, session_id, State.READY_TO_CHAT.name, {})
    
    mock_faq_service.get_answer_for_question.assert_called_once_with(question_text=question)
    assert response == expected_answer
