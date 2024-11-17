from domain.entities.users import User
from domain.values.email import Email
from domain.values.password import Password
from domain.values.login import Login

import pytest

def test_create_user():
    login = Login('hellosd')
    password = Password('dada131s')
    email = Email('jdakl2')
    
    user = User(login=login, password=password, email=email)
    
    assert user.login == login
    assert user.password == password
    assert user.email == email
    
    