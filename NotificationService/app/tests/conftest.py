import pytest
import psycopg2

@pytest.fixture
def db_cursor():
    # Настрой подключение к базе данных
    conn = psycopg2.connect(
        dbname="EMarket",
        user="admin",
        password="password",
        host="localhost",
        port="5433"
    )
    cursor = conn.cursor()
    
    # Передаем курсор тестам
    yield cursor
    
    # Закрываем соединение после выполнения тестов
    cursor.close()
    conn.close()
