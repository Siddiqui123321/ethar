def test_products_api(client):
    # create product
    resp = client.post('/products/', json={"name":"APIProd","sku":"API-1","price":5.5,"quantity":10})
    assert resp.status_code == 201
    pid = resp.json()['id']

    # list
    resp = client.get('/products/')
    assert resp.status_code == 200
    assert any(p['id'] == pid for p in resp.json())

    # get
    resp = client.get(f'/products/{pid}')
    assert resp.status_code == 200

    # update
    resp = client.put(f'/products/{pid}', json={"price":6.0})
    assert resp.status_code == 200
    assert resp.json()['price'] == 6.0

    # delete
    resp = client.delete(f'/products/{pid}')
    assert resp.status_code == 204


def test_full_order_flow(client):
    # create product and customer
    pr = client.post('/products/', json={"name":"OProd","sku":"O-1","price":3.0,"quantity":4}).json()
    cu = client.post('/customers/', json={"full_name":"Zed","email":"zed@example.com","phone":"1"}).json()

    # create order
    order_payload = {"customer_id": cu['id'], "items": [{"product_id": pr['id'], "quantity": 2}]}
    resp = client.post('/orders/', json=order_payload)
    assert resp.status_code == 201
    order = resp.json()
    assert order['total_amount'] == 6.0

    # check product stock decreased
    p = client.get(f"/products/{pr['id']}").json()
    assert p['quantity'] == 2

    # delete order
    resp = client.delete(f"/orders/{order['id']}")
    assert resp.status_code == 204

    p2 = client.get(f"/products/{pr['id']}").json()
    assert p2['quantity'] == 4
