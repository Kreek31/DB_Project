import jwt
import datetime
import os
import psycopg2
import bcrypt
from psycopg2 import extras
from repositories.connector import get_connection


# Конфигурация
SECRET_KEY = os.getenv("SECRET_KEY")

# Хеширование пароля
def hash_password(password):
    salt = bcrypt.gensalt()  # Генерация соли
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


# Проверка пароля
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

def authenticate_user(username, password):
    """
    Проверяет учетные данные пользователя и возвращает JWT при успешной аутентификации.
    """
    query = """SELECT usr.user_id, usr.password_hash, rls.role_id FROM (SELECT user_id, password_hash, role_id FROM users WHERE username = %(user_name)s) as usr inner join roles as rls on usr.role_id=rls.role_id"""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"user_name": username})
            user = cur.fetchone()
            if user and check_password(password, bytes(user["password_hash"])):
                user_id = user["user_id"]
                user_role = user["role_id"]
                # Создаем JWT
                token = jwt.encode({
                    'user_id': user_id,
                    'user_role': user_role,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Срок действия токена
                }, SECRET_KEY, algorithm='HS256')
                return {"token": token}
    return {"error": "Неправильный логин или пароль"}

def check_user(username):
    query = """SELECT count(user_id) as users FROM users WHERE username = %(user_name)s"""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"user_name": username})
            users = cur.fetchone()
            count_users = users["users"]
            if count_users != 0:
                return {"error": "Пользователь с данным логином уже существует"}
            return {"ok": "ok"}
            
def register_user(username, password):
    query = """
        INSERT INTO users (username, password_hash, role_id)
        VALUES (%s, %s, %s) RETURNING user_id, username, password_hash, role_id;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            hashed_pass = hash_password(password)
            cur.execute(query, [username, hashed_pass, 2])
            conn.commit()
            user = cur.fetchone()
            user_id = user["user_id"]
            user_role = user["role_id"]
            # Создаем JWT
            token = jwt.encode({
                'user_id': user_id,
                'user_role': user_role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Срок действия токена
            }, SECRET_KEY, algorithm='HS256')
            return {"token": token}
        
def get_users() -> list[dict]:
    print("Получение пользователей")
    query = "SELECT user_id, username FROM users;"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()