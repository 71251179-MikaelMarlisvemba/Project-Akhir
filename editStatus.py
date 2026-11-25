import streamlit as st
from db import supabase

st.title("Edit Status")

opsi = ["Belum Dibaca", "Sedang Dibaca", "Selesai Dibaca"]

if "error" not in st.session_state:
    st.session_state["error"] = None
if "sukses" not in st.session_state:
    st.session_state["sukses"] = ""

data = st.session_state["id_edit"]

_, mid, _ = st.columns(3)

with mid:
    with st.container(border=True ):
        st.image(data["cover"], width="stretch")
        st.subheader(data["judul_manhwa"])
        st.caption(data["genre"])

status = st.selectbox("Status",options=opsi, index=opsi.index(data["status"]), width="stretch")

chapter = None
if status == "Sedang Dibaca":
    chapter = st.number_input(label="Chapter terakhir dibaca", min_value=1)

x1,x2 = st.columns(2)
with x1:
    if st.button("Simpan", width="stretch", type="primary"):
        if data["status"] == "Sedang Dibaca" and data["chapter_terakhir"] == chapter:
            st.session_state["error"] = ("Chapter tidak boleh sama")
        elif data["status"] == status and data["status"] != "Sedang Dibaca":
            st.session_state["error"] = ("Pilih status yang lain")
        else:
            temp = {}
            temp["Manhwa"] = data["judul_manhwa"]
            temp["Sebelum"] = data["status"]
            temp["Chapter_sebelum"] = data["chapter_terahkir"] 
            temp["Sesudah"] = status
            temp["Chapter_sesudah"] = chapter
            (supabase.table("bookmark_user").update({"status": status, "chapter_terakhir": chapter}).eq("id_manhwa",data["id_manhwa"]).execute())
            st.session_state["sukses"] = (f"Pergantian Status Manhwa {data["judul_manhwa"]} Berhasil!")
            st.session_state["edit"] = False
            st.rerun()
        
with x2:
    if st.button("Batal",width="stretch", type="secondary"):
        st.session_state["edit"] = False
        st.rerun()

if st.session_state["error"]:
    st.error(st.session_state.pop("error"))