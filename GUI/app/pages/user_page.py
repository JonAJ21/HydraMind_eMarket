import httpx
import streamlit as st

from settings.config import services

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = ""
if 'refresh_token' not in st.session_state:
    st.session_state['refresh_token'] = ""

st.set_page_config(
    page_title="Личный кабинет"
)

st.title("Личный кабинет")


def get_user_info():
    with httpx.Client() as client:
        url = f"{services['user']}{'/info'}"
        schema = {
            'token' : st.session_state['access_token']
        }
        response = client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        st.write("Error: failed to get user info")
        return False
    
    st.write('Логин: ', response.json()['login'])
    st.write('Почта: ', response.json()['email'])
    
    if response.json()['role'] == 'CUSTOMER':   
        st.write('Роль: покупатель')
    if response.json()['role'] == 'SALESMAN':   
        st.write('Роль: продавец')
    if response.json()['role'] == 'ADMIN':   
        st.write('Роль: админ')
    
    return True
    
def change_email():
    def _change_email():
        with httpx.Client() as client:
            url = f"{services['user']}{'/change/email'}"
            schema = {
                'token' : st.session_state['access_token'],
                'new_email' : email
            }
            response = client.request('PUT', url, json=schema, headers=None)

        if response.is_error:
            return False
        
        return True
    
    st.write("### Изменить почту:")
    email = st.text_input(label='')
    submit_button = st.button(label='Изменить', on_click=_change_email)
    
    if submit_button:
        st.success("Почта успешно изменена")


def delete_adress(adress_id):
    def _delete_adress():
        with httpx.Client() as client:
            url = f"{services['user']}{'/delete/adress'}"
            schema = {
                'token' : st.session_state['access_token'],
                'adress_id': adress_id
            }
            response = client.request('PUT', url, json=schema, headers=None)

        if response.is_error:
            False
        return True
    
    button = st.button(label='Удалить', on_click=_delete_adress, key=adress_id)
    if button:
        st.success("Адресс успешно удален")
    
    return True
                  
def get_adresses():
    st.write("### Адреса:")
    with httpx.Client() as client:
        url = f"{services['user']}{'/get/adresses'}"
        schema = {
            'token' : st.session_state['access_token']
        }
        response = client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        return False
    
    # st.write(response.json())
    
    for i in range(0, len(response.json()['data'])):
        adress = response.json()['data'][i]
        st.write(f"{i + 1} : {adress['region']}, {adress['locality']}, {adress['street']}, {adress['building']}")
        delete_adress(adress['adress_id'])
    
        
        # st.write(adress)
    
    
    
    return True

def add_adress():
    def _add_adress():
        with httpx.Client() as client:
            url = f"{services['user']}{'/add/adress'}"
            schema = {
                'token' : st.session_state['access_token'],
                'region' : region,
                'locality': locality,
                'street' : street,
                'building' : building
            }
            response = client.request('POST', url, json=schema, headers=None)

        if response.is_error:
            return False
        
        return True
    
    st.write("### Добавить новый адресс:")
    region = st.text_input(label='Регион')
    locality= st.text_input(label='Населенный пункт')
    street= st.text_input(label='Улица')
    building= st.text_input(label='Дом')
    
    submit_button = st.button(label='Добавить', on_click=_add_adress)
    if submit_button:
        st.success("Адресс успешно добавлен")
    else:
        st.error("Не удалось добавить адресс")
    
    
def change_role():
    with httpx.Client() as client:
        url = f"{services['user']}{'/info'}"
        schema = {
            'token' : st.session_state['access_token']
        }
        response = client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        st.write("Error: failed to get user info")
        return False
    
    if response.json()['role'] != 'ADMIN':
        return False
    
    def _change_role():
        with httpx.Client() as client:
            url = f"{services['user']}{'/change/role'}"
            schema = {
                'token' : st.session_state['access_token'],
                'login': login,
                'new_role': new_role
            }
            response = client.request('PUT', url, json=schema, headers=None)

        if response.is_error:
            return False
        
        return True
    
    
    
    st.write("### Изменить роль:")
    login = st.text_input(label='Логин')
    new_role = st.text_input(label='Роль')
    
    submit_button = st.button(label='Изменить', on_click=_change_role, key='change_role')
    if submit_button:
        st.success("Роль успешно изменена")
    else:
        st.error("Ошибка")
    
    
    


if st.session_state['access_token'] == "":
    st.write("Чтобы войти в личный кабинет надо авторизоваться")
else:
    get_user_info()
    
    change_email()
    
    get_adresses()
    
    add_adress()
    
    change_role()
    # delete_adress()
   
    
    # st.write("kdls")
    # st.write(st.session_state['access_token'])