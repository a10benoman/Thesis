def test_create_product_and_movement(client):
    # create product
    r = client.post('/products/', json={'sku': 'SKU-1', 'name': 'Test Product'})
    assert r.status_code == 200
    p = r.json()
    assert p['sku'] == 'SKU-1'

    # create an OUT movement
    r2 = client.post('/movements/', params={'product_id': p['id'], 'type': 'OUT', 'quantity': 3})
    assert r2.status_code == 200
    assert r2.json().get('status') == 'ok'
