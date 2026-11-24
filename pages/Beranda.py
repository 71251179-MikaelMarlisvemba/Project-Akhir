import streamlit as st
from db import supabase 

st.title(f"Beranda - Koleksi {st.session_state["username"]}")
opsi_status = ["Semua","Belum Dibaca", "Sedang Dibaca", "Selesai Dibaca"]
opsi_sort = ["A-Z", "Z-A", "Terlama", "Terbaru"]

data_manhwa = supabase.table("bookmark_user").select("*").eq("id_user",st.session_state["id_user"]).execute()

x1,x2 = st.columns([1,1])
with x1:
    status=st.selectbox("Filter Status", options=opsi_status)
with x2:
    urutan =st.selectbox("Sort by:", options=opsi_sort)

cols = st.columns(3)

for i, manhwa in enumerate(data_manhwa.data):
    with cols[i % 3]:
        with st.container(border=True, height="stretch"):
            st.image(manhwa["cover"],width="stretch")
            st.subheader(manhwa["judul_manhwa"])
            st.caption(manhwa["genre"])
            st.caption(f"Status: {manhwa["status"]}")
            col1,col2 = st.columns([1,1])
            with col1 :
                if st.button("Edit Status", key=f"Edit{manhwa["id_manhwa"]}",width="stretch"):
                    st.session_state["id_edit"] = manhwa["id_manhwa"]
                    st.switch_page("editStatus.py")
            with col2 :
                if st.button("Hapus", key=f"hapus{manhwa["id_manhwa"]}",width="stretch",type="primary"):
                    supabase.table("bookmark_user").delete().eq("id_manhwa",manhwa["id_manhwa"]).execute()
                    st.rerun()