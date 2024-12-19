import psycopg2
import psycopg2.extras
from repositories.connector import get_connection

def get_products() -> list[dict]:
    print("Получение продуктов")
    query = "SELECT product_barcode, name FROM products;"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
