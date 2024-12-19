import streamlit as st
from repositories.authenticate import authenticate_user, check_user, register_user

def show_authenticate_page():
    st.title("Авторизация")
    with st.form("authorization"):
        username = st.text_input('Логин:', max_chars=50)
        password = st.text_input('Пароль:', type="password")
        authorise_btn = st.form_submit_button('Войти')
        register_btn = st.form_submit_button('Регистрация')
        if authorise_btn:
            status = authenticate_user(username, password)
            if "error" in status:
                st.write(status["error"])
            elif "token" in status:
                st.session_state.token = status["token"]
                st.write("Авторизация успешна")
                print(st.session_state["token"])
                st.rerun()
                
        if register_btn:
            status = check_user(username)
            if "error" in status:
                st.write(status["error"])
            else:
                st.session_state.token = register_user(username, password)["token"]
                st.write("Авторизация успешна")
                print(st.session_state["token"])
                st.rerun()
                