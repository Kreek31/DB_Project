import psycopg2
import psycopg2.extras
from repositories.connector import get_connection

def create_review(user_id: int, barcode: str, review: str, rating: int):
    query = """
        CALL add_review(%s, %s, %s, %s);
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (user_id, barcode, review, rating))
            conn.commit()

def get_rating(barcode):
    query = """SELECT total_rating FROM v_product_ratings WHERE product_barcode = %(barcode)s;"""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"barcode": barcode})
            return cur.fetchall()[0]["total_rating"]
   
def get_reviews(barcode):
    query = """SELECT user_id, review, rating, review_id FROM reviews WHERE product_barcode = %(barcode)s;"""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"barcode": barcode})
            return cur.fetchall()
        
def delete_review(review_id):
    query = """DELETE FROM reviews WHERE review_id = %(review_id)s;"""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"review_id": review_id})
            conn.commit()