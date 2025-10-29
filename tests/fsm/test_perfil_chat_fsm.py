import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from chatbot_gsantana.fsm.perfil import (
    PerfilChatFSM,
    State,
    _user_states,
)
from chatbot_gsantana.services.voluntario import VoluntarioService
from chatbot_gsantana.services.faq import FaqService
from chatbot_gsantana.repositories.voluntario import (
    VoluntarioRepository,
)  # Importa o repositório


class TestPerfilChatFSM(unittest.TestCase):

    def setUp(self):
        _user_states.clear()
        self.mock_db_session = MagicMock(spec=Session)
        self.mock_voluntario_service = MagicMock(spec=VoluntarioService)
        self.mock_faq_service = MagicMock(spec=FaqService)

        # Atribui um mock para o atributo 'repository' dentro do mock do serviço
        self.mock_voluntario_service.repository = MagicMock(spec=VoluntarioRepository)

        self.fsm = PerfilChatFSM(
            voluntario_service=self.mock_voluntario_service,
            faq_service=self.mock_faq_service,
        )

    def test_fsm_full_onboarding_flow_and_delegation(self):
        session_id = "test_session_fsm_1"

        # Simula que o perfil não existe no início
        self.mock_voluntario_service.repository.get_by_session_id.return_value = None

        # ... (passos do onboarding) ...
        self.fsm.handle_message(session_id, "Olá", self.mock_db_session)
        self.fsm.handle_message(session_id, "Carlos", self.mock_db_session)
        self.fsm.handle_message(session_id, "Python, SQL", self.mock_db_session)
        self.fsm.handle_message(session_id, "São Paulo/SP", self.mock_db_session)

        # Último passo do onboarding
        response = self.fsm.handle_message(session_id, "Leitura", self.mock_db_session)
        self.assertEqual(_user_states[session_id]["state"], State.READY_TO_CHAT)
        self.assertIn("perfil foi salvo", response)

        # Verifica se o serviço de persistência foi chamado
        self.mock_voluntario_service.persistir_perfil_voluntario.assert_called_once()

        # Delegação para o FAQ Service
        question = "Qual o horário de funcionamento?"
        expected_answer = "O horário é das 9h às 18h."
        self.mock_faq_service.get_answer_for_question.return_value = expected_answer

        response = self.fsm.handle_message(session_id, question, self.mock_db_session)

        self.mock_faq_service.get_answer_for_question.assert_called_once_with(
            db=self.mock_db_session, question_text=question
        )
        self.assertEqual(response, expected_answer)

    def test_fsm_skips_onboarding_if_profile_exists(self):
        session_id = "existing_user_session"

        # Simula que um perfil já existe para esta sessão
        self.mock_voluntario_service.repository.get_by_session_id.return_value = (
            MagicMock()
        )

        question = "Qual o endereço?"
        expected_answer = "Nosso endereço é Rua Exemplo, 123."
        self.mock_faq_service.get_answer_for_question.return_value = expected_answer

        response = self.fsm.handle_message(session_id, question, self.mock_db_session)

        self.assertEqual(_user_states[session_id]["state"], State.READY_TO_CHAT)
        self.mock_faq_service.get_answer_for_question.assert_called_once_with(
            db=self.mock_db_session, question_text=question
        )
        self.assertEqual(response, expected_answer)
