from sqlalchemy.orm import Session
from typing import Dict, Any

from ..models.conversation_state import ConversationState


class ConversationStateRepository:
    """
    Encapsula a lógica de acesso a dados para o estado da conversa.
    """

    def get_by_session_id(
        self, db: Session, session_id: str
    ) -> ConversationState | None:
        """Busca o estado de uma conversa pelo session_id."""
        return (
            db.query(ConversationState)
            .filter(ConversationState.session_id == session_id)
            .first()
        )

    def save_or_update(
        self, db: Session, session_id: str, state: str, data: Dict[str, Any]
    ) -> ConversationState:
        """
        Salva um novo estado de conversa ou atualiza um existente.
        """
        # Tenta buscar o estado existente
        db_state = self.get_by_session_id(db, session_id)

        if not db_state:
            # Se não existir, cria um novo
            db_state = ConversationState(session_id=session_id)
            db.add(db_state)

        # Atualiza os campos
        db_state.state = state
        db_state.data = data

        db.commit()
        db.refresh(db_state)
        return db_state
