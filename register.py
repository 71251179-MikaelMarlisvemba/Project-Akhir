# register.py
import streamlit as st
from db import buat_akun_baru  # Import fungsi insert ke Supabase

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.header("CREATE ACCOUNT", text_alignment="center")

    with st.form("form_register"):
        new_username = st.text_input("Buat Username Baru", placeholder="username baru")
        new_password = st.text_input("Buat Password Baru", type="password", placeholder="password baru")
        confirm_password = st.text_input("Konfirmasi Password", type="password", placeholder="ulangi password")
        submit = st.form_submit_button("CREATE ACCOUNT", type="primary", width="stretch")
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
# def halaman_register():
#     col1, col2, col3 = st.columns([1, 1.2, 1])

#     with col2:
#         st.header("CREATE ACCOUNT", text_alignment="center")

#         new_username = st.text_input("Buat Username Baru", placeholder="username baru")
#         new_password = st.text_input("Buat Password Baru", type="password", placeholder="password baru")
#         confirm_password = st.text_input("Konfirmasi Password", type="password", placeholder="ulangi password")

#         # Tombol Daftarkan Akun
#         if st.button("CREATE ACCOUNT", key="btn_daftar", use_container_width=True):
#             if not new_username or not new_password:
#                 st.error("Username dan Password tidak boleh kosong!")
#             elif new_password != confirm_password:
#                 st.error("Konfirmasi password tidak cocok!")
#             else:
#                 # Simpan akun baru ke tabel User di Supabase
#                 berhasil, pesan = buat_akun_baru(new_username, new_password)
#                 if berhasil:
#                     st.success(pesan)
#                 else:
#                     st.error(pesan)

#         # Tombol Kembali ke Halaman Login
#         sub_c1, sub_c2, sub_c3 = st.columns([1, 2, 1])
#         with sub_c2:
#             if st.button("Sudah punya akun? Login", type="tertiary", use_container_width=True):
#                 st.session_state.halaman = "login"
#                 st.rerun()