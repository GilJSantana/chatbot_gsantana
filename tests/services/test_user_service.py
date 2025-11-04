import unittest
from unittest.mock import MagicMock, patch, ANY

from sqlalchemy.orm import Session

from chatbot_gsantana.models.user import User
from chatbot_gsantana.schemas.user import UserCreate
from chatbot_gsantana.services.user import UserService
from chatbot_gsantana.repositories.user import UserRepository


REALISTIC_HASH = "$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgt8g5o5dJ/A"


class TestUserService(unittest.TestCase):

    def setUp(self):
        self.mock_user_repository = MagicMock(spec=UserRepository)
        self.mock_db_session = MagicMock(spec=Session)
        self.user_service = UserService(
            repository=self.mock_user_repository, db=self.mock_db_session
        )

    @patch("chatbot_gsantana.services.user.verify_password", return_value=True)
    def test_authenticate_user_success(self, mock_verify_password):
        mock_user = User(id=1, username="testuser", hashed_password=REALISTIC_HASH)
        self.mock_user_repository.get_user_by_username.return_value = mock_user

        authenticated_user = self.user_service.authenticate_user(
            username="testuser", password="testpassword"
        )

        # CORREÇÃO: A chamada real é com db posicional e username keyword-only
        self.mock_user_repository.get_user_by_username.assert_called_once_with(
            self.mock_db_session, username="testuser"
        )
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.username, "testuser")

    @patch(
        "chatbot_gsantana.services.user.get_password_hash", return_value=REALISTIC_HASH
    )
    def test_create_user(self, mock_get_password_hash):
        user_in = UserCreate(
            username="newuser", email="newuser@example.com", password="newpassword"
        )

        self.mock_user_repository.get_user_by_username.return_value = None
        self.mock_user_repository.get_user_by_email.return_value = None

        self.user_service.create_user(user_data=user_in.dict())

        # CORREÇÃO: A chamada real é com db posicional e user posicional
        self.mock_user_repository.save.assert_called_once_with(
            self.mock_db_session, ANY
        )

        saved_user_arg = self.mock_user_repository.save.call_args.args[1]
        self.assertIsInstance(saved_user_arg, User)
        self.assertEqual(saved_user_arg.username, "newuser")
        self.assertEqual(saved_user_arg.hashed_password, REALISTIC_HASH)
