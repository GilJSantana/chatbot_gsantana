from fastapi import APIRouter, Depends

from .... import schemas
from ....fsm.perfil import PerfilChatFSM

router = APIRouter()

@router.post("/", response_model=schemas.ChatResponse)
def handle_chat_message(
    chat_in: schemas.ChatMessage,
    fsm: PerfilChatFSM = Depends(),
):
    response_text = fsm.handle_message(
        session_id=chat_in.session_id, message=chat_in.message
    )

    return schemas.ChatResponse(reply=response_text)
