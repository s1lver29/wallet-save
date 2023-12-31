from typing import Optional

from pydantic import BaseModel, Field, constr


class Expense(BaseModel):
    name: str = constr(min_length=2)
    amount: float = Field(gt=0, description="Число не отрицательное")
    category_id: int

class ExpenseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    amount: Optional[float] = Field(None, gt=0, description="Число не отрицательное")
    category_id: Optional[int] = None

class ExpenseGet(Expense):
    id: int

    class Config:
        from_attributes = True
