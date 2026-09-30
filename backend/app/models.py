import enum
import uuid

from sqlalchemy import (
    Column, String, Date, DateTime, Numeric, Text, ForeignKey, Enum, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


class CustomerStatus(str, enum.Enum):
    lead = "lead"
    confirmed = "confirmed"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class EventType(str, enum.Enum):
    engagement = "engagement"
    haldi = "haldi"
    sangeet = "sangeet"
    wedding = "wedding"
    reception = "reception"
    other = "other"


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(120), nullable=True)
    partner_name = Column(String(120), nullable=True)
    event_type = Column(Enum(EventType), nullable=False, default=EventType.wedding)
    event_date = Column(Date, nullable=True)
    venue = Column(String(200), nullable=True)
    guest_count = Column(String(20), nullable=True)
    budget = Column(Numeric(12, 2), nullable=True)
    status = Column(Enum(CustomerStatus), nullable=False, default=CustomerStatus.lead)
    source = Column(String(80), nullable=True)  # referral, instagram, walk-in, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    payments = relationship("Payment", back_populates="customer", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="customer", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    method = Column(String(40), nullable=True)  # cash, upi, card, bank_transfer
    paid_on = Column(Date, nullable=False, server_default=func.current_date())
    remarks = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="payments")


class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="notes")
