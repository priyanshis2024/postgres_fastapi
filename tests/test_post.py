import pytest

def test_post_by_id(client):
    post_id = 1
    res = client.get(f"/posts/{post_id}")
    print(res.json())
    assert res.status_code == 200 

def test_all_user(client):
    res = client.get("/posts/")
    print(res.json())
    assert res.status_code == 200

@pytest.mark.parametrize(
    "Id, Name, Domain, Age, Email, Is_student, Rating",  
    [
        (23, "Jigna", "IT", 23, "jign23@gmail.com", True, 5),
        (24, "Nancy", "BCA", 20, "nancy12@gmail.com", True, 4),
        (25, "Veer", "BCA", 22, "veeral@gmail.com", True, 3)
    ]
)
def test_multiple_post(client, Id, Name, Domain, Age, Email, Is_student, Rating):
    res = client.post("/posts/", json={
        "Id": Id,
        "Name": Name,
        "Domain": Domain,
        "Age": Age,
        "Email": Email,
        "Is_student": Is_student,
        "Rating": Rating
    })
    print(res.json())
    assert res.status_code == 201


def test_user_create(client):
    res = client.post("/posts/",json={"Id":26,"Name":"Mixi","Domain": "MCA","Age": 20,"Email": "mixi12390@hotmail.com","Is_student": True,"Rating": 3})
    print(res.json())
    assert res.status_code == 201

def test_update_post(client):
    post_id = 18
    res = client.put(f"/posts/{post_id}",json={"Id":18,"Name":"Mixi","Domain": "BCA","Age": 18,"Email": "mixi12390@hotmail.com","Is_student": True,"Rating": 3})
    print(res.json())
    assert res.status_code == 200

def test_delete_post(client):
    post_id = 8
    res = client.delete(f"/posts/{post_id}")
    print("Post successfully deleted")
    assert res.status_code == 200

def test_delete_non_exist_post(client):
    post_id = 10000000
    res = client.delete(f"/posts/{post_id}")
    print("Post successfully deleted")
    assert res.status_code == 404
