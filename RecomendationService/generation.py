import uuid
import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy import create_engine, text

# Настройки подключения к базе данных
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'your_database'

# Создание подключения
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

fake = Faker()

def generate_users(n):
    users = []
    roles = ['user', 'admin', 'seller']
    for _ in range(n):
        user = {
            'user_id': str(uuid.uuid4()),
            'login': fake.user_name(),
            'password': fake.password(length=12),
            'email': fake.email(),
            'role': random.choice(roles),
            'active': random.choice([True, False])
        }
        users.append(user)
    return users

def generate_addresses(users, n):
    addresses = []
    for _ in range(n):
        address = {
            'user_adress_id': str(uuid.uuid4()),
            'user_id': random.choice(users)['user_id'],
            'region': fake.state(),
            'locality': fake.city(),
            'street': fake.street_name(),
            'building': fake.building_number()
        }
        addresses.append(address)
    return addresses

def generate_categories(n):
    categories = []
    for _ in range(n):
        category = {
            'category_id': str(uuid.uuid4()),
            'name': fake.word().capitalize(),
            'parent_category_id': None  # Для простоты все категории будут корневыми
        }
        categories.append(category)
    return categories

def generate_products(users, categories, n):
    products = []
    for _ in range(n):
        product = {
            'product_id': str(uuid.uuid4()),
            'name': fake.word().capitalize(),
            'salesman_id': random.choice([user['user_id'] for user in users if user['role'] == 'seller']),
            'category_id': random.choice(categories)['category_id'],
            'description': fake.text(max_nb_chars=200),
            'rating': round(random.uniform(1, 5), 2),
            'price': round(random.uniform(10, 1000), 2),
            'discount_percent': round(random.uniform(0, 50), 2)
        }
        products.append(product)
    return products

def generate_product_photos(products, n_per_product=3):
    photos = []
    for product in products:
        for _ in range(n_per_product):
            photo = {
                'photo_id': str(uuid.uuid4()),
                'product_id': product['product_id'],
                'photo_url': fake.image_url()
            }
            photos.append(photo)
    return photos

def generate_storages(n):
    storages = []
    for _ in range(n):
        storage = {
            'storage_id': str(uuid.uuid4()),
            'region': fake.state(),
            'locality': fake.city(),
            'street': fake.street_name(),
            'building': fake.building_number()
        }
        storages.append(storage)
    return storages

def generate_product_storage_count(products, storages, n):
    psc = []
    for _ in range(n):
        entry = {
            'product_id': random.choice(products)['product_id'],
            'storage_id': random.choice(storages)['storage_id'],
            'count': random.randint(0, 100)
        }
        psc.append(entry)
    return psc

def generate_orders(users, n):
    orders = []
    for _ in range(n):
        order = {
            'order_id': str(uuid.uuid4()),
            'user_id': random.choice(users)['user_id'],
            'time_created': fake.date_time_between(start_date='-1y', end_date='now'),
            'time_delivered': fake.date_time_between(start_date='now', end_date='+30d'),
            'status': random.choice(['pending', 'delivered', 'canceled']),
            'is_paid': random.choice([True, False])
        }
        orders.append(order)
    return orders

def generate_order_product_count(orders, products, n):
    opc = []
    for _ in range(n):
        entry = {
            'order_id': random.choice(orders)['order_id'],
            'product_id': random.choice(products)['product_id'],
            'count': random.randint(1, 5)
        }
        opc.append(entry)
    return opc

def generate_order_notifications(users, n):
    notifications = []
    for _ in range(n):
        notification = {
            'notification_id': str(uuid.uuid4()),
            'user_id': random.choice(users)['user_id'],
            'notification_text': fake.sentence(),
            'is_readed': random.choice([True, False]),
            'time_created': fake.date_time_between(start_date='-1y', end_date='now')
        }
        notifications.append(notification)
    return notifications

def insert_data(table, data):
    if not data:
        return
    keys = data[0].keys()
    columns = ', '.join(keys)
    placeholders = ', '.join([f":{key}" for key in keys])
    insert_query = text(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})")
    with engine.begin() as connection:
        connection.execute(text(f"DELETE FROM {table}"))  # Очистка таблицы перед вставкой
        connection.execute(text(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1"),) if 'id_seq' in table else None
        connection.execute(
            f"INSERT INTO {table} ({columns}) VALUES " +
            ','.join([f"({', '.join(['%s'] * len(keys))})" for _ in data]),
            [tuple(item.values()) for item in data]
        )

def main():
    with engine.connect() as connection:
        # Отключение ограничений внешних ключей для вставки данных в правильном порядке
        connection.execute(text("SET session_replication_role = 'replica';"))

        # Генерация данных
        users = generate_users(10)
        insert_data('users', users)

        addresses = generate_addresses(users, 15)
        insert_data('users_adresses', addresses)

        categories = generate_categories(5)
        insert_data('categories', categories)

        products = generate_products(users, categories, 20)
        insert_data('products', products)

        photos = generate_product_photos(products)
        insert_data('product_photos', photos)

        storages = generate_storages(5)
        insert_data('storages', storages)

        psc = generate_product_storage_count(products, storages, 50)
        insert_data('product_storage_count', psc)

        orders = generate_orders(users, 30)
        insert_data('orders', orders)

        opc = generate_order_product_count(orders, products, 60)
        insert_data('order_product_count', opc)

        notifications = generate_order_notifications(users, 20)
        insert_data('order_notifications', notifications)

        # Включение ограничений внешних ключей
        connection.execute(text("SET session_replication_role = 'origin';"))

    print("Данные успешно вставлены в базу данных.")

if __name__ == "__main__":
    main()