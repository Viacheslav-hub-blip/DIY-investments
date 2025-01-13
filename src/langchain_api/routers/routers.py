from fastapi import APIRouter
from src.langchain_api.llm_api.llms.answer_llm.chat_model import ChatModel

router = APIRouter(
    prefix="/chatmodel",
    tags=["ChaModel"]
)

chat_model = ChatModel()


@router.post("")
async def get_answer_from_chatmodel(question: str) -> dict:
    return chat_model.get_answer_on_question(question)
