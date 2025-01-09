from app.calculations import add,sub,BankAccount,InsufficientFunds
import pytest
def test_add():
    # assert True => No changes code will run
    # assert False => Throws the error
    print("Testing add function")
    assert add(5,3) == 8

def test_sub():
    assert sub(10,5) == 5

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(100000)

def test_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0

def test_bank_set_initial_amount(bank_account):
    # bank_account = BankAccount(100000)
    assert bank_account.balance == 100000

def test_withdraw(bank_account):
    # bank_account = BankAccount(100000)
    bank_account.withdraw(20000)
    assert bank_account.balance == 80000

def test_deposit(bank_account):
    # bank_account = BankAccount(100000)
    bank_account.deposit(25000)
    assert bank_account.balance == 125000

def test_collect_interest(bank_account):
    # bank_account = BankAccount(100000)
    bank_account.collect_interest()
    assert int(bank_account.balance) == 110000

# parametrizing
@pytest.mark.parametrize("Deposited, Withdraw, Expected",[
    (50000,10000,40000),
    (100000,1000,99000),
    (79000,50000,29000)
])

def test_bank_transaction(zero_bank_account,Deposited,Withdraw,Expected):
    # zero_bank_account.deposit(20000)
    # zero_bank_account.withdraw(10000)
    zero_bank_account.deposit(Deposited)
    zero_bank_account.withdraw(Withdraw)
    # assert zero_bank_account.balance == 10000
    assert zero_bank_account.balance == Expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200000)