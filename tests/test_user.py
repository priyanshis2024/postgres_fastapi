from jose import jwt
import pytest
from app import schemas
from app.configure import settings
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
# def test_login_user(test_user,client):
    res = client.post("/login",data={"username":"callmephone@gmail.com","password":"password123"})
    # res = client.post("/login",data={"username":test_user["Email"],"password":test_user["Password"]})
    # login_res = schemas.Token(**res.json())
    # payload = jwt.decode(login_res,settings.secret_key,algorithms=[settings.algorithm])
    # id: str = payload.get("user_id")
    # assert id == test_user['id'] 
    # print(res.json())
    # assert login_res.token_type == 'bearer'
    assert res.status_code == 200

def test_incorrect_login(client):
    res = client.post("/login",data={"username":"callmephone@gmail.com","password":"wrongPassword"})
    assert res.status_code == 403