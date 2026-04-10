async def test_add_portfolio_item(client):
    # 1. Регистрация
    response = await client.post("/auth/register", json={
        "full_name": "Test User",
        "email": "test@test.com",
        "password": "password"
    })
    assert response.status_code == 200

    # 2. Логин — получаем токен
    response = await client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "password"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Добавляем акцию
    response = await client.post("/portfolio/add", json={
        "ticker": "005930",
        "quantity": 10,
        "purchase_price": 70000
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["ticker"] == "005930"



async def test_get_portfolio(client):
    # 1. Регистрация
    response = await client.post("/auth/register", json={
        "full_name": "Test User",
        "email": "test@test.com",
        "password": "password"
    })
    assert response.status_code == 200

    # 2. Логин — получаем токен
    response = await client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "password"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Добавляем акцию
    _ = await client.post("/portfolio/add", json={
        "ticker": "005930",
        "quantity": 10,
        "purchase_price": 70000
    }, headers=headers)

    # 4. Get portfolio items
    response = await client.get("/portfolio/", headers=headers)
    assert response.status_code == 200
    assert response.json()[0]["ticker"] == "005930"


async def test_delete_portfolio_item(client):
    # 1. Регистрация
    response = await client.post("/auth/register", json={
        "full_name": "Test User",
        "email": "test@test.com",
        "password": "password"
    })
    assert response.status_code == 200

    # 2. Логин — получаем токен
    response = await client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "password"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Добавляем акцию
    item = await client.post("/portfolio/add", json={
        "ticker": "005930",
        "quantity": 10,
        "purchase_price": 70000
    }, headers=headers)

    # 4. Delete item
    item_id = item.json()["id"]
    response = await client.delete(f"/portfolio/{item_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "deleted"
