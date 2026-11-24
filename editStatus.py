import streamlit as st
from db import supabase

st.title("Edit Status")

opsi = ["Belum Dibaca", "Sedang Dibaca", "Selesai Dibaca"]

if "error" not in st.session_state:
    st.session_state["error"] = False

manhwa = supabase.table("bookmark_user").select("*").eq("id_user", st.session_state["id_user"]).eq("id_manhwa",st.session_state["id_edit"]).execute()
data = manhwa.data[0]

_, mid, _ = st.columns(3)

with mid:
    with st.container(border=True, ):
        st.image(data["cover"], width="stretch")
        st.subheader(data["judul_manhwa"])
        st.caption(data["genre"])

status = st.selectbox("Status",options=opsi, width="stretch")

if status == "Sedang Dibaca":
    chapter = st.number_input(label="Chapter terahkir dibaca", min_value=1)

x1,x2 = st.columns(2)
with x1:
    if st.button("Simpan", width="stretch", type="primary"):
        if data["status"] == "Sedang Dibaca" and data["chapter_terahkir"] == chapter:
            st.session_state["error"] = ("Chapter tidak boleh sama")
        elif data["status"] == status:
            st.session_state["error"] = ("Pilih status yang lain")
        elif status == "Sudah Dibaca":
            data["chapter_terahir"] = False
            data["status"] = "Sudah Dibaca"
        elif status == "Belum Dibaca":
            data["chapter_terahir"] = False
            data["status"] = "Belum Dibaca"
        elif status == "Sedang Dibaca":
            data["chapter_terahir"] = chapter
            data["status"] = "Sedang Dibaca"
        # st.session_state["id_edit"] = False

with x2:
    if st.button("Batal",width="stretch", type="secondary"):
        st.session_state["edit"] = False
        st.session_state["id_edit"] = False
        st.switch_page["pages/beranda/py"]

if "error" in st.session_state:
    st.error(st.session_state["error"])