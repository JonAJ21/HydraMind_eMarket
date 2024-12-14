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


INSERT INTO public.categories (category_id,"name",parent_category_id) VALUES
	 ('68b96257-d325-44aa-8405-503e97e08b95'::uuid,'Верхняя одежда','3f591be6-a395-4011-9e5c-a6ce77ce3d15'::uuid),
	 ('eb9c4bfd-5161-4733-82e3-72caa68eecd0'::uuid,'Шапки','68b96257-d325-44aa-8405-503e97e08b95'::uuid),
	 ('64d2fa90-9b75-4bec-9b7e-516438d38eb1'::uuid,'Куртки','68b96257-d325-44aa-8405-503e97e08b95'::uuid),
	 ('f8cc22dd-8e3f-4d06-a714-e9ddc5c35f36'::uuid,'Кофты','68b96257-d325-44aa-8405-503e97e08b95'::uuid),
	 ('0207ef60-942b-498d-a23d-a02498220f24'::uuid,'Кросовки','7d2c1d16-37ab-429e-973f-3b374e81366a'::uuid),
	 ('7d2c1d16-37ab-429e-973f-3b374e81366a'::uuid,'Обувь','3f591be6-a395-4011-9e5c-a6ce77ce3d15'::uuid);

INSERT INTO public.order_notifications (notification_id,user_id,notification_text,is_readed,time_created) VALUES
	 ('2d11544d-0779-436e-90a0-e54c8b600ac0'::uuid,'33589880-26d1-43b5-a501-29be357ac696'::uuid,'Order d22beb0e-7bc7-4ea5-adfd-40686571cc5c created. 
 Product: ebc6f1f4-e6be-4d9e-9983-111f6884dead. 
 User: 33589880-26d1-43b5-a501-29be357ac696. 
 Adress: МО, Москва, Улица, ',true,'2024-12-14 06:45:08.226181'),
	 ('74a3fe79-5148-47c5-9f67-d42016de4c56'::uuid,'33589880-26d1-43b5-a501-29be357ac696'::uuid,'Order 087a59fb-39cb-4089-89e2-6d873f9d59bc created. 
 Product: ebc6f1f4-e6be-4d9e-9983-111f6884dead. 
 User: 96fcc352-cd41-4aaf-8bf2-b8c7a3e9d6fe. 
 Adress: вф, вф, вф, ',false,'2024-12-14 06:45:08.226181'),
	 ('34608b09-9da3-4e0e-b326-f8313a091b7a'::uuid,'33589880-26d1-43b5-a501-29be357ac696'::uuid,'Order d6d0f2aa-0ef5-4d27-a06f-474b336e977b created. 
 Product: ebc6f1f4-e6be-4d9e-9983-111f6884dead. 
 User: 96fcc352-cd41-4aaf-8bf2-b8c7a3e9d6fe. 
 Adress: вф, вф, вф, ',false,'2024-12-14 06:45:08.226181');

INSERT INTO public.order_product_count (order_id,product_id,count) VALUES
	 ('d22beb0e-7bc7-4ea5-adfd-40686571cc5c'::uuid,'ebc6f1f4-e6be-4d9e-9983-111f6884dead'::uuid,1),
	 ('087a59fb-39cb-4089-89e2-6d873f9d59bc'::uuid,'ebc6f1f4-e6be-4d9e-9983-111f6884dead'::uuid,1),
	 ('087a59fb-39cb-4089-89e2-6d873f9d59bc'::uuid,'ebc6f1f4-e6be-4d9e-9983-111f6884dead'::uuid,1);

INSERT INTO public.orders (order_id,user_id,time_created,time_delivered,status,is_paid) VALUES
	 ('d22beb0e-7bc7-4ea5-adfd-40686571cc5c'::uuid,'33589880-26d1-43b5-a501-29be357ac696'::uuid,'2024-12-14 06:50:05.890845',NULL,'CREATED',false),
	 ('087a59fb-39cb-4089-89e2-6d873f9d59bc'::uuid,'96fcc352-cd41-4aaf-8bf2-b8c7a3e9d6fe'::uuid,'2024-12-14 06:50:05.890845',NULL,'CREATED',false),
	 ('d6d0f2aa-0ef5-4d27-a06f-474b336e977b'::uuid,'96fcc352-cd41-4aaf-8bf2-b8c7a3e9d6fe'::uuid,'2024-12-14 06:50:05.890845',NULL,'CREATED',false);

INSERT INTO public.products (product_id,"name",salesman_id,category_id,description,rating,price,discount_percent) VALUES
	 ('ebc6f1f4-e6be-4d9e-9983-111f6884dead'::uuid,'Ушанка','33589880-26d1-43b5-a501-29be357ac696'::uuid,'eb9c4bfd-5161-4733-82e3-72caa68eecd0'::uuid,'Шапка с ушами белая',NULL,1250.0,5.0),
	 ('120462f3-54b4-436d-be17-e7a173bcb23e'::uuid,'Нике','96fcc352-cd41-4aaf-8bf2-b8c7a3e9d6fe'::uuid,'0207ef60-942b-498d-a23d-a02498220f24'::uuid,'лдвы',NULL,10.0,1.0);

INSERT INTO public.users (user_id,login,"password",email,"role",active) VALUES
	 ('bc1406a6-e63f-4ab3-ade1-4c99e7849994'::uuid,'admin','$2b$12$h5xbGrjkgnTqEL6O5DLLm.I5DjjWwYcxhgbH5uWVqCqUhPN7uIK.q','admin@adm.ru','ADMIN',true),
	 ('e8c1619d-b631-41ae-9dfe-41609e4958e2'::uuid,'new1','$2b$12$9ocHtlwwGf2kz3f8K4NnUOldjV2xvYBJJ9jHqVK7o9CnCZpCuFTeW',NULL,'CUSTOMER',true),
	 ('fd567429-cecb-445d-a236-25ff87a06b55'::uuid,'new2','$2b$12$PMVI6JplM4YfDAc9HpkVKOX3Y4BAuIT8okUipopCuYSrIoQvp.Xsa',NULL,'CUSTOMER',true),
	 ('49f2cafc-d49a-4c18-b094-49f67eb8f187'::uuid,'new3','$2b$12$6EwQ0Uo9yuRN21QRfECbGOQ.eF985COnwGO.Us8QW0rFntXVRJfEi',NULL,'CUSTOMER',true),
	 ('33589880-26d1-43b5-a501-29be357ac696'::uuid,'salesman','$2b$12$Q3dnPtmA8v/RkCz5lMZngOqmFWYM7Knj26avzaCY7ejNtLWfVlaV6',NULL,'SALESMAN',true),
	 ('96fcc352-cd41-4aaf-8bf2-b8c7a3e9d6fe'::uuid,'new','$2b$12$QFNnyPSrzDhIghSbvzDqle8UKGHH1j5Zjn4kE.U3zxJwd/V/UUxJG',NULL,'SALESMAN',true);

INSERT INTO public.users_adresses (user_adress_id,user_id,region,locality,street,building) VALUES
	 ('8ba4e068-09f6-48b6-9b13-e9e7a3d9dd3d'::uuid,'33589880-26d1-43b5-a501-29be357ac696'::uuid,'МО','Москва','Улица',''),
	 ('ab1b50fd-fcee-434a-963a-d109b266a199'::uuid,'96fcc352-cd41-4aaf-8bf2-b8c7a3e9d6fe'::uuid,'вф','вф','вф','');