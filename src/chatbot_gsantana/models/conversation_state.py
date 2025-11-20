from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.sql import func

from ..core.database import Base


class ConversationState(Base):
    __tablename__ = "conversation_states"

    session_id = Column(String, primary_key=True, index=True)
    state = Column(String, nullable=False)
    data = Column(JSON, nullable=False, default={})
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), default=func.now()
    )
