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
    name VARCHAR(256)
);

CREATE TABLE sub_categories (
    sub_category_id UUID PRIMARY KEY,
    main_category_id UUID,
    name VARCHAR(256),
    FOREIGN KEY (main_category_id) REFERENCES categories (category_id)
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
	FOREIGN KEY (category_id) REFERENCES sub_categories (sub_category_id)
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
    count UUID,
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);

CREATE TABLE order_notifications (
    notification_id UUID PRIMARY KEY,
    user_id UUID,
    notification_text TEXT,
    is_readed BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);


