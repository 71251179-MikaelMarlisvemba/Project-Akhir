# register.py
import streamlit as st
from db import buat_akun_baru

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.header("Create Account", text_alignment="center")

    with st.form("form_register"):
        new_username = st.text_input("Buat Username Baru", placeholder="Username")
        new_password = st.text_input("Buat Password Baru", type="password", placeholder="Password")
        confirm_password = st.text_input("Konfirmasi Password", type="password", placeholder="Ulangi Password")
        submit = st.form_submit_button("Create Account", type="primary", width="stretch")
        kembali = st.form_submit_button("Sudah punya akun? Login", type='tertiary',width="stretch")

    if kembali:
        st.switch_page("login.py")

    if submit:
        if  new_username == "" or  new_password == "":
            st.error("Username dan Password tidak boleh kosong!")
        elif new_password != confirm_password:
            st.error("Konfirmasi password tidak cocok!")
        elif len(new_password) <8:
            st.error("Panjang minimal password 8") 
        else:
            berhasil, pesan = buat_akun_baru(new_username, new_password)
            if berhasil:
                st.session_state["berhasil_buat_akun"] = ("Akun berhasil dibuat!")
                st.switch_page("login.py")
            else:
                st.error(pesan)