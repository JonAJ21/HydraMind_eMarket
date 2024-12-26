import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.neighbors import NearestNeighbors
from datetime import datetime

# Настройки подключения к базе данных
DB_USER = 'admin'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'EMarket'

# Создание подключения
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


def load_data():
    """
    Загружает данные о заказах, продуктах и пользователях из базы данных.
    """
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
    """
    Создает матрицу взаимодействий пользователей и продуктов.
    """
    user_product_matrix = orders_df.pivot_table(
        index='user_id',
        columns='product_id',
        values='count',
        aggfunc='sum',
        fill_value=0
    )
    return user_product_matrix


def train_knn(user_product_matrix, n_neighbors=6):
    """
    Обучает модель K-Nearest Neighbors на основе матрицы взаимодействий.
    """
    n_users = user_product_matrix.shape[0]
    effective_n_neighbors = min(n_neighbors, n_users)

    if effective_n_neighbors < 2:
        raise ValueError("Недостаточно пользователей для обучения модели KNN.")

    model_knn = NearestNeighbors(
        metric='cosine',
        algorithm='brute',
        n_neighbors=effective_n_neighbors,
        n_jobs=-1
    )
    model_knn.fit(user_product_matrix.values)
    return model_knn, effective_n_neighbors


def get_recommendations(user_id, user_product_matrix, model_knn, effective_n_neighbors, num_recommendations=5):
    """
    Генерирует рекомендации для заданного пользователя.
    """
    if user_id not in user_product_matrix.index:
        print(f"Пользователь с ID {user_id} не найден.")
        return []

    # Вектор пользователя
    user_vector = user_product_matrix.loc[user_id].values.reshape(1, -1)

    # Поиск ближайших соседей
    distances, indices = model_knn.kneighbors(user_vector, n_neighbors=effective_n_neighbors)

    # Получение ID соседей (исключая самого пользователя)
    similar_users = []
    for idx in indices.flatten():
        similar_user_id = user_product_matrix.index[idx]
        if similar_user_id != user_id:
            similar_users.append(similar_user_id)

    if not similar_users:
        return []

    # Суммирование покупок соседей
    similar_users_purchases = user_product_matrix.loc[similar_users].sum(axis=0)

    # Исключение товаров, уже купленных пользователем
    purchased = user_product_matrix.loc[user_id]
    recommendations = similar_users_purchases[purchased == 0].sort_values(ascending=False)

    # Возвращение топ-N рекомендаций
    top_recommendations = recommendations.head(num_recommendations).index.tolist()
    return top_recommendations


def save_recommendations(user_id, recommended_products):
    """
    Сохраняет рекомендации в базу данных.
    """
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
        'generated_at': datetime.now()
    }
    with engine.connect() as connection:
        connection.execute(text(insert_query), data)


def generate_and_save_all_recommendations():
    """
    Генерирует и сохраняет рекомендации для всех пользователей.
    """
    orders_df, products_df, users_df = load_data()
    user_product_matrix = create_user_product_matrix(orders_df)

    try:
        model_knn, effective_n_neighbors = train_knn(user_product_matrix, n_neighbors=6)
    except ValueError as e:
        print(f"Ошибка при обучении модели KNN: {e}")
        return

    for user_id in user_product_matrix.index:
        try:
            recs = get_recommendations(
                user_id,
                user_product_matrix,
                model_knn,
                effective_n_neighbors,
                num_recommendations=5
            )
            if recs:
                save_recommendations(user_id, recs)
                print(f"Рекомендации для пользователя {user_id}: {recs}")
            else:
                print(f"Нет рекомендаций для пользователя {user_id}.")
        except Exception as e:
            print(f"Ошибка при генерации рекомендаций для пользователя {user_id}: {e}")

    print("Рекомендации сгенерированы и сохранены в базе данных.")


def get_user_recommendations_with_names(user_id):
    query = """
    SELECT p.name
    FROM user_recommendations ur
    JOIN products p ON p.product_id = ANY(ur.recommended_products)
    WHERE ur.user_id = :user_id
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {'user_id': user_id}).fetchall()
    if result:
        return [row[0] for row in result]
    else:
        return []


if __name__ == "__main__":
    generate_and_save_all_recommendations()

    orders_df, products_df, users_df = load_data()
    if not users_df.empty:
        example_user_id = users_df['user_id'].iloc[0]
        try:
            recommended_products = get_user_recommendations_with_names(example_user_id)
            print(f"\nРекомендованные продукты для пользователя {example_user_id}: {recommended_products}")
        except Exception as e:
            print(f"Ошибка при получении рекомендаций для пользователя {example_user_id}: {e}")
    else:
        print("Нет пользователей для получения рекомендаций.")