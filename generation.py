import uuid
import random
from datetime import datetime, timedelta
import time

import httpx
from faker import Faker
from sqlalchemy import create_engine, text

# Настройки подключения к базе данных
DB_USER = 'admin'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'EMarket'

# URL сервисов
AUTH_SERVICE_URL = 'http://localhost:8001'
USER_SERVICE_URL = 'http://localhost:8002'

# Access Token администратора
ADMIN_ACCESS_TOKEN = (
    "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJDVVNUT01FUiIsIm9pZCI6IjM2NWZkYWQ3LTRjYjAtNDRmMC04NzIyLTY3YmYwMGZhY2Y5YSIsInR5cGUiOiJhY2Nlc3MiLCJleHAiOjE3MzUyNDA5NDMsImlhdCI6MTczNTIzOTE0M30.Ufucd7-c3G2j8VlF-DygLHmtI-2mKu3cx1PQQ2Fvixp-unFKTHbaH13vXEVgkts0i7oc2z_kZLF7kHPFGeTM1x5BS21On6Wr-VtIzJ3KeP4XY8Fb_1jxKfAkCC3S-r_czNVwo688fJcv1n_3V88xz5XtuEBdyiWaQG5b9NJB-nOF7b0EBPEX56-TQqPAXBofIz06EeakedJmyxwbrnI5ylR239_BuKpVARB1szVMmxNZSYcrXcHFxm3j2KTxefMYOFjnKLnx5Vj3wVdS2XPy3OfGjD-9OjOWZH9wHevmickCGP3AYUm7b-uTpIRkW7RU46MaREv2FoSnTfZ9Ejq0_A"
)

# Создание подключения к PostgreSQL
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

fake = Faker()


def register_command(login, password):
    """
    Регистрирует пользователя через Auth API.
    Возвращает user_id (oid) или False при ошибке.
    """
    with httpx.Client() as client:
        url = f"{AUTH_SERVICE_URL}/auth/register"
        payload = {
            'login': login,
            'password': password
        }
        try:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get('oid')
        except httpx.HTTPError as e:
            print(f"[ERROR] Не удалось зарегистрировать пользователя '{login}': {e}")
            return False


def login_command(login, password):
    """
    Авторизует пользователя через Auth API.
    Возвращает access_token или False при ошибке.
    """
    with httpx.Client() as client:
        url = f"{AUTH_SERVICE_URL}/auth/login"
        payload = {
            'login': login,
            'password': password
        }
        try:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get('access_token')
        except httpx.HTTPError as e:
            print(f"[ERROR] Не удалось авторизовать пользователя '{login}': {e}")
            return False


def change_role(admin_token, login, new_role):
    """
    Изменяет роль пользователя через User Service API.
    Возвращает True при успехе или False при ошибке.
    """
    with httpx.Client() as client:
        url = f"{USER_SERVICE_URL}/user/change/role"
        payload = {
            'token': admin_token,
            'login': login,
            'new_role': new_role
        }
        headers = {
            'Authorization': f"Bearer {admin_token}"
        }
        try:
            response = client.put(url, json=payload, headers=headers)
            response.raise_for_status()
            return True
        except httpx.HTTPError as e:
            print(f"[ERROR] Не удалось изменить роль пользователя '{login}': {e}")
            return False


def change_email(user_id, access_token, new_email):
    """
    Меняет электронную почту пользователя через User Service API.
    Возвращает True при успехе или False при ошибке.
    """
    with httpx.Client() as client:
        url = f"{USER_SERVICE_URL}/user/change/email"
        payload = {
            'token': access_token,
            'new_email': new_email
        }
        try:
            response = client.put(url, json=payload)
            response.raise_for_status()
            return True
        except httpx.HTTPError as e:
            print(f"[ERROR] Не удалось изменить email для пользователя ID '{user_id}': {e}")
            return False

def generate_users(n):
    """
    Генерирует n пользователей. По умолчанию все роли – CUSTOMER,
    но с некоторой вероятностью меняем роль на SALESMAN.
    """
    users = []
    for _ in range(n):
        login = fake.unique.user_name()
        password = fake.password(length=12)
        role = 'CUSTOMER'
        user_id = register_command(login, password)
        if not user_id:
            continue

        access_token = login_command(login, password)
        if not access_token:
            print(f"[ERROR] Не удалось получить access_token для '{login}' — пользователь пропущен.")
            continue

        # Генерация нового email
        new_email = fake.email()
        if not change_email(user_id, access_token, new_email):
            print(f"[WARN] Не удалось изменить email для пользователя '{login}'.")

        if random.random() < 0.55:
            success = change_role(ADMIN_ACCESS_TOKEN, login, 'SALESMAN')
            if success:
                role = 'SALESMAN'
            else:
                print(f"[WARN] Пользователь '{login}' остался CUSTOMER, т.к. не удалось изменить роль.")

        user = {
            'user_id': user_id,
            'login': login,
            'email': new_email,  # Используем новый email
            'role': role
        }
        users.append(user)
        print(f"[OK] Пользователь зарегистрирован: {login} (ID: {user_id}, Роль: {role}, Email: {new_email})")

    return users



def generate_adresses(users, n):
    adresses = []
    for _ in range(n):
        adresses.append({
            'user_adress_id': str(uuid.uuid4()),
            'user_id': random.choice(users)['user_id'],
            'region': fake.state(),
            'locality': fake.city(),
            'street': fake.street_name(),
            'building': fake.building_number()
        })
    return adresses


def generate_categories(n):
    """
    Генерирует n категорий (у всех parent_category_id = None для простоты).
    """
    categories = []
    for _ in range(n):
        categories.append({
            'category_id': str(uuid.uuid4()),
            'name': fake.unique.word().capitalize(),
            'parent_category_id': None
        })
    return categories


def generate_products(users, categories, n):
    """
    Генерирует n продуктов. Продаёт их случайный SALESMAN.
    """
    sellers = [u['user_id'] for u in users if u['role'] == 'SALESMAN']
    if not sellers:
        raise ValueError("Нет пользователей с ролью 'SALESMAN'. Без них не получится генерировать продукты.")

    products = []
    for _ in range(n):
        products.append({
            'product_id': str(uuid.uuid4()),
            'name': fake.unique.word().capitalize(),
            'salesman_id': random.choice(sellers),
            'category_id': random.choice(categories)['category_id'],
            'description': fake.text(max_nb_chars=200),
            'rating': round(random.uniform(1, 5), 2),
            'price': round(random.uniform(10, 1000), 2),
            'discount_percent': round(random.uniform(0, 50), 2)
        })
    return products


def generate_product_photos(products, n_per_product=3):
    """
    Генерирует по n_per_product фото на каждый товар.
    """
    photos = []
    for product in products:
        for _ in range(n_per_product):
            photos.append({
                'photo_id': str(uuid.uuid4()),
                'product_id': product['product_id'],
                'photo_url': fake.image_url()
            })
    return photos


def generate_storages(n):
    """
    Генерирует n записей о складах.
    """
    storages = []
    for _ in range(n):
        storages.append({
            'storage_id': str(uuid.uuid4()),
            'region': fake.state(),
            'locality': fake.city(),
            'street': fake.street_name(),
            'building': fake.building_number()
        })
    return storages


def generate_product_storage_count(products, storages, n):
    """
    Создаёт n связей между продуктами и складами с указанием количества.
    """
    psc = []
    for _ in range(n):
        psc.append({
            'product_id': random.choice(products)['product_id'],
            'storage_id': random.choice(storages)['storage_id'],
            'count': random.randint(0, 100)
        })
    return psc


def generate_orders(users, n):
    """
    Генерирует n заказов, случайно распределяя по пользователям.
    """
    orders = []
    for _ in range(n):
        created_time = fake.date_time_between(start_date='-1y', end_date='now')
        delivered_time = created_time + timedelta(days=random.randint(1, 30))
        orders.append({
            'order_id': str(uuid.uuid4()),
            'user_id': random.choice(users)['user_id'],
            'time_created': created_time,
            'time_delivered': delivered_time,
            'status': random.choice(['pending', 'delivered', 'canceled']),
            'is_paid': random.choice([True, False])
        })
    return orders


def generate_order_product_count(orders, products, n):
    """
    Генерирует записи для связи заказы-продукты.
    """
    opc = []
    for _ in range(n):
        opc.append({
            'order_id': random.choice(orders)['order_id'],
            'product_id': random.choice(products)['product_id'],
            'count': random.randint(1, 5)
        })
    return opc


def generate_order_notifications(users, n):
    """
    Генерирует уведомления для пользователей о заказах или событиях.
    """
    notifications = []
    for _ in range(n):
        notifications.append({
            'notification_id': str(uuid.uuid4()),
            'user_id': random.choice(users)['user_id'],
            'notification_text': fake.sentence(),
            'is_readed': random.choice([True, False]),
            'time_created': fake.date_time_between(start_date='-1y', end_date='now')
        })
    return notifications




def insert_data(table, data):
    if not data:
        return
    keys = data[0].keys()
    columns = ', '.join(keys)
    placeholders = ', '.join([f":{key}" for key in keys])
    insert_query = text(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})")
    with engine.begin() as connection:
        # Очистка таблицы перед вставкой
        connection.execute(text(f"DELETE FROM {table}"))

        # Вставка данных
        connection.execute(insert_query, data)




def main():
    try:
        users = generate_users(5)
        if not users:
            print("[ERROR] Не удалось создать ни одного пользователя, прерываем генерацию.")
            return

        addresses = generate_adresses(users, 100)
        insert_data('users_adresses', addresses)

        categories = generate_categories(20)
        insert_data('categories', categories)

        products = generate_products(users, categories, 200)
        insert_data('products', products)

        photos = generate_product_photos(products, n_per_product=3)
        insert_data('product_photos', photos)

        storages = generate_storages(20)
        insert_data('storages', storages)

        psc = generate_product_storage_count(products, storages, 500)
        insert_data('product_storage_count', psc)

        orders = generate_orders(users, 300)
        insert_data('orders', orders)

        opc = generate_order_product_count(orders, products, 600)
        insert_data('order_product_count', opc)

        notifications = generate_order_notifications(users, 100)
        insert_data('order_notifications', notifications)

    except Exception as e:
        print(f"[FATAL] Произошла ошибка при генерации данных: {e}")
    else:
        print("[OK] Данные успешно вставлены в базу.")


if __name__ == "__main__":
    main()