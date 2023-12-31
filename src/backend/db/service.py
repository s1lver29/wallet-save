from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .connections import async_session
from .models import Expenses, User


@asynccontextmanager
async def async_database_session():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


class Expense:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_expense(self, name: str, amount: float, user_id: str, category_id: str):
        new_expense = Expenses(name=name, amount=amount, user_id=user_id, category_id=category_id)
        self.session.add(new_expense)
        return True

    async def get_expenses(
        self, user_id: int, category_ids: list[int] | None = None, skip: int = 0, limit: int = 100
    ):
        filters = [Expenses.user_id == user_id]
        if category_ids is not None and len(category_ids) != 0:
            filters.append(Expenses.category_id.in_(category_ids))
        query = select(Expenses).where(and_(*filters)).limit(limit).offset(skip)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_expense(self, user_id: int, expense_id: int):
        filters = [Expenses.user_id == user_id, Expenses.id == expense_id]
        query = select(Expenses).where(*filters)
        expense = await self.session.execute(query)
        return expense.scalars().first()

    async def delete_expense(self, user_id: int, expense_id: int):
        expense_to_delete = await self.get_expense(user_id=user_id, expense_id=expense_id)
        if expense_to_delete:
            await self.session.delete(expense_to_delete)
            return True
        return False


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
