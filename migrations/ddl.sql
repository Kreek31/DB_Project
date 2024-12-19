-- Таблица с информацией о ролях пользователей
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

COMMENT ON TABLE roles IS 'Информация о ролях пользователей';

COMMENT ON COLUMN roles.role_id IS 'Уникальный идентификатор роли';

COMMENT ON COLUMN roles.role_name IS 'Название роли';

-- Таблица с информацией о ролях пользователей
CREATE TABLE role_descriptions (
    description_id SERIAL PRIMARY KEY,
    role_id INT REFERENCES roles(role_id) ON DELETE CASCADE,
    description TEXT
);

COMMENT ON TABLE role_descriptions IS 'Описание ролей пользователей';

COMMENT ON COLUMN role_descriptions.description_id IS 'Уникальный идентификатор описания роли';

COMMENT ON COLUMN role_descriptions.role_id IS 'Идентификатор роли';

COMMENT ON COLUMN role_descriptions.description IS 'Описание роли';

-- Таблица для хранения информации о пользователях
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash BYTEA NOT NULL,
    role_id INT REFERENCES roles(role_id) ON DELETE CASCADE
);

COMMENT ON TABLE users IS 'Информация о пользователях';

COMMENT ON COLUMN users.user_id IS 'Уникальный идентификатор пользователя';

COMMENT ON COLUMN users.password_hash IS 'Хэш пароля пользователя';

COMMENT ON COLUMN users.role_id IS 'идентификатор роли';

-- Таблица для хранения информации о товарах
CREATE TABLE products (
    product_barcode VARCHAR(20) PRIMARY KEY,
    name VARCHAR(512),
    package_size VARCHAR(50),
    weight NUMERIC
);

COMMENT ON TABLE products IS 'Информация о товарах';

COMMENT ON COLUMN products.name IS 'Название товара';

COMMENT ON COLUMN products.product_barcode IS 'Уникальный штрихкод товара';

COMMENT ON COLUMN products.package_size IS 'Размер упаковки товара';

COMMENT ON COLUMN products.weight IS 'Вес товара';

-- Таблица для хранения отзывов
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    product_barcode VARCHAR(20) REFERENCES products(product_barcode) ON DELETE CASCADE,
    review TEXT,
    rating INT
);

COMMENT ON TABLE reviews IS 'Информация об отзывах';

COMMENT ON column reviews.review_id IS 'Уникальный идентификатор отзыва';

COMMENT ON column reviews.user_id IS 'Идентификатор пользователя';

COMMENT ON column reviews.product_barcode IS 'Штрихкод товара';

COMMENT ON column reviews.review IS 'Отзыв о товаре';

COMMENT ON column reviews.rating IS 'Рейтинг товара по отзыву';

-- Таблица для хранения информации о покупках пользователей
CREATE TABLE purchases (
    purchase_id SERIAL PRIMARY KEY,
    product_barcode VARCHAR(20) REFERENCES products(product_barcode) ON DELETE CASCADE,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    purchase_date DATE NOT NULL
);

COMMENT ON TABLE purchases IS 'Основная информация о продажах';

COMMENT ON COLUMN purchases.purchase_id IS 'Уникальный идентификатор покупки';

COMMENT ON COLUMN purchases.product_barcode IS 'Штрихкод товара';

COMMENT ON COLUMN purchases.user_id IS 'Идентификатор пользователя';

COMMENT ON COLUMN purchases.purchase_date IS 'Дата покупки';

-- Таблица для хранения цен на товары
CREATE TABLE prices (
    price_id SERIAL PRIMARY KEY,
    product_barcode VARCHAR(20) REFERENCES products(product_barcode) ON DELETE CASCADE,
    price NUMERIC NOT NULL
);


COMMENT ON TABLE prices IS 'Цены на товар';

COMMENT ON COLUMN prices.price_id IS 'Уникальный идентификатор записи цены';

COMMENT ON COLUMN prices.product_barcode IS 'Штрихкод товара';

COMMENT ON COLUMN prices.price IS 'Цена товара';

--Таблица с историей обзоров
CREATE TABLE reviews_history(
	history_id SERIAL PRIMARY KEY,
	review_id INT,
	user_id INT,
	product_barcode VARCHAR(20),
	rating INT,
	review TEXT,
	description VARCHAR(32),
	date TIMESTAMP
);

COMMENT ON TABLE reviews_history IS 'История обзоров';

COMMENT ON COLUMN reviews_history.history_id IS 'Уникальный идентификатор истории';

COMMENT ON COLUMN reviews_history.review_id IS 'Идентификатор обзора';

COMMENT ON COLUMN reviews_history.user_id IS 'Идентификатор пользователя';

COMMENT ON COLUMN reviews_history.product_barcode IS 'Штрихкод продукта';

COMMENT ON COLUMN reviews_history.rating IS 'Рейтинг обзора';

COMMENT ON COLUMN reviews_history.review IS 'Обзор продукта';

COMMENT ON COLUMN reviews_history.description IS 'Описание истории';

COMMENT ON COLUMN reviews_history.date IS 'Момент записи истории';

---------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW v_product_ratings AS
SELECT
    avg(r.rating) as total_rating,
    p.product_barcode
FROM
    products p
    LEFT JOIN reviews r ON p.product_barcode = r.product_barcode
GROUP BY
    p.product_barcode;

COMMENT ON VIEW v_product_ratings IS 'Рейтинги товаров, основанные на отзывах покупателей';

----------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION handle_reviews_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO reviews_history (review_id, user_id, product_barcode, rating, review, description, date)
    VALUES (NEW.review_id, NEW.user_id, NEW.product_barcode, NEW.rating, NEW.review, 'Создан', current_timestamp);
    RETURN NEW;
END;$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION handle_reviews_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO reviews_history (review_id, user_id, product_barcode, rating, review, description, date)
    VALUES (OLD.review_id, OLD.user_id, OLD.product_barcode, OLD.rating, OLD.review, 'Удален', current_timestamp);
    RETURN OLD;
END;$$ LANGUAGE plpgsql;



CREATE TRIGGER t_reviews_insert
AFTER INSERT ON reviews
FOR EACH ROW
EXECUTE FUNCTION handle_reviews_insert();

CREATE TRIGGER t_reviews_delete
AFTER DELETE ON reviews
FOR EACH ROW
EXECUTE FUNCTION handle_reviews_delete();

-----------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE add_review(
    p_user_id INT,
    p_product_barcode VARCHAR(20),
    p_review TEXT,
    p_rating INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO reviews (user_id, product_barcode, rating, review)
    VALUES (p_user_id, p_product_barcode, p_rating, p_review);
END;
$$;