import httpx
import streamlit as st
import pandas as pd
from settings.config import services



st.set_page_config(
    page_title="Страница админа"
)

st.title("Страница админа")

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = ""
if 'refresh_token' not in st.session_state:
    st.session_state['refresh_token'] = ""
    
def make_repl():
    with httpx.Client() as client:
        url = f"{services['user']}{'/info'}"
        schema = {
            'token' : st.session_state['access_token']
        }
        response = client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        return False
    
    st.write(response.json()['role'])
    
make_repl()