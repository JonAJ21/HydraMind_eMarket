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
    