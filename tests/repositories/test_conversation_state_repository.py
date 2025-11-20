import pytest
from sqlalchemy.orm import Session

from chatbot_gsantana.repositories.conversation_state import ConversationStateRepository
from chatbot_gsantana.models.conversation_state import ConversationState


@pytest.fixture
def state_repository() -> ConversationStateRepository:
    """Retorna uma instância do repositório de estado da conversa."""
    return ConversationStateRepository()


def test_get_by_session_id_not_found(
    db_session: Session, state_repository: ConversationStateRepository
):
    """
    Testa se get_by_session_id retorna None quando o estado não existe.
    """
    state = state_repository.get_by_session_id(db_session, "non_existent_session")
    assert state is None


def test_save_or_update_creates_new_state(
    db_session: Session, state_repository: ConversationStateRepository
):
    """
    Testa se save_or_update cria um novo registro de estado corretamente.
    """
    session_id = "new_session_1"
    state_name = "WAITING_NAME"
    data = {"initial_prompt": True}

    # Ação: Salva o estado pela primeira vez
    state_repository.save_or_update(db_session, session_id, state_name, data)

    # Verificação: Busca o estado no banco e valida os campos
    saved_state = (
        db_session.query(ConversationState)
        .filter(ConversationState.session_id == session_id)
        .first()
    )

    assert saved_state is not None
    assert saved_state.session_id == session_id
    assert saved_state.state == state_name
    assert saved_state.data == data


def test_save_or_update_updates_existing_state(
    db_session: Session, state_repository: ConversationStateRepository
):
    """
    Testa se save_or_update atualiza um registro de estado existente corretamente.
    """
    session_id = "existing_session_1"

    # Configuração: Cria um estado inicial no banco
    initial_state = ConversationState(
        session_id=session_id, state="WAITING_NAME", data={"nome": "Carlos"}
    )
    db_session.add(initial_state)
    db_session.commit()

    # Ação: Atualiza o estado
    new_state_name = "WAITING_KNOWLEDGE"
    new_data = {"nome": "Carlos", "conhecimentos": "Python"}
    state_repository.save_or_update(db_session, session_id, new_state_name, new_data)

    # Verificação: Busca o estado atualizado e valida os campos
    updated_state = (
        db_session.query(ConversationState)
        .filter(ConversationState.session_id == session_id)
        .first()
    )

    assert updated_state is not None
    assert updated_state.state == new_state_name
    assert updated_state.data == new_data
    assert (
        updated_state.data["nome"] == "Carlos"
    )  # Garante que os dados antigos foram mantidos/atualizados
