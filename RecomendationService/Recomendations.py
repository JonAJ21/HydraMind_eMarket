import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.neighbors import NearestNeighbors
import numpy as np
import uuid
from datetime import datetime

# Настройки подключения к базе данных
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'your_database'

# Создание подключения
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def load_data():
    # Загрузка данных о заказах и продуктах
    orders_query = """
    SELECT o.user_id, opc.product_id, opc.count
    FROM orders o
    JOIN order_product_count opc ON o.order_id = opc.order_id
    WHERE o.status = 'delivered' AND o.is_paid = TRUE
    """
    orders_df = pd.read_sql(orders_query, engine)

    products_query = "SELECT product_id, name, category_id FROM products"
    products_df = pd.read_sql(products_query, engine)

    users_query = "SELECT user_id, login FROM users"
    users_df = pd.read_sql(users_query, engine)
    
    return orders_df, products_df, users_df

def create_user_product_matrix(orders_df):
    user_product_matrix = orders_df.pivot_table(index='user_id', 
                                               columns='product_id', 
                                               values='count', 
                                               aggfunc='sum', 
                                               fill_value=0)
    return user_product_matrix

def train_knn(user_product_matrix):
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=6, n_jobs=-1)
    model_knn.fit(user_product_matrix.values)
    return model_knn

def get_recommendations(user_id, user_product_matrix, model_knn, num_recommendations=5):
    if user_id not in user_product_matrix.index:
        print(f"Пользователь с ID {user_id} не найден.")
        return []
    
    # Вектор пользователя
    user_vector = user_product_matrix.loc[user_id].values.reshape(1, -1)
    
    # Поиск ближайших соседей
    distances, indices = model_knn.kneighbors(user_vector, n_neighbors=6)
    
    # Получение ID соседей (исключая самого пользователя)
    similar_users = user_product_matrix.index[indices.flatten()][1:]
    
    # Суммирование покупок соседей
    similar_users_purchases = user_product_matrix.loc[similar_users].sum(axis=0)
    
    # Исключение товаров, уже купленных пользователем
    purchased = user_product_matrix.loc[user_id]
    recommendations = similar_users_purchases[purchased == 0].sort_values(ascending=False)
    
    # Возвращение топ-N рекомендаций
    top_recommendations = recommendations.head(num_recommendations).index.tolist()
    return top_recommendations

def save_recommendations(user_id, recommended_products):
    insert_query = """
    INSERT INTO user_recommendations (user_id, recommended_products, generated_at)
    VALUES (:user_id, :recommended_products, :generated_at)
    ON CONFLICT (user_id) 
    DO UPDATE SET recommended_products = EXCLUDED.recommended_products,
                  generated_at = EXCLUDED.generated_at
    """
    data = {
        'user_id': user_id,
        'recommended_products': recommended_products,
        'generated_at': datetime.utcnow()
    }
    with engine.begin() as connection:
        connection.execute(text(insert_query), **data)

def generate_and_save_all_recommendations():
    orders_df, products_df, users_df = load_data()
    user_product_matrix = create_user_product_matrix(orders_df)
    model_knn = train_knn(user_product_matrix)
    
    for user_id in user_product_matrix.index:
        recs = get_recommendations(user_id, user_product_matrix, model_knn)
        if recs:
            save_recommendations(user_id, recs)
            print(f"Рекомендации для пользователя {user_id}: {recs}")
        else:
            print(f"Нет рекомендаций для пользователя {user_id}.")

if __name__ == "__main__":
    generate_and_save_all_recommendations()
    print("Рекомендации сгенерированы и сохранены в базе данных.")