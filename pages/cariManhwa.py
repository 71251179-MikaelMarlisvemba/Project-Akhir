import streamlit as st
from db import supabase
from manhwa import cari_manhwa
from datetime import datetime
from zoneinfo import ZoneInfo

st.header("Cari Manhwa")

if "cari_manhwa" not in st.session_state:
    st.session_state.hasil_manhwa = []
    st.session_state.page_cari = 1
    st.session_state.cari = False
    
cari = st.text_input("**Cari**", key="cari_manhwa",placeholder="Masukkan nama manhwa").strip()

genres = [
    "Semua",
    "Action",
    "Adventure",
    "Comedy",
    "Drama",
    "Fantasy",
    "Romance",
    "Horror",
    "Mystery",
    "Psychological",
    "Slice of Life",
    "Sports",
    "Supernatural",
    "Thriller"
]


user = (supabase.table("User").select("id_user").eq("username", st.session_state["username"]).execute())

id_user = user.data[0]["id_user"]

data_user = (supabase.table("bookmark_user").select("judul_manhwa").eq("id_user", id_user).execute())
data_manhwa = [item["judul_manhwa"] for item in data_user.data]

genre = st.selectbox("**Filter Kategori**", options=genres)

def muat_manhwa():
    data = cari_manhwa(
            search=st.session_state.manhwa,
            genre=st.session_state.genre,
        )
    
    st.session_state.hasil_manhwa = data
    
if st.button("**Cari**", type='primary', use_container_width=True):
    st.session_state.manhwa = cari
    st.session_state.genre = genre
    st.session_state.page_cari = 1
    st.session_state.cari = True
    muat_manhwa()
    
perHalaman = 3
hasilCari = st.session_state.hasil_manhwa
mulai = (st.session_state.page_cari - 1) * perHalaman
hasil = hasilCari[mulai:mulai + perHalaman]
selanjutnya = mulai + perHalaman < len(hasilCari)

    
if len(hasil) == 0:
    if st.session_state.cari:
        st.subheader("Hasil Pencarian")
        st.error("Manhwa tidak ada/tidak tersedia.")
            
else:
    if st.session_state.cari:
        st.subheader("Hasil Pencarian")
        cols = st.columns(3)
        
        for index, manga in enumerate(hasil):
            with cols[index % 3]:
                with st.container(border=True, height="stretch"):
                    cover = manga["coverImage"]["large"]
                    
                    st.image(cover, use_container_width=True)
                    judul = (manga["title"]["english"] or manga["title"]["romaji"])
                    
                    st.markdown(f"**{judul}**")
                    
                    st.caption(f"Jumlah Chapter : {manga["chapters"] or "Belum ada chapter (Ongoing)"}")
                    
                    st.caption(", ".join(manga["genres"]))
                    
                    waktu = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat()
                    
                    if judul in data_manhwa:
                        st.button("Tersimpan", disabled=True, use_container_width=True, key=f"tersimpan_{manga["id"]}")
                    
                    else:
                        if st.button("Bookmark", key=f"library_{manga["id"]}", use_container_width=True):
                            tambah = {
                                "id_user": id_user,
                                "judul_manhwa" : judul,
                                "jumlah_chapter" : manga["chapters"],
                                "genre" : ", ".join(manga["genres"]),
                                "chapter_terakhir" : None,
                                "status" : "Belum Dibaca",
                                "waktu_ditambahkan" : waktu,
                                "cover" : cover
                            }
                            
                            tambah_manhwa = (supabase.table("bookmark_user").insert(tambah)).execute()
                            
                            if len(tambah_manhwa.data) == 0:
                                st.warning("Gagal menambahkan manhwa")
                            else:
                                st.rerun()
                                
        if len(hasil) != 0:

            col1, col2, col3 = st.columns(3)
            if col1.button("Sebelumnya", disabled=st.session_state.page_cari == 1, use_container_width=True):
                st.session_state.page_cari -= 1
                muat_manhwa()
                st.rerun()
                
            col2.button(f"**Halaman {st.session_state.page_cari}**", use_container_width=True, type="tertiary", disabled=True)
                        
            if col3.button("Selanjutnya", disabled=not selanjutnya, use_container_width=True):
                st.session_state.page_cari += 1
                muat_manhwa()
                st.rerun()
