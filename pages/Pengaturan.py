import streamlit as st
import json 
import csv
from db import supabase

st.title("Pengaturan")

with st.container(border=True):
    st.subheader("Ganti Password")
    password_lama = st.text_input("Password lama", type="password", placeholder="Masukkan password lama")
    password_baru = st.text_input("Password baru", type="password", placeholder="Masukkan password baru")
    konfirmasi_password_baru = st.text_input("Konfirmasi password baru", type="password", placeholder="Ulangi password baru")
    submit = st.button("Ganti Password",type='primary', width="stretch")

if submit:
    username = st.session_state.get("username")
    if not password_lama or not password_baru or not konfirmasi_password_baru:
        st.error("Mohon untuk mengisi semua field 😊")
    elif password_baru != konfirmasi_password_baru:
        st.error("Konfirmasi Password Baru tidak sesuai dengan Password Baru")
    elif not username:
        st.error("Username tidak ditemukan.")
    else:
        response = (
            supabase.table("User").select("*").eq("username", username).eq("password", password_lama).execute()
        )
        if response.data:
            supabase.table("User").update({"password": password_baru}).eq("username", username).execute()
            st.success("Password berhasil diganti!")
        else:
            st.error("Password lama tidak sesuai.")

with st.container(border=True):
    st.subheader("Export Data")
    st.write("Unduh koleksi manhwa Anda")
    col1, col2 = st.columns([1, 1])
    with col1:
        tombol_json =st.button("Export JSON", type='secondary', use_container_width= True)
    with col2:
        tombol_excel = st.button("Export Excel", type='secondary', use_container_width= True)

with st.container(border=True):
    st.subheader("Import Data")
    st.write("Pilh file backup (.json), maks 200 MB")
    file_upload = st.file_uploader("Upload", type=["json"], accept_multiple_files=False,label_visibility="collapsed")
    if file_upload is None:
        st.caption("Belum ada file yang diunggah")

if st.button("Log Out", type="primary", width="stretch"):
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["id_user"] = None
    st.rerun()

        