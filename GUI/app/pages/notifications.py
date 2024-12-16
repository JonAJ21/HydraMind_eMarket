import httpx
import streamlit as st
import pandas as pd
from settings.config import services

st.set_page_config(
    page_title="Оповещения"
)

st.title("Оповещения")

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = ""
if 'refresh_token' not in st.session_state:
    st.session_state['refresh_token'] = ""
    
def get_notifications():
    
    def _get_notifications():
        with httpx.Client() as client:
            url = f"{services['notification']}{'/get'}"
            schema = {
                'token' : st.session_state['access_token'],
                'count_limit' : int(n)
            }
            response = client.request('GET', url, json=schema, headers=None)

        if response.is_error:
            return False
        
        df = pd.DataFrame(response.json()['data'])
        st.write(f"### Последние {len(df)} оповещений")
        st.dataframe(df)
    
    st.write("### Прочитать n оповещений:")
    n = st.text_input(label='')
    submit_button = st.button(label='Прочитать', on_click=_get_notifications)
    if submit_button:
        st.success('Успешно')
    
def get_unread_notifications():
    with httpx.Client() as client:
        url = f"{services['notification']}{'/get/unread'}"
        schema = {
            'token': st.session_state['access_token']
        }
        response = client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        return False
    
    st.write('### Непрочитанные оповещения')
    df = pd.DataFrame(response.json()['data'])
    st.dataframe(df)
    
    return response.json()

    
if st.session_state['access_token'] == "":
    st.write("Чтобы пользоваться сервисом оповещений надо авторизоваться")
else:
    get_notifications()
    
    get_unread_notifications()