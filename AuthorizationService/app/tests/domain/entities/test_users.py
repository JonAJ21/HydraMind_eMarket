import pytest

from domain.events.user import NewUserAddedEvent
from domain.exceptions.role import RoleIsIncorrectException
from domain.values.role import Role
from domain.exceptions.email import EmailTooLongException
from domain.exceptions.login import LoginTooLongException
from domain.values.login import Login
from domain.values.password import Password
from domain.exceptions.password import PasswordTooLongException
from domain.values.email import Email
from domain.entities.user import User

def test_create_login():
    login = Login('login')
    assert login.value == 'login'
    
def test_create_login_too_long():
    with pytest.raises(LoginTooLongException):
        login = Login('l' * 300)

def test_create_password():
    password = Password('password')
    assert password.value == 'password'
    
def test_create_password_too_long():
    with pytest.raises(PasswordTooLongException):
        password = Password('r' * 300) 
        
def test_create_email():
    email = Email('email')
    assert email.value == 'email'
    
def test_create_password_too_long():
    with pytest.raises(EmailTooLongException):
        email = Email('r' * 300)
        
def test_create_role():
    customer = Role('CUSTOMER')
    salesman = Role('SALESMAN')
    admin = Role('ADMIN')
    assert customer.value == 'CUSTOMER'
    assert salesman.value == 'SALESMAN'
    assert admin.value == 'ADMIN'
    
def test_create_role_incorrect():
    with pytest.raises(RoleIsIncorrectException):
        role = Role('r')

def test_create_user():
    user = User(login='login',
                password='password',
                email='email',
                role='CUSTOMER')
    assert user.login == 'login'
    assert user.password == 'password'
    assert user.email == 'email'
    assert user.role == 'CUSTOMER'
   
    
def test_new_user_events():
    login = Login('login')
    password = Password('password')
    email = Email('email')
    role = Role('CUSTOMER')
    
    user = User.add_user(login=login, password=password, email=email, role=role)
    events = user.pull_events()
    pulled_events = user.pull_events()
    assert not pulled_events, pulled_events
    assert len(events) == 1, events
    
    new_event = events[0]
    
    assert isinstance(new_event, NewUserAddedEvent), new_event
    assert new_event.user_oid == user.oid
    assert new_event.login == login
    assert new_event.password == password
    assert new_event.email == email
    assert new_event.role == role
    

    