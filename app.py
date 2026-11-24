import streamlit as st

st.set_page_config(page_title="Manhwaverse", layout="wide", page_icon="📖")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "password" not in st.session_state:
    st.session_state["password"] = ""
    
if "edit" not in st.session_state:
    st.session_state["edit"] = False

if st.session_state["logged_in"] == True and st.session_state["edit"] == False:
    pg = st.navigation(
        [
            st.Page("pages/Beranda.py", title="Beranda", default=True),
            st.Page("pages/cariManhwa.py", title="Cari Manhwa"),
            st.Page("pages/Statistik.py", title="Statistik"),
            st.Page("pages/Pengaturan.py", title="Pengaturan")
        ],
    )
    pg.run()    

    
elif st.session_state["logged_in"] == True and st.session_state["edit"] == True:
    pg = st.navigation([
        st.Page("editStatus.py", title="Edit Status")
    ], position="hidden")
    
    pg.run()
    
else:
    pg = st.navigation(
        [
            st.Page("login.py", title="Login", default=True),
            st.Page("register.py", title="Create Account"),
        ],
    position="hidden")
    
    pg.run()
    
# import streamlit as st 
# from db import cek_login
# from register import halaman_register  # Import tampilan register dari register.py

# def main():
#     st.set_page_config(page_title="Manhwaverse - Login")
#     # Sembunyikan sidebar secara total di halaman login
#     st.markdown("""
#         <style>
#             [data-testid="stSidebar"] {
#                 display: none;
#             }
#         </style>
#     """, unsafe_allow_html=True)
#     # 1. Inisialisasi data pengguna dari users.py menggunakan .copy()
#     if 'halaman' not in st.session_state:
#         st.session_state.halaman = "login"
#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False
#     if 'username' not in st.session_state:
#         st.session_state.username = None
#     if 'id_user' not in st.session_state:
#         st.session_state.id_user = None

#     # Sembunyikan sidebar di halaman Login / Register
#     st.markdown("""
#         <style>
#             [data-testid="stSidebar"] {
#                 display: none;
#             }
#         </style>
#     """, unsafe_allow_html=True)

#     # 3. Logika perpindahan halaman
#     if st.session_state.halaman == "register":
#         halaman_register()
#     else:
#         tampilkan_halaman_login()


# def tampilkan_halaman_login():
#     # Styling tombol oval abu-abu dan link create account
#     st.markdown("""
#         <style>
#         div.stButton > button[key="login_button"] {
#             background-color: #bebebe;
#             color: black;
#             border-radius: 20px;
#             border: 1.5px solid #333333;
#             font-weight: 500;
#         }
#         div.stButton > button[key="login_button"]:hover {
#             background-color: #a8a8a8;
#             color: black;
#             border: 1.5px solid #000000;
#         }
#         div.stButton > button[key="create_account_button"] {
#             text-decoration: underline;
#             color: black;
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 1.2, 1])

#     with col2:
#         st.header("LOGIN", text_alignment='center')

#         username = st.text_input("Masukkan Username", placeholder="username")
#         password = st.text_input("Masukkan Password", type="password", placeholder="password")

#         # Tombol yang mengarahkan ke halaman Register
#         sub_c1, sub_c2, sub_c3 = st.columns([1, 2, 1])
#         with sub_c2:
#             if st.button("Create Account?", type="tertiary", key="create_account_button", use_container_width=True):
#                 # Pindah ke tampilan register lalu refresh
#                 st.session_state.halaman = "register"
#                 st.rerun()

#         # Tombol Login
#         btn_c1, btn_c2, btn_c3 = st.columns([1, 1.8, 1])
#         with btn_c2:
#             if st.button("LOGIN", key="login_button", use_container_width=True):
#                 # Cek ke data yang tersimpan di st.session_state.data_pengguna
#                 if not username or not password:
#                     st.error("Username dan Password tidak boleh kosong!")
#                 else:
#                     berhasil,pesan,user_data = cek_login(username,password)
#                     if berhasil:
#                         st.session_state.logged_in = True
#                         st.session_state.username = user_data["username"]
#                         st.session_state.id_user = user_data['id_user']

#                         st.success(pesan)
#                         st.switch_page('pages/Beranda.py')
#                     else:
#                         st.error(pesan)


# if __name__ == '__main__':
#     main()
