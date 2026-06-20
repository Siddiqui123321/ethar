from app import crud, schemas


def test_create_product_and_customer(db_session):
    p_in = schemas.ProductCreate(name="Test Prod", sku="TP-1", price=10.0, quantity=5)
    p = crud.create_product(db_session, p_in)
    assert p.id is not None
    assert p.sku == "TP-1"

    c_in = schemas.CustomerCreate(full_name="Alice", email="alice@example.com", phone="123")
    c = crud.create_customer(db_session, c_in)
    assert c.id is not None
    assert c.email == "alice@example.com"


def test_order_creates_and_reduces_stock(db_session):
    # create product and customer
    p_in = schemas.ProductCreate(name="Widget", sku="W-01", price=2.5, quantity=10)
    p = crud.create_product(db_session, p_in)
    c_in = schemas.CustomerCreate(full_name="Bob", email="bob@example.com", phone="000")
    c = crud.create_customer(db_session, c_in)

    order_in = schemas.OrderCreate(customer_id=c.id, items=[schemas.OrderItemCreate(product_id=p.id, quantity=3)])
    order = crud.create_order(db_session, order_in)
    assert order.total_amount == 3 * p.price

    # product quantity reduced
    refreshed = crud.get_product(db_session, p.id)
    assert refreshed.quantity == 7


def test_order_fails_if_insufficient_stock(db_session):
    p_in = schemas.ProductCreate(name="Small", sku="S-1", price=1.0, quantity=1)
    p = crud.create_product(db_session, p_in)
    c_in = schemas.CustomerCreate(full_name="Carol", email="carol@example.com", phone=None)
    c = crud.create_customer(db_session, c_in)

    order_in = schemas.OrderCreate(customer_id=c.id, items=[schemas.OrderItemCreate(product_id=p.id, quantity=5)])
    try:
        crud.create_order(db_session, order_in)
        assert False, "Expected HTTPException due to insufficient stock"
    except Exception as e:
        # crud raises HTTPException; ensure product quantity unchanged
        refreshed = crud.get_product(db_session, p.id)
        assert refreshed.quantity == 1


def test_delete_order_restores_stock(db_session):
    p_in = schemas.ProductCreate(name="Restore", sku="R-1", price=4.0, quantity=5)
    p = crud.create_product(db_session, p_in)
    c_in = schemas.CustomerCreate(full_name="Dan", email="dan@example.com", phone=None)
    c = crud.create_customer(db_session, c_in)

    order_in = schemas.OrderCreate(customer_id=c.id, items=[schemas.OrderItemCreate(product_id=p.id, quantity=2)])
    order = crud.create_order(db_session, order_in)
    assert crud.get_product(db_session, p.id).quantity == 3

    crud.delete_order(db_session, order.id)
    assert crud.get_product(db_session, p.id).quantity == 5
