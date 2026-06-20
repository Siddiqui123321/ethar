from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.CustomerRead, status_code=201)
def create_customer(customer_in: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer_in)


@router.get("/", response_model=list[schemas.CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)


@router.get("/{customer_id}", response_model=schemas.CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    crud.delete_customer(db, customer_id)
    return None
