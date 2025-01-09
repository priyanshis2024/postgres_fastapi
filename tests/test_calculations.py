from app.calculations import add,sub
def test_add():
    # assert True => No changes code will run
    # assert False => Throws the error
    print("Testing add function")
    assert add(5,3) == 8

def test_sub():
    assert sub(10,5) == 5