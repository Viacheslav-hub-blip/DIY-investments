from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.finance_api.routers import router as finance_router
from src.users_api.routers import router as user_router

from src.langchain_api.routers import router as router_langchain

app = FastAPI()

app.include_router(user_router)
app.include_router(router_langchain)
app.include_router(finance_router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uvicorn src.main:app --use-colors --log-level debug --reload
