import streamlit as st
from db import supabase
import pandas as pd
import matplotlib.pyplot as plt

manhwa = supabase.table("bookmark_user").select("*").eq("id_user", st.session_state["id_user"]).execute()
data = manhwa.data

st.title("Statistik")

genre = {}
status = {}
for i in data:
    if i["status"] not in status:
        status[i["status"]] = 1
    else:
        status[i["status"]] += 1
    bersih = i["genre"].split(", ")
    for j in bersih:
        if j not in genre:
            genre[j] = 1
        else:
            genre[j] += 1

jenis_genre = []
jumlah_genre = []
for key, value in genre.values():
    jenis_genre.append(key)
    jumlah_genre.append(value)

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
            st.header(status["Selesai Dibaca"])

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

with st.container(width="stretch", height="stretch"):    
    x1,x2 = st.columns(2)
    with x1:
        fig1, ax1 = plt.subplot()
        ax1.bar(jenis_genre, jumlah_genre)
        ax1.set_x

    with x2:
        pass