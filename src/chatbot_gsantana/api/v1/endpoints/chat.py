from fastapi import APIRouter, Depends

from .... import schemas
from ....api import deps
from ....fsm.perfil import PerfilChatFSM, get_fsm

router = APIRouter()


@router.post("/", response_model=schemas.ChatResponse)
def handle_chat_message(
    chat_in: schemas.ChatMessage,
    db: deps.SessionDep,
    fsm: PerfilChatFSM = Depends(get_fsm),
):
    """
    Ponto de entrada principal para as mensagens do chat.
    """
    response_text = fsm.handle_message(
        session_id=chat_in.session_id, message=chat_in.message, db=db
    )

    return schemas.ChatResponse(reply=response_text)
