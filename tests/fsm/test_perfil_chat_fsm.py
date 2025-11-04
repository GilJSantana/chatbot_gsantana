from unittest.mock import MagicMock
import pytest
from sqlalchemy.orm import Session

from chatbot_gsantana.fsm.perfil import PerfilChatFSM, State, _user_states
from chatbot_gsantana.services.voluntario import VoluntarioService
from chatbot_gsantana.services.faq import FaqService
from chatbot_gsantana.repositories.voluntario import VoluntarioRepository
from chatbot_gsantana.repositories.faq import FaqRepository


@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_voluntario_repo():
    return MagicMock(spec=VoluntarioRepository)


@pytest.fixture
def mock_voluntario_service(mock_voluntario_repo, mock_db_session):
    # Mocka a instância do serviço, não a classe
    service = MagicMock(spec=VoluntarioService)
    service.repository = mock_voluntario_repo
    service.db = mock_db_session  # Garante que o serviço tenha acesso ao mock de db
    return service


@pytest.fixture
def mock_faq_repo():
    return MagicMock(spec=FaqRepository)


@pytest.fixture
def mock_faq_service(mock_faq_repo, mock_db_session):
    # Mocka a instância do serviço, não a classe
    service = MagicMock(spec=FaqService)
    service.repository = mock_faq_repo
    service.db = mock_db_session  # Garante que o serviço tenha acesso ao mock de db
    return service


@pytest.fixture
def fsm(mock_voluntario_service, mock_faq_service, mock_db_session):
    _user_states.clear()  # Limpa estados entre testes
    # Passa os mocks para o construtor da FSM
    return PerfilChatFSM(
        voluntario_service=mock_voluntario_service,
        faq_service=mock_faq_service,
        db=mock_db_session,
    )


def test_fsm_full_onboarding_flow_and_delegation(
    fsm: PerfilChatFSM,
    mock_db_session: Session,
    mock_voluntario_service: MagicMock,
    mock_faq_service: MagicMock,
):
    session_id = "test_session_fsm_1"
    # Mocka o retorno do repositório dentro do serviço mockado
    mock_voluntario_service.repository.get_by_session_id.return_value = None

    fsm.handle_message(session_id, "Olá")
    assert _user_states[session_id]["state"] == State.WAITING_NAME

    fsm.handle_message(session_id, "Carlos")
    assert _user_states[session_id]["state"] == State.WAITING_KNOWLEDGE

    fsm.handle_message(session_id, "Python, SQL")
    assert _user_states[session_id]["state"] == State.WAITING_LOCATION

    fsm.handle_message(session_id, "São Paulo/SP")
    assert _user_states[session_id]["state"] == State.WAITING_HOBBIES

    response = fsm.handle_message(session_id, "Leitura")
    assert _user_states[session_id]["state"] == State.READY_TO_CHAT
    assert "perfil foi salvo" in response
    # Agora o assert é feito no método do serviço mockado
    mock_voluntario_service.persistir_perfil_voluntario.assert_called_once_with(
        session_id=session_id,
        nome="Carlos",
        local="São Paulo/SP",
        hobbies="Leitura",
        conhecimentos={"python": "avançado", "sql": "intermediário"},
    )

    question = "Qual o horário de funcionamento?"
    expected_answer = "O horário é das 9h às 18h."
    # Define o retorno do método do serviço mockado
    mock_faq_service.get_answer_for_question.return_value = expected_answer

    response = fsm.handle_message(session_id, question)
    mock_faq_service.get_answer_for_question.assert_called_once_with(
        question_text=question
    )
    assert response == expected_answer


def test_fsm_skips_onboarding_if_profile_exists(
    fsm: PerfilChatFSM,
    mock_db_session: Session,
    mock_voluntario_service: MagicMock,
    mock_faq_service: MagicMock,
):
    session_id = "existing_user_session"
    mock_voluntario_service.repository.get_by_session_id.return_value = MagicMock()

    question = "Qual o endereço?"
    expected_answer = "Nosso endereço é Rua Exemplo, 123."
    # Define o retorno do método do serviço mockado
    mock_faq_service.get_answer_for_question.return_value = expected_answer

    response = fsm.handle_message(session_id, question)

    assert _user_states[session_id]["state"] == State.READY_TO_CHAT
    mock_faq_service.get_answer_for_question.assert_called_once_with(
        question_text=question
    )
    assert response == expected_answer
