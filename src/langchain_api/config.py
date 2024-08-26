from langchain_huggingface import HuggingFaceEndpoint

token = 'ZTk3ZjdmYjMtNmMwOC00NGE1LTk0MzktYzA3ZjU4Yzc2YWI3OmY2OGFlMTQ1LTIyNzgtNDIxMC05M2JmLWFhNTFkZjdmYTY1Yw=='

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"

hugginface_token = "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"
chat_model  = HuggingFaceEndpoint(repo_id=repo_id,huggingfacehub_api_token=hugginface_token)
