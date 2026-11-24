import streamlit as st
from db import cek_login

col1, col2, col3 = st.columns([1, 1.2, 1])

with col2:
    st.header("Login", text_alignment="center", anchor=False)

    with st.form("form_login"):
        username = st.text_input("Masukkan Username", placeholder="Username")
        password = st.text_input("Masukkan Password", type="password", placeholder="Password")
        submit = st.form_submit_button("Login", type="primary", width="stretch")
        register = st.form_submit_button("Belum punya akun? Buat Akun", type="tertiary", width="stretch")

    if register:
        st.switch_page("register.py")

    if submit:
        if username == "" or password == "":
            st.error("Username dan Password tidak boleh kosong!")
        else:
            berhasil, pesan, user_data = cek_login(username, password)
            if berhasil:
                st.session_state["logged_in"] = True
                st.session_state["username"] = user_data["username"]
                st.session_state["id_user"] = user_data["id_user"]
                st.rerun()
            else:
                st.error(pesan)

    if "berhasil_buat_akun" in st.session_state:
        st.success(st.session_state.pop("berhasil_buat_akun"), icon="✅")