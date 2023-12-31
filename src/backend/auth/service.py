from typing import Optional

from db.models import User
from db.service import get_user_db
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.password import PasswordHelper

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

async def get_user_manager(session: AsyncSession = Depends(get_user_db)):
    yield UserManager(session)
