# db.py
import streamlit as st
from supabase import create_client, Client

# Minta URL dan Key ini dari temanmu
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]

# Inisialisasi koneksi Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def data_bookmark(id_user, id_manhwa):
    response = supabase.table("bookmark_user").select("*").eq("id_user", id_user).eq("id_manhwa",id_manhwa).execute()
    st.write(response)
    return response.data

def cek_login(username, password):

    response = supabase.table("User").select("*").eq("username", username).eq("password", password).execute()
    
    if response.data and len(response.data) > 0:
        user_data = response.data[0]
        return True, "Login berhasil!", user_data
    
    return False, "Username atau password salah!", None

def buat_akun_baru(username, password):

    # Cek apakah username sudah ada
    check_user = supabase.table("User").select("username").eq("username", username).execute()
    if check_user.data and len(check_user.data) > 0:
        return False, "Username sudah terdaftar! Gunakan yang lain."

    # Masukkan user baru ke tabel 'User'
    supabase.table("User").insert({
        "username": username,
        "password": password
    }).execute()
    
    return True, "Akun berhasil dibuat! Silakan kembali ke Login."
