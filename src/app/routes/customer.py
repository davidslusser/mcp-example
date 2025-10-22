from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    responses={404: {"description": "Customer not found"}},
)


@router.post("/", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED, operation_id="create_customer")
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.get("/", response_model=List[schemas.Customer], operation_id="read_customers")
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).offset(skip).limit(limit).all()
    return customers


@router.get("/{customer_id}", response_model=schemas.Customer, operation_id="read_customer")
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@router.put("/{customer_id}", response_model=schemas.Customer, operation_id="update_customer")
def update_customer(customer_id: int, customer: schemas.Customer, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    if customer.email != db_customer.email:
        existing_customer = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
        if existing_customer:
            raise HTTPException(status_code=400, detail="Email already registered")

    for key, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(db_customer)
    db.commit()
    return None
