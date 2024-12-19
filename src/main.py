import streamlit as st
from pages.authenticate_user import show_authenticate_page
from pages.create_review import show_create_review_page
from pages.search_reviews import show_search_review_page


# Главная логика приложения с навигацией
def main():
    if "token" not in st.session_state:
        show_authenticate_page()
    else:
        st.sidebar.title("Навигация")
        page = st.sidebar.radio(
            "Перейти к странице",
            ["Написать отзыв к товару", "Просмотреть отзывы"],
        )
        if page == "Написать отзыв к товару":
            show_create_review_page()
        elif page == "Просмотреть отзывы":
            show_search_review_page()


if __name__ == "__main__":
    main()