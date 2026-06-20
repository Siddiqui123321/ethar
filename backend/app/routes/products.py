from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.ProductRead, status_code=201)
def create_product(product_in: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product_in)


@router.get("/", response_model=list[schemas.ProductRead])
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=schemas.ProductRead)
def update_product(product_id: int, update: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.update_product(db, product_id, update)


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    crud.delete_product(db, product_id)
    return None
