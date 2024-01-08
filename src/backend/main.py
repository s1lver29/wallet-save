from api.expenses import router as expenses_router
from auth.auth import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://172.23.29.54:3000",
    "https://172.23.29.54:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Указать доверенные домены (* для всех)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["auth"],
)

app.include_router(expenses_router, prefix="")

