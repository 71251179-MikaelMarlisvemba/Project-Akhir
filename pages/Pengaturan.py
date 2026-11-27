import io
import streamlit as st
import json 
import xlsxwriter as xlsx 
from db import supabase

st.title("Pengaturan")

with st.container(border=True):
    st.subheader("Ganti Password")
    password_lama = st.text_input("Password lama", type="password", placeholder="Masukkan password lama")
    password_baru = st.text_input("Password baru", type="password", placeholder="Masukkan password baru")
    konfirmasi_password_baru = st.text_input("Konfirmasi password baru", type="password", placeholder="Ulangi password baru")
    submit = st.button("Ganti Password",type='primary', width="stretch")

if submit:
    username = st.session_state.get("username")
    if not password_lama or not password_baru or not konfirmasi_password_baru:
        st.error("Mohon untuk mengisi semua field 😊")
    elif password_baru != konfirmasi_password_baru:
        st.error("Konfirmasi Password Baru tidak sesuai dengan Password Baru")
    elif not username:
        st.error("Username tidak ditemukan.")
    else:
        response = (
            supabase.table("User").select("*").eq("username", username).eq("password", password_lama).execute()
        )
        if response.data:
            supabase.table("User").update({"password": password_baru}).eq("username", username).execute()
            st.success("Password berhasil diganti!")
        else:
            st.error("Password lama tidak sesuai.")

with st.container(border=True):
    st.subheader("Export Data")
    st.write("Unduh koleksi manhwa Anda")
    col1, col2 = st.columns([1, 1])
    with col1:

        file_json= supabase.table("bookmark_user").select("*").eq("id_user", st.session_state["id_user"]).execute()
        data_json = file_json.data
        json_data = json.dumps(data_json, indent=4)
        st.download_button(
            label="Export JSON",
            data=json_data,
            file_name="backup_manhwa.json",
            mime="application/json",
            use_container_width=True
        )
    with col2:
        output = io.BytesIO()
        workbook = xlsx.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Backup Manhwa")
        headers = ["id_user", "id_manhwa", "judul_manhwa", "cover", "genre", "status", "chapter_terakhir"]
        for kolom, header in enumerate(headers):
            worksheet.write(0, kolom, header)
        for baris, data in enumerate(data_json, start=1):
            for kolom, header in enumerate(headers):
                worksheet.write(baris, kolom, data.get(header))
        workbook.close()
        output.seek(0)
        st.download_button(
            label="Export Excel",
            data=output,
            file_name="backup_manhwa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

with st.container(border=True):
    st.subheader("Import Data")
    st.write("Pilih file backup (.json), maks 200 MB")
    file_upload = st.file_uploader("Upload", type=["json"], accept_multiple_files=False, label_visibility="collapsed")
    
    if file_upload is not None:
        try:
            data = json.load(file_upload)
        except Exception:
            st.error("File bukan JSON yang valid.")
            data = None

        if data is not None:
            res = supabase.table("bookmark_user").select("id_manhwa").eq("id_user", st.session_state["id_user"]).execute()
            existing_ids = [row["id_manhwa"] for row in res.data]
    
            for item in data:
                if isinstance(item, dict) and item.get("id_manhwa") not in existing_ids:
                    item["id_user"] = st.session_state["id_user"]
                    supabase.table("bookmark_user").insert(item).execute()
            st.success("Data berhasil diimpor!")
    else:
        st.caption("Belum ada file yang diunggah")

if st.button("Log Out", type="primary", width="stretch"):
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["id_user"] = None
    st.session_state["riwayat_edit"] = []
    st.rerun()

        