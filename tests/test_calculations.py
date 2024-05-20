import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 3),
    (4, 5, 9),
    (6, 7, 13)
    ])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, -1),
    (4, 5, -1),
    (6, 7, -1)
    ])
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 2),
    (4, 5, 20),
    (6, 7, 42)
    ])
def test_multiply(num1, num2, expected):
    assert multiply(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 0.5),
    (4, 5, 0.8),
    (6, 7, round((6/7), 6))
    ])
def test_divide(num1, num2, expected):
    assert divide(num1, num2) == expected





@pytest.fixture
def zero_bank_account():
    print("creating empty bank account...")
    return BankAccount()

@pytest.fixture
def charged_50_bank_account():
    print("creating charged bank account with 50 dollars")
    return BankAccount(50)

def test_bank_account_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_account_withdraw(charged_50_bank_account):
    charged_50_bank_account.withdraw(50)
    assert charged_50_bank_account.balance == 0

def test_bank_account_deposit(zero_bank_account):
    zero_bank_account.deposit(50)
    assert zero_bank_account.balance == 50

def test_bank_account_collect_interest(charged_50_bank_account):
    charged_50_bank_account.collect_interest()
    assert charged_50_bank_account.balance == 55 

def test_bank_account_insufficient_funds(charged_50_bank_account):
    with pytest.raises(InsufficientFunds):
        charged_50_bank_account.withdraw(200)

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40), 
    (1200, 200, 1000)
    ])

def test_bank_account_transaction_manual(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected