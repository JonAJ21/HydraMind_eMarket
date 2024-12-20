import httpx
import streamlit as st

from settings.config import services

st.set_page_config(
    page_title="Авторизация / Регистрация"
)

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = ""
if 'refresh_token' not in st.session_state:
    st.session_state['refresh_token'] = ""

def login_command(login, password):
    
    with httpx.Client() as client:
        url = f"{services['auth']}{'/login'}"
        schema = {
            'login': login,
            'password': password
        }
        response = client.request('POST', url, json=schema, headers=None)
    
    if response.is_error:
        return False
    
    # st.write(response.json())
    
    
    st.session_state['access_token'] = response.json()['access_token']
    st.session_state['refresh_token'] = response.json()['refresh_token']
    
    
    return True

def register_command(login, password):
    
    with httpx.Client() as client:
        url = f"{services['auth']}{'/register'}"
        schema = {
            'login': login,
            'password': password
        }
        response = client.request('POST', url, json=schema, headers=None)
    
    if response.is_error:
        return False
    
    return True

# Заголовок приложения
st.title("Авторизация / Регистрация")

# Переключатель между формами
form_type = st.radio("Выберите действие:", ("Войти", "Зарегистрироваться"))

if form_type == "Войти":
    # Создание формы для авторизации
    with st.form(key='login_form'):
        login = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type='password')
        submit_button = st.form_submit_button(label='Войти')

    # Проверка учетных данных при отправке формы
    if submit_button:
        if login_command(login, password):
            st.success("Успешная авторизация!")
            # Здесь можно добавить код для перехода к защищенному контенту
        else:
            st.error("Неверное имя пользователя или пароль.")

else:  # Если выбрана регистрация
    # Создание формы для регистрации
    with st.form(key='registration_form'):
        new_login = st.text_input("Имя пользователя")
        new_password = st.text_input("Пароль", type='password')
        register_button = st.form_submit_button(label='Зарегистрироваться')

    # Регистрация пользователя при отправке формы
    if register_button:
        if register_command(new_login, new_password):
           st.success("Вы успешно зарегистрировались. Не забудьте авторизоваться.")
        else:
            st.error("Не удалось зарегистрироваться. Попробуйте другой логин.")
           
            