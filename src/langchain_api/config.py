from langchain_huggingface import HuggingFaceEndpoint
from src.config import settings

token = settings.HUGGIFACE_TOKEN

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"

hugginface_token = "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"
chat_model = HuggingFaceEndpoint(repo_id=repo_id, huggingfacehub_api_token=hugginface_token)
