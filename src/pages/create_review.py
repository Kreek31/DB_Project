import streamlit as st
import repositories.products
import repositories.reviews
from repositories.jwt import decode_jwt
from repositories.reviews import create_review



@st.cache_data
def get_products() -> dict[str, str]:
    print("Получение продуктов")
    products = repositories.products.get_products()

    return {product["name"]: product["product_barcode"] for product in products}

def get_reviews(barcode):
    return repositories.reviews.get_reviews(barcode)

products = get_products()

def show_create_review_page():
    if ("token" not in st.session_state):
        st.rerun()

    token = decode_jwt(st.session_state["token"])
    if ("error" in token):
        print(token["error"])
        del st.session_state["token"]
        st.rerun()

    # print(token)
    user_id = token["token"]["user_id"]
    user_role = token["token"]["user_role"]
    st.title("Написать отзыв к товару")
    selected_product = st.selectbox("Выберите продукт", products.keys())
    rating = st.slider("Рейтинг", 1, 5, 3, 1)
    review = st.text_input("Ваш отзыв")
    apply_btn = st.button("Оставить отзыв")
    if apply_btn:
        has_review = False
        product_barcode = products[selected_product]
        reviews = get_reviews(product_barcode)
        for i in reviews:
            if (user_id == i["user_id"]):
                has_review = True
                break
        if has_review:
            st.write("У вас уже есть отзыв на данный товар")
        else:
            create_review(user_id, product_barcode, review, rating)
            st.write("Отзыв успешно оставлен")
            st.rerun()