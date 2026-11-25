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
