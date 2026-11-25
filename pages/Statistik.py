import streamlit as st
from db import supabase

manhwa = supabase.table("bookmark_user").select("*").eq("id_user", st.session_state["id_user"]).execute()
data = manhwa.data

st.title("Statistik")

genre = {}
for i in data:
    bersih = i["genre"].split(", ")
    for j in bersih:
        if j not in genre:
            genre[j] = 1
        else:
            genre[j] += 1

with st.container(width="stretch", height="stretch"):    
    x1,x2,x3 = st.columns(3)
    with x1:
        with st.container(border=True,height="stretch"):
            st.write("Total Bookmark")
            total = len(data)
            st.header(total)

    with x2:
        with st.container(border=True,height="stretch"):
            st.write("Selesai Dibaca")
            counter = 0
            for i in data:
                if i["status"] == "Selesai Dibaca":
                    counter += 1
            st.header(counter)

    with x3:
        with st.container(border=True):
            st.write("Kategori Favorit")
            maks = max(genre.values())
            text = ""
            for kategori, jumlah in genre.items():
                if text == "" and jumlah == maks:
                    text = kategori
                elif jumlah == maks:
                    text += ", " + kategori
            st.header(text)

