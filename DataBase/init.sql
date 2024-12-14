-- Active: 1733244414269@@127.0.0.1@5432@EMarket@public

CREATE TABLE users (
	user_id UUID PRIMARY KEY,
	login VARCHAR(52),
	password VARCHAR(60),
	email VARCHAR(128),
	role VARCHAR(8),
	active BOOLEAN
);

CREATE TABLE users_adresses (
	user_adress_id UUID PRIMARY KEY,
    user_id UUID,
	region VARCHAR(128),
	locality VARCHAR(128),
	street VARCHAR(128),
	building VARCHAR(16),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);


CREATE TABLE categories (
    category_id UUID PRIMARY KEY,
    name VARCHAR(256),
    parent_category_id UUID
);

CREATE TABLE products (
	product_id UUID PRIMARY KEY,
	name VARCHAR(256),
    salesman_id UUID,
    category_id UUID,
	description TEXT,
	rating float,
	price float,
	discount_percent float,
    FOREIGN KEY (salesman_id) REFERENCES users (user_id),
	FOREIGN KEY (category_id) REFERENCES categories (category_id)
);

CREATE TABLE product_photos (
	photo_id UUID PRIMARY KEY,
	product_id UUID,
	photo_url TEXT,
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);

CREATE TABLE storages (
    storage_id UUID PRIMARY KEY,
    region VARCHAR(128),
	locality VARCHAR(128),
	street VARCHAR(128),
	building VARCHAR(16)
);

CREATE TABLE product_storage_count (
    product_id UUID,
    storage_id UUID,
    count INT,
    FOREIGN KEY (product_id) REFERENCES products (product_id),
    FOREIGN KEY (storage_id) REFERENCES storages (storage_id)
);

CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID,
    time_created TIMESTAMP,
    time_delivered TIMESTAMP,
    status VARCHAR(64),
    is_paid BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE order_product_count (
    order_id UUID,
    product_id UUID,
    count INT,
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);

CREATE TABLE order_notifications (
    notification_id UUID PRIMARY KEY,
    user_id UUID,
    notification_text TEXT,
    is_readed BOOLEAN,
    time_created TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE VIEW order_product_details AS
SELECT 
    op.order_id,
    op.product_id,
    op.count AS product_count,
    p.name AS product_name,
    p.price AS product_price,
    (op.count * p.price) AS total_price
FROM 
    order_product_count op
JOIN 
    products p ON op.product_id = p.product_id;

CREATE VIEW user_notifications AS
SELECT 
    n.notification_id,
    n.notification_text,
    n.is_readed,
    n.time_created,
    u.login AS user_login
FROM 
    order_notifications n
JOIN 
    users u ON n.user_id = u.user_id;

CREATE OR REPLACE PROCEDURE add_new_product(
    p_product_id UUID,
    p_name VARCHAR,
    p_salesman_id UUID,
    p_category_id UUID,
    p_description TEXT,
    p_rating FLOAT,
    p_price FLOAT,
    p_discount_percent FLOAT,
    p_photo_url TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    -- Вставка нового продукта
    INSERT INTO products (product_id, name, salesman_id, category_id, description, rating, price, discount_percent)
    VALUES (p_product_id, p_name, p_salesman_id, p_category_id, p_description, p_rating, p_price, p_discount_percent);
    
    -- Вставка фотографии продукта
    INSERT INTO product_photos (photo_id, product_id, photo_url)
    VALUES (uuid_generate_v4(), p_product_id, p_photo_url);
END;
$$;


CREATE OR REPLACE FUNCTION check_user_exists()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM users WHERE user_id = NEW.user_id) THEN
        RAISE EXCEPTION 'User with ID % does not exist', NEW.user_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_user_exists
BEFORE INSERT ON users_adresses
FOR EACH ROW
EXECUTE FUNCTION check_user_exists();
