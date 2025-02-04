from fastapi import FastAPI
from src.finance_api.Routers.routers import router as finance_api_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(finance_api_router)

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
