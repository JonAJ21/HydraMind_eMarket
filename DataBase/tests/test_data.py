def test_insert_user(db_cursor):
    db_cursor.execute("""
        INSERT INTO users (user_id, login, password, email, role, active)
        VALUES ('123e4567-e89b-12d3-a456-426614174000', 'testuser', 'password', 'test@example.com', 'CUSTOMER', true);
    """)
    db_cursor.connection.commit()

    db_cursor.execute("""
        SELECT * FROM users WHERE login = 'testuser';
    """)
    user = db_cursor.fetchone()
    assert user is not None, "Пользователь не был добавлен"

def test_order_view(db_cursor):
    db_cursor.execute("""
        SELECT * FROM order_product_details WHERE order_id = 'd22beb0e-7bc7-4ea5-adfd-40686571cc5c';
    """)
    order_details = db_cursor.fetchall()
    assert len(order_details) > 0, "Нет данных по заказу в представлении order_product_details"
