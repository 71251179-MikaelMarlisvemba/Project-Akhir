import streamlit as st

import app

# ==========================================
# STYLING SIDEBAR (HILANGKAN APP & BIKIN PILL ABU-ABU)
# ==========================================
st.markdown("""
    <style>
        /* 1. Hilangkan tulisan 'app' (item pertama di sidebar) */
        [data-testid="stSidebarNavItems"] > li:first-child {
            display: none !important;
        }

        /* 2. Ubah menu yang aktif menjadi bentuk pill abu-abu seperti di mockup */
        [data-testid="stSidebarNavItems"] a[aria-current="page"] {
            background-color: #c4c4c4 !important;
            color: #000000 !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            padding: 8px 16px !important;
        }

        /* 3. Efek saat kursor diarahkan ke menu lain */
        [data-testid="stSidebarNavItems"] a:hover {
            border-radius: 12px !important;
            background-color: #e0e0e0 !important;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Pengaturan")


with st.container(border=True):
    st.subheader("Ganti Password")
    password_lama = st.text_input("Password lama", type="password", placeholder="Masukkan password lama")
    password_baru = st.text_input("Password baru", type="password", placeholder="Masukkan password baru")

    konfirmasi_password_baru = st.text_input("Konfirmasi password baru", type="password", placeholder="Ulangi password baru")

    if st.button("Ganti Password", use_container_width = True):
        if not password_lama or not password_baru or not konfirmasi_password_baru:
            st.error("Mohon untuk mengisi semua field 😊")
        elif password_baru != konfirmasi_password_baru:
            st.error("Konfirmasi Password Baru tidak sesuai dengan Password Baru")
        else:
            from db import supabase
            # Ambil username dari session state
            username = st.session_state.get("username")
            if username:
                # Cek apakah password lama sesuai dengan yang ada di database
                response = supabase.table("User").select("*").eq("username", username).eq("password", password_lama).execute()
                if response.data and len(response.data) > 0:
                    # Update password baru
                    supabase.table("User").update({"password": password_baru}).eq("username", username).execute()
                    st.success("Password berhasil diganti!")
                else:
                    st.error("Password lama tidak sesuai.")
            else:
                st.error("Username tidak ditemukan.")


with st.container(border=True):
    st.subheader("Export Data")



with st.container(border = True):
    st.subheader("Import Data")


if st.button('Log Out', type = 'primary', use_container_width = True):
    # Hapus data login dari session state
    if "username" in st.session_state:
        del st.session_state["username"]
    if "password" in st.session_state:
        del st.session_state["password"]
    
    #balik ke halaman login
    st.switch_page("app.py")

        