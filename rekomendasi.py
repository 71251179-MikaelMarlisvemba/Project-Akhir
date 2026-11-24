from google import genai
import streamlit as st

def rekomendasi(data):
    key = st.secrets["supabase"]["GEMINI_API_KEY"]

    client = genai.Client(api_key=key)
        
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=f"Berdasarkan variabel {data} berikan rekomendasi 5 manhwa yang serupa yang tersedia di website https://anilist.co/. Format : Rekomendasi untuk Anda : 1. Judul saja tanpa penjelasan"
    )
    
    if interaction:
        return interaction.output_text
    else: 
        return st.error("Gagal, coba lagi nanti!")