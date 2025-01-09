from tests.database import client

def test_root(client):
    res = client.get("/")
    # print(res)
    # print(res.json()) # it shows actual payload
    assert res.json() == ['Welcome to the API!!']
    assert res.status_code == 200

# def test_user_create(client):
#     res = client.post("/users/",json={"Id":46,"Email":"callmephone@gmail.com","Password":"password123"})
#     print(res.json())
#     assert res.status_code == 201

def test_user_by_id(client):
    user_id = 38
    res = client.get(f"/users/{user_id}")
    print(res.json())
    assert res.status_code == 200 

def test_all_user(client):
    res = client.get("/users/")
    print(res.json())
    assert res.status_code == 200

def test_login_user(client):
    res = client.post("/login",data={"username":"callmephone@gmail.com","password":"password123"})
    print(res.json())
    assert res.status_code == 200