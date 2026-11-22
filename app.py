import streamlit as st 
from users import pengguna

def main():
    st.set_page_config(page_title = "Manhwaverse - Login")
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.usernae = False

    st.markdown("""
        <style>
        /* Tombol LOGIN oval abu-abu */
        div.stButton > button[key="login_button"] {
            background-color: #bebebe;
            color: black;
            border-radius: 20px;
            border: 1.5px solid #333333;
            font-weight: 500;
        }
        div.stButton > button[key="login_button"]:hover {
            background-color: #a8a8a8;
            color: black;
            border: 1.5px solid #000000;
        }
        /* Link Create Account dengan underline */
        div.stButton > button[key="create_account_button"] {
            text-decoration: underline;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)
    # 1. Buat 3 kolom utama agar seluruh form berada pas di tengah layar
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.header("LOGIN", text_alignment='center')
        # 2. Tambahkan placeholder="username" & placeholder="password"
        username = st.text_input("Masukkan Username", placeholder="username")
        password = st.text_input("Masukkan Password", type="password", placeholder="password")
        # 3. Create Account ditaruh di tengah di atas tombol LOGIN
        sub_c1, sub_c2, sub_c3 = st.columns([1, 2, 1])
        with sub_c2:
            if st.button("Create Account?", type="tertiary", key="create_account_button", use_container_width=True):
                st.write("Arahkan ke create account!")
        # 4. Tombol LOGIN berada di tengah dan berukuran proporsional
        btn_c1, btn_c2, btn_c3 = st.columns([1, 1.8, 1])
        with btn_c2:
            if st.button("LOGIN", key="login_button", use_container_width=True):
                if username in pengguna and pengguna[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login berhasil!")
                    st.switch_page("pages/Beranda.py")
                else:
                    st.error("Username atau password salah!")

            
    











if __name__ == '__main__':
    main()