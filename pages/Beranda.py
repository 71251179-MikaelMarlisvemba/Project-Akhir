import streamlit as st
from db import supabase 
import math
from rekomendasi import rekomendasi

st.title(f"Beranda - Koleksi {st.session_state["username"]}")

if "sukses" in st.session_state and st.session_state["sukses"] is not None:
    st.success(st.session_state.pop("sukses"))

opsi_status = ["Semua","Belum Dibaca", "Sedang Dibaca", "Selesai Dibaca"]
opsi_sort = ["Terbaru", "Terlama", "A-Z", "Z-A"]

data_manhwa = supabase.table("bookmark_user").select("*").eq("id_user",st.session_state["id_user"]).execute()

if "beranda_now" not in st.session_state:
    st.session_state["beranda_now"] = 1
if "id_edit" not in st.session_state:
    st.session_state["id_edit"] = {}
if "riwayat_edit" not in st.session_state:
    st.session_state["riwayat_edit"] = []
if "rekomendasi" not in st.session_state:
    st.session_state["rekomendasi"] = ""

def ke_sebelumnya():
    st.session_state["beranda_now"] -= 1

def ke_selanjutnya():
    st.session_state["beranda_now"] += 1

def reset_halaman():
    st.session_state["beranda_now"] = 1

def quick_sort_nama(data):
    if len(data)<=1:
        return data

    pivot = data[-1]
    kiri = []
    kanan = []

    for manhwa in data[:-1]:
        if manhwa["judul_manhwa"].lower() < pivot["judul_manhwa"].lower():
            kiri.append(manhwa)
        else:
            kanan.append(manhwa)

    return (quick_sort_nama(kiri) + [pivot] + quick_sort_nama(kanan))
  
def quick_sort_waktu(data):
    if len(data)<=1:
        return data

    pivot = data[-1]
    kiri = []
    kanan = []
    for manhwa in data[:-1]:
        if manhwa["waktu_ditambahkan"] < pivot["waktu_ditambahkan"]:
            kiri.append(manhwa)
        else:
            kanan.append(manhwa)

    return (quick_sort_waktu(kiri) + [pivot] + quick_sort_waktu(kanan))

def urut_status(data, status):
    temp = []
    for manhwa in data:
        if manhwa["status"] == status:
            temp.append(manhwa)
    return temp

x1,x2 = st.columns([1,1])
with x1:
    status=st.selectbox("Filter Status", options=opsi_status, on_change=reset_halaman)
with x2:
    urutan =st.selectbox("Urutkan", options=opsi_sort, on_change=reset_halaman)
st.divider()

data_urut = data_manhwa.data

if data_urut == []:
    st.error("**Belum ada manhwa yang di bookmark!**")

if urutan == "A-Z":
    data_urut = quick_sort_nama(data_manhwa.data)
elif urutan == "Z-A":
    data_urut = quick_sort_nama(data_manhwa.data)[::-1]
elif urutan == "Terlama":
    data_urut = quick_sort_waktu(data_manhwa.data)
elif urutan == "Terbaru":
    data_urut = quick_sort_waktu(data_manhwa.data)[::-1]

if status == "Semua":
    data_filter = data_urut
elif status == "Belum Dibaca":
    data_filter = urut_status(data_urut,"Belum Dibaca")
elif status == "Sedang Dibaca":
    data_filter= urut_status(data_urut,"Sedang Dibaca")
elif status == "Selesai Dibaca":
    data_filter = urut_status(data_urut,"Selesai Dibaca")

if data_filter == [] and data_urut != []:
    st.warning(f"**Belum ada manhwa yang di bookmark dengan status {status}**")

total_manhwa_perhalaman = 3
total_halaman = max(1, math.ceil(len(data_filter)/total_manhwa_perhalaman))
st.session_state["beranda_now"] = min(st.session_state["beranda_now"], total_halaman) # antisipasi delete

awal = (st.session_state["beranda_now"] - 1) * total_manhwa_perhalaman
data_halaman = data_filter[awal : awal + total_manhwa_perhalaman]

kolom = st.columns(3)
for i, manhwa in enumerate(data_halaman):
    with kolom[i % 3]:
        with st.container(border=True, height="stretch"):
            st.image(manhwa["cover"],width="stretch")
            st.subheader(manhwa["judul_manhwa"])
            st.caption(manhwa["genre"])
            st.caption(f"Status: {manhwa["status"]}")
            if manhwa["chapter_terakhir"] != 0 and manhwa["chapter_terakhir"]  != None:
                st.caption(f"Chapter terahkir: {manhwa["chapter_terakhir"]}")
            col1,col2 = st.columns([1,1])
            with col1 :
                if st.button("Edit Status", key=f"edit_{manhwa['id_manhwa']}_{i}",width="stretch"):
                    st.session_state["id_edit"] = manhwa
                    st.session_state["edit"] = True
                    st.rerun()
            with col2 :
                if st.button("Hapus", key=f"hapus_{manhwa["id_manhwa"]}_{i}",width="stretch",type="primary"):
                    supabase.table("bookmark_user").delete().eq("id_manhwa",manhwa["id_manhwa"]).execute()
                    st.rerun()

isi_riwayat = st.session_state["riwayat_edit"]
if data_halaman == []:
    isi_riwayat.clear()

if data_halaman != []:
    x1,x2,x3 = st.columns(3)
    with x1:
        st.button("Sebelumnya", disabled=st.session_state["beranda_now"] <= 1,on_click=ke_sebelumnya, width="stretch")

    with x2:
        st.button(f"**Halaman {st.session_state['beranda_now']}**", disabled=True, width="stretch", type="tertiary")

    with x3:
        st.button("Selanjutnya", disabled=st.session_state["beranda_now"] >= total_halaman, on_click=ke_selanjutnya, width="stretch")

    st.divider()

    if st.session_state["riwayat_edit"] != []:
        tampil = []
        st.subheader("**Riwayat Edit**")
        st.caption("Perubahan status atau chapter terakhir")
        if len(isi_riwayat) == 6:
            isi_riwayat.pop(0)
        for i in isi_riwayat:
            temp = {}
            temp["Manhwa"] = i["Manhwa"]
            temp['Sebelum']= None
            temp["Sesudah"]= None
            if i["Sebelum_status"] == i["Sesudah_status"]:
                temp["Sebelum"]= f"Sedang Dibaca, Chapter {i["Chapter_sebelum"]}"
                temp["Sesudah"]= f"Sedang Dibaca, Chapter {i["Chapter_sesudah"]}"
            elif i["Sebelum_status"] == "Sedang Dibaca":
                temp["Sebelum"]= f"Sedang Dibaca, Chapter {i["Chapter_sebelum"]}"
                temp["Sesudah"]= i["Sesudah_status"]
            elif i["Sesudah_status"] == "Sedang Dibaca":
                temp["Sebelum"]= i["Sebelum_status"]
                temp["Sesudah"]= f"Sedang Dibaca, Chapter {i["Chapter_sesudah"]}"
            else:
                temp["Sebelum"] = i["Sebelum_status"]
                temp["Sesudah"] = i["Sesudah_status"]
    
            tampil.append(temp)

        st.dataframe(tampil)
        st.divider()

    st.subheader("**Rekomendasi Manhwa**")
    st.caption("AI akan merekomendasikan 5 judul berdasarkan manhwa di bookmark Anda")
    if st.button("Rekomendasikan 5 Manhwa", type="primary", width="stretch"):
        st.session_state["rekomendasi"] = rekomendasi(data_halaman)
        
        with st.container(border=True):
            st.write(st.session_state["rekomendasi"])