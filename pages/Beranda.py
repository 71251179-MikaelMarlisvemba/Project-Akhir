import streamlit as st

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


# ==========================================
# KONTEN HALAMAN BERANDA
# ==========================================
st.title("Beranda - Koleksi Nama")

st.selectbox("Filter Status", ["Semua", "Belum Dibaca", "Sedang Dibaca", "Selesai Dibaca"], key="filter_status")

st.selectbox("Sort by:", ["A-Z", "Z-A"], key="sort_by")