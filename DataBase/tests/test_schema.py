def test_users_table_exists(db_cursor):
    db_cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_name = 'users';
    """)
    result = db_cursor.fetchone()
    assert result is not None, "Таблица 'users' не существует"

def test_users_columns(db_cursor):
    db_cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'users';
    """)
    columns = [row[0] for row in db_cursor.fetchall()]
    expected_columns = ['user_id', 'login', 'password', 'email', 'role', 'active']
    assert all(column in columns for column in expected_columns), "Не все колонки присутствуют в таблице 'users'"
