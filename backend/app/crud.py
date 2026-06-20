from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from . import models, schemas
from typing import List

def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    # ensure SKU unique
    existing = db.query(models.Product).filter(models.Product.sku == product_in.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    product = models.Product(name=product_in.name, sku=product_in.sku, price=product_in.price, quantity=product_in.quantity)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_products(db: Session) -> List[models.Product]:
    return db.query(models.Product).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_product(db: Session, product_id: int, update: schemas.ProductUpdate):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if update.name is not None:
        product.name = update.name
    if update.price is not None:
        if update.price < 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative")
        product.price = update.price
    if update.quantity is not None:
        if update.quantity < 0:
            raise HTTPException(status_code=400, detail="Quantity cannot be negative")
        product.quantity = update.quantity
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Check for existing order items referencing this product
    ref = db.query(models.OrderItem).filter(models.OrderItem.product_id == product_id).first()
    if ref:
        raise HTTPException(status_code=400, detail="Cannot delete product: it is referenced by existing orders")
    db.delete(product)
    db.commit()
    return True

def create_customer(db: Session, customer_in: schemas.CustomerCreate):
    existing = db.query(models.Customer).filter(models.Customer.email == customer_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    customer = models.Customer(full_name=customer_in.full_name, email=customer_in.email, phone=customer_in.phone)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def get_customers(db: Session):
    return db.query(models.Customer).all()

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def delete_customer(db: Session, customer_id: int):
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return True

def create_order(db: Session, order_in: schemas.OrderCreate):
    # verify customer
    customer = get_customer(db, order_in.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # start a transaction
    total = 0.0
    order = models.Order(customer_id=order_in.customer_id, total_amount=0.0)
    db.add(order)
    db.flush()  # get order.id

    for item in order_in.items:
        product = get_product(db, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.sku}")
        unit_price = product.price
        total += unit_price * item.quantity
        # decrement stock
        product.quantity -= item.quantity
        db.add(product)
        order_item = models.OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, unit_price=unit_price)
        db.add(order_item)

    order.total_amount = total
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_orders(db: Session):
    return db.query(models.Order).all()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def delete_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # when deleting/cancelling an order, restore stock
    for item in order.items:
        product = get_product(db, item.product_id)
        if product:
            product.quantity += item.quantity
            db.add(product)
    db.delete(order)
    db.commit()
    return True
