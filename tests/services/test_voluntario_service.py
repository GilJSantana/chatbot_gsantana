import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from chatbot_gsantana.models.voluntario import Voluntario
from chatbot_gsantana.repositories.voluntario import VoluntarioRepository
from chatbot_gsantana.services.voluntario import VoluntarioService


class TestVoluntarioService(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=VoluntarioRepository)
        self.mock_db_session = MagicMock(spec=Session)
        # Injeta o repositório mockado no serviço
        self.service = VoluntarioService(repository=self.mock_repository)

    def test_persistir_perfil_voluntario_cria_novo(self):
        """
        Testa se um novo perfil é criado quando não há um existente para a session_id.
        """
        # Configuração
        self.mock_repository.get_by_session_id.return_value = None
        session_id = "test-session-123"
        dados_perfil = {
            "nome": "João Silva",
            "local": "São Paulo/SP",
            "hobbies": "Leitura, cinema",
            "conhecimentos": {"python": "avançado"},
        }

        # Ação
        self.service.persistir_perfil_voluntario(
            db=self.mock_db_session, session_id=session_id, **dados_perfil
        )

        # Verificações
        self.mock_repository.get_by_session_id.assert_called_once_with(
            self.mock_db_session, session_id=session_id
        )

        # Verifica se save_or_update foi chamado com um objeto Voluntario
        self.mock_repository.save_or_update.assert_called_once()

        # Acessa os argumentos nomeados (kwargs) da chamada do mock
        saved_voluntario: Voluntario = (
            self.mock_repository.save_or_update.call_args.kwargs["voluntario"]
        )

        self.assertIsInstance(saved_voluntario, Voluntario)
        self.assertEqual(saved_voluntario.session_id, session_id)
        self.assertEqual(saved_voluntario.nome, dados_perfil["nome"])
