import httpx
import streamlit as st
import pandas as pd
from settings.config import services



st.set_page_config(
    page_title="Каталог"
)

st.title("Каталог")

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = ""
if 'refresh_token' not in st.session_state:
    st.session_state['refresh_token'] = ""

    
def get_categories():
    with httpx.Client() as client:
        url = f"{services['catalog']}{'/get/categories'}"
        schema = {
        }
        response = client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        return False
    
    names = []
    
    for category in response.json()['data']:
        names.append(category['name'])
    
    return names

def get_products(category_name):
    def _make_order(product_id, salesman_id):
        with httpx.Client() as client:
            url = f"{services['user']}{'/get/adresses'}"
            schema = {
                'token' : st.session_state['access_token']
            }
            response = client.request('GET', url, json=schema, headers=None)

        if response.is_error:
            return False
        
        if len(response.json()['data']) != 1:
            st.error("Должен быть один адрес")
            return False
        
        region = response.json()['data'][0]['region']
        locality = response.json()['data'][0]['locality']
        street = response.json()['data'][0]['street']
        building = response.json()['data'][0]['building']
        
        with httpx.Client() as client:
            url = f"{services['catalog']}{'/create/order'}"
            scheme_json = {
                'token' : st.session_state['access_token']
            }
            response = client.request('POST', url, json=scheme_json, headers=None)

        if response.is_error:
            return False
        
        
        order_id = response.json()['order_id']
        user_id = response.json()['user_id']
        
        with httpx.Client() as client:
            url = f"{services['catalog']}{'/add/order/product'}"
            
            scheme_json = {
                'token' : st.session_state['access_token'],
                'product_id': product_id,
                'count': 1
            }
            response = client.request('POST', url, json=scheme_json, headers=None)

        if response.is_error:
            return False
        
        with httpx.Client() as client:
            url = f"{services['notification']}{'/add/notification'}"
            scheme_json = {
                'user_id': salesman_id,
                'text': f'Order {order_id} created. \n Product: {product_id}. \n User: {user_id}. \n Adress: {region}, {locality}, {street}, {building}'
            }
            response = client.request('POST', url, json=scheme_json, headers=None)

        if response.is_error:
            return False
        
        
        # print(response.json())
        
        return True
    
    
    with httpx.Client() as client:
        url = f"{services['catalog']}{'/get/category/products'}"
        schema = {
            'category_name' : category_name,
        }
        response = client.request('GET', url, json=schema, headers=None)

    if response.is_error:
        return False
    st.divider()
    # st.write(response.json())
    
    
    for i in range(0, len(response.json()['data'])):
        product = response.json()['data'][i]
        
        st.write(f"Название: {product['name']}")
        st.write(f"Описание: {product['description']}")
        st.write(f"Рейтинг: {product['rating']}")
        st.write(f"Цена: {product['price']}")
        st.write(f"Скидка: {product['discount_percent']}%")
        
        submit_button = st.button(
            label='Заказать',
            on_click=lambda product_id=product['product_id'], salesman_id=product['salesman_id'] :_make_order(product_id, salesman_id),
            key=product['product_id']
        )
    



category = st.selectbox(
    "Выбери категорию",
    get_categories()
)


st.write(get_products(category))

# st.write(get_categories())