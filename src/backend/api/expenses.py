from db.models import User
from dependencies import current_active_user
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Expense, ExpenseGet, ExpenseUpdate
from service import add_expense, delete_expense, get_expenses, update_expense

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/")
async def expense_get_items(user: User = Depends(current_active_user)) -> list[ExpenseGet] | None:
    expenses = await get_expenses(user_id=user.id)
    if len(expenses) == 0:
        print(user.id)
        return None
    return expenses


@router.post("/")
async def expense_insert(expense: Expense, user: User = Depends(current_active_user)) -> str:
    expense_data = expense.model_dump()
    is_added = await add_expense(**expense_data, user_id=user.id)

    if is_added:
        return "Record added successfully"
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to add record")


@router.patch("/{expense_id}", response_model=ExpenseUpdate, response_model_exclude_none=True)
async def expense_edit(
    expense_id: int, expense: ExpenseUpdate, user: User = Depends(current_active_user)
):
    edit_expense = await update_expense(
        user_id=user.id, expense_id=expense_id, expense_data=expense
    )
    if not edit_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return edit_expense


@router.delete("/{expense_id}")
async def expense_delete(expense_id: int, user: User = Depends(current_active_user)):
    del_expense = await delete_expense(user_id=user.id, expense_id=expense_id)
    if not del_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {"detail": "Expense deleted successfully"}
