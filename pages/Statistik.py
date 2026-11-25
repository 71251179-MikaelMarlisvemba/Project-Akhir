import streamlit as st

st.title("Statistik")

x1,x2,x3 = st.columns(3)
with x1:
    with st.container(border=True):
        st.write("Total Bookmark")

with x2:
    with st.container(border=True):
        st.write("Selesai Dibaca")

with x3:
    with st.container(border=True):
        st.write("Kategori Favorit")