from auth.auth import auth_backend
from auth.schemas import UserCreate, UserRead
from auth.service import get_user_manager
from db.models import User
from fastapi import Depends, FastAPI, HTTPException
from fastapi_users import FastAPIUsers
from schemas import Expense, ExpenseGet, ExpenseUpdate
from service import add_expense, get_expenses, update_expense

app = FastAPI()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_active_user = fastapi_users.current_user(active=True)


@app.get("/expenses/")
async def expense_get_items(user: User = Depends(current_active_user)) -> list[ExpenseGet] | None:
    expenses = await get_expenses(user_id=user.id)
    if len(expenses) == 0:
        print(user.id)
        return None
    return expenses


@app.post("/expenses/")
async def expense_insert(expense: Expense, user: User = Depends(current_active_user)) -> str:
    expense = expense.model_dump()
    message_action = await add_expense(**expense, user_id=user.id)
    return message_action


@app.patch(
    "/expenses/{expense_id}", response_model=ExpenseUpdate, response_model_exclude_none=True
)
async def expense_edit(
    expense_id: int, expense: ExpenseUpdate, user: User = Depends(current_active_user)
):
    edit_expense = await update_expense(
        user_id=user.id, expense_id=expense_id, expense_data=expense
    )
    if not edit_expense:
        raise HTTPException(status_code=404, detail="expense not found")

    return edit_expense
