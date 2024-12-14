import httpx
import streamlit as st

from settings.config import services

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = ""
if 'refresh_token' not in st.session_state:
    st.session_state['refresh_token'] = ""

st.set_page_config(
    page_title="Страница продавца"
)

st.title("Страница продавца")

st.write("### Изменить статус заказа")

def change_status(status, user_id):
    with httpx.Client() as client:
        url = f"{services['catalog']}{'/change/order/status'}"
        print(url)
        scheme_json = {
            'token' : st.session_state['access_token'],
            'order_id': order_id,
            'status': status
        }
        response = client.request('POST', url, json=scheme_json, headers=None)

    if response.is_error:
        return False
    
    
    
    
    
    with httpx.Client() as client:
        url = f"{services['notification']}{'/add/notification'}"
        scheme_json = {
            'user_id': user_id,
            'text': f'Статус заказа {order_id} изменен на {status}'
        }
        response = client.request('POST', url, json=scheme_json, headers=None)

    if response.is_error:
        return False
    
    # st.write(status)


order_id = st.text_input(label='Идентификатор заказа')
customer_id = st.text_input(label='Идентификатор пользователя')
status = st.text_input(label='Статус заказа')
    
submit_button = st.button(label='Изменить', on_click=lambda st=status, cid=customer_id: change_status(st, cid), key='change_status')
if submit_button:
    st.success("Статус успешно изменен")
else:
    st.error("Ошибка")