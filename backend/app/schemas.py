import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .models import CustomerStatus, EventType


# ---------- Note ----------
class NoteBase(BaseModel):
    content: str


class NoteCreate(NoteBase):
    pass


class NoteOut(NoteBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


# ---------- Payment ----------
class PaymentBase(BaseModel):
    amount: Decimal
    method: Optional[str] = None
    paid_on: Optional[date] = None
    remarks: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentOut(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


# ---------- Customer ----------
class CustomerBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    partner_name: Optional[str] = None
    event_type: EventType = EventType.wedding
    event_date: Optional[date] = None
    venue: Optional[str] = None
    guest_count: Optional[str] = None
    budget: Optional[Decimal] = None
    status: CustomerStatus = CustomerStatus.lead
    source: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    partner_name: Optional[str] = None
    event_type: Optional[EventType] = None
    event_date: Optional[date] = None
    venue: Optional[str] = None
    guest_count: Optional[str] = None
    budget: Optional[Decimal] = None
    status: Optional[CustomerStatus] = None
    source: Optional[str] = None


class CustomerOut(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CustomerDetail(CustomerOut):
    payments: list[PaymentOut] = []
    notes: list[NoteOut] = []
