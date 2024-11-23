from langchain_huggingface import HuggingFaceEndpoint
from src.config import settings

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"

hugginface_token = settings.HUGGIFACE_TOKEN
chat_model = HuggingFaceEndpoint(repo_id=repo_id, huggingfacehub_api_token=hugginface_token)
