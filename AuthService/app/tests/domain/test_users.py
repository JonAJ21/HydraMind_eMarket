import pytest

from domain.entities.user import User
from domain.exceptions.role import RoleIsIncorrectException
from domain.values.role import Role
from domain.values.email import Email
from domain.values.password import Password
from domain.exceptions.login import LoginTooLongException
from domain.values.login import Login

def test_create_login_success():
    login = Login('login')
    assert login.value == 'login'
    
def test_create_login_too_long():
    with pytest.raises(LoginTooLongException):
        login = Login('l' * 300)
        
def test_create_password_success():
    password = Password.hashed_password('password')
    assert password == b'password'
    
    
def test_create_some_passwords_success():
    password_1 = Password.hashed_password('password')
    password_2 = Password.hashed_password('pswrd')
    assert password_1 == str.encode('password')
    assert password_2 == b'pswrd'
    
def test_check_password_incorrect():
    password = Password.hashed_password('psdkad')
    assert not (password == b'b')
    
def test_create_email_success():
    email = Email('email@email.com')
    assert email.value == 'email@email.com'
    
def test_create_role_success():
    customer = Role('CUSTOMER')
    salesman = Role('SALESMAN')
    admin = Role('ADMIN')
    assert customer.value == 'CUSTOMER'
    assert salesman.value == 'SALESMAN'
    assert admin.value == 'ADMIN'
    
def test_create_role_fail():
    with pytest.raises(RoleIsIncorrectException):
        role = Role('r')

def test_create_user_without_hashing_password():
    user = User(
        login=Login('login'),
        password=Password(b'password')
    )
    assert user.login == Login('login')
    assert user.password == b'password'
    assert user.email is None
    assert user.role == Role('CUSTOMER')
    assert user.active == True
    
def test_create_user_hashing_password():
    user = User(
        login=Login('login'),
        password=Password.hashed_password('password')
    )
    assert user.login == Login('login')
    assert user.password == b'password'
    assert user.email is None
    assert user.role == Role('CUSTOMER')
    assert user.active == True
    
def test_register_user():
    user = User.register_user(
        login='login',
        password='pas'
    )
    assert user.login == Login('login')
    assert user.password == b'pas'
    assert user.email is None
    assert user.role == Role('CUSTOMER')
    assert user.active == True
    

    