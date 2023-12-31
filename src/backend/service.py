from db.service import Expense, async_database_session
from schemas import ExpenseGet, ExpenseUpdate


async def get_expenses(user_id: int):
    async with async_database_session() as session:
        expense_manager = Expense(session)
        all_expenses = await expense_manager.get_expenses(user_id=user_id)
        return [ExpenseGet.from_orm(expense) for expense in all_expenses]


async def add_expense(user_id: int, name: str, amount: float, category_id: str):
    async with async_database_session() as session:
        expense_manager = Expense(session)
        is_added = await expense_manager.add_expense(name, amount, user_id, category_id)
        return is_added


async def update_expense(user_id: int, expense_id: int, expense_data: ExpenseUpdate):
    async with async_database_session() as session:
        expense_manager = Expense(session)
        expense = await expense_manager.get_expense(user_id=user_id, expense_id=expense_id)
        if not expense:
            return None
        if expense_data.name:
            expense.name = expense_data.name
        if expense_data.amount:
            expense.amount = expense_data.amount
        if expense_data.category_id:
            expense.category_id = expense_data.category_id

        return expense_data
