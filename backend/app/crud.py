import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session

from . import models, schemas


def get_customer(db: Session, customer_id: uuid.UUID):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def list_customers(db: Session, search: str | None = None, status: str | None = None,
                    skip: int = 0, limit: int = 50):
    q = db.query(models.Customer)
    if search:
        like = f"%{search}%"
        q = q.filter(or_(models.Customer.name.ilike(like),
                          models.Customer.phone.ilike(like),
                          models.Customer.email.ilike(like)))
    if status:
        q = q.filter(models.Customer.status == status)
    return q.order_by(models.Customer.created_at.desc()).offset(skip).limit(limit).all()


def create_customer(db: Session, payload: schemas.CustomerCreate):
    customer = models.Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer: models.Customer, payload: schemas.CustomerUpdate):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer: models.Customer):
    db.delete(customer)
    db.commit()


def add_payment(db: Session, customer_id: uuid.UUID, payload: schemas.PaymentCreate):
    payment = models.Payment(customer_id=customer_id, **payload.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def add_note(db: Session, customer_id: uuid.UUID, payload: schemas.NoteCreate):
    note = models.Note(customer_id=customer_id, **payload.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
