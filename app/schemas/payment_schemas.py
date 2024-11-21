from pydantic import BaseModel
from decimal import Decimal
from app.enums import PaymentStatus


class PaymentSchema(BaseModel):
    user_id: str
    payment_id: str
    amount: Decimal
    email: str | None
    type: str | None
    company_id: int

    class Config:
        from_attributes = True


class PaymentResultSchema(BaseModel):
    status: PaymentStatus
    payment_id: str
