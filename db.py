# db.py
import streamlit as st
from supabase import create_client, Client

# Minta URL dan Key ini dari temanmu
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Inisialisasi koneksi Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def cek_login(username, password):
    """Mengecek login ke tabel 'User' di Supabase"""
    try:
        response = supabase.table("User").select("*").eq("username", username).eq("password", password).execute()
        
        if response.data and len(response.data) > 0:
            user_data = response.data[0]
            return True, "Login berhasil!", user_data
        
        return False, "Username atau password salah!", None
    except Exception as e:
        return False, f"Terjadi kesalahan database: {e}", None


def buat_akun_baru(username, password):
    """Menambahkan akun baru ke tabel 'User' di Supabase"""
    try:
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
    except Exception as e:
        return False, f"Gagal membuat akun: {e}"