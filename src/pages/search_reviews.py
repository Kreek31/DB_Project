import streamlit as st
import repositories.authenticate
import repositories.products
import repositories.reviews
from repositories.jwt import decode_jwt
from repositories.reviews import get_rating, delete_review



@st.cache_data
def get_products() -> dict[str, str]:
    print("Получение продуктов")
    products = repositories.products.get_products()

    return {product["name"]: product["product_barcode"] for product in products}

def get_reviews(barcode):
    return repositories.reviews.get_reviews(barcode)


def get_users() -> dict[str, str]:
    print("Получение пользователей")
    users = repositories.authenticate.get_users()

    return {user["user_id"]: user["username"] for user in users}

products = get_products()

def show_search_review_page():
    users = get_users()
    print("Пользователи: ", users)
    if ("token" not in st.session_state):
        st.rerun()

    token = decode_jwt(st.session_state["token"])
    if ("error" in token):
        print(token["error"])
        del st.session_state["token"]
        st.rerun()

    user_role = token["token"]["user_role"]
    st.title("Просмотр отзывов")
    selected_product = st.selectbox("Выберите продукт", products.keys())
    product_barcode = products[selected_product]
    reviews = get_reviews(product_barcode)
    st.write("Средний рейтинг товара: ", get_rating(product_barcode))
    print("Обзоры пользователей:")
    for i in reviews:
            print(users[i["user_id"]])
            with st.expander(users[i["user_id"]]):
                review_id = i["review_id"]
                username = users[i["user_id"]]
                st.write("Пользователь: ", username)
                st.write("Рейтинг: ", i["rating"])
                st.write(i["review"])
            if user_role == 1:
                delete_btn = st.button("Удалить обзор", key=users[i["user_id"]])
                if delete_btn:
                    delete_review(review_id)
                    st.rerun()
                        