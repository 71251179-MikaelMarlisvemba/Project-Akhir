import streamlit as st
from db import supabase
import pandas as pd
import matplotlib.pyplot as plt

manhwa = supabase.table("bookmark_user").select("*").eq("id_user", st.session_state["id_user"]).execute()
data = manhwa.data

st.title("Statistik")

if len(data) != 0:
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

    jenis_status = ["Belum Dibaca", "Sedang Dibaca", "Selesai Dibaca"]
    jumlah_status = []
    for jumlah in jenis_status:
        jumlah_status.append(status.get(jumlah,0))

    jenis_genre = []
    jumlah_genre = []
    for key, value in genre.items():
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
                if "Selesai Dibaca" in status:
                    st.header(status["Selesai Dibaca"])
                else:
                    st.header("0")

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
            with st.container(border=True, height='stretch'):    
                st.subheader("Jumlah per Status",text_alignment='center')
                fig1, ax1 = plt.subplots()
                ax1.bar(jenis_status, jumlah_status)
                ax1.set_xlabel("Jenis Kategori")
                ax1.set_ylabel("Jumlah Kategori")
                st.pyplot(fig1)

        with x2:
            with st.container(border=True, height='stretch'):    
                st.subheader("Proporsi Genre",text_alignment='center')
                fig2, ax2 = plt.subplots()
                ax2.pie(jumlah_genre, labels=jenis_genre, autopct="%1.1f%%")
                st.pyplot(fig2)

else:
    st.warning("Belum ada statistik!")