from fastapi import APIRouter
from src.langchain_api.LLMModelApi import ChatModel
from src.langchain_api.config import chat_model

router  = APIRouter(
    prefix="/chatmodel",
    tags=["ChaModel"]
)

@router.post("")
async def get_answer_from_chatmodel(question: str) -> dict:
    model  = ChatModel(chat_model)
    answer  = model.get_answer_on_question(question)
    print(answer)
    return answer