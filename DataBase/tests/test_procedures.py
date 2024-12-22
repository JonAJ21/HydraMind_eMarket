def test_add_new_product_procedure(db_cursor):
    db_cursor.execute("""
        CALL add_new_product(
            '123e4567-e89b-12d3-a456-426614174001',
            'Test Product',
            '33589880-26d1-43b5-a501-29be357ac696',
            '68b96257-d325-44aa-8405-503e97e08b95',
            'Test description',
            4.5, 100.0, 10.0, 'http://example.com/photo.jpg'
        );
    """)
    db_cursor.connection.commit()

    db_cursor.execute("SELECT * FROM products WHERE product_id = '123e4567-e89b-12d3-a456-426614174001';")
    product = db_cursor.fetchone()
    assert product is not None, "Процедура add_new_product не добавила продукт"
