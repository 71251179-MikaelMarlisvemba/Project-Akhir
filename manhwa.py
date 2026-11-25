import requests
import streamlit as st 

url = "https://graphql.anilist.co"

query = """
query(
    $search: String,
    $genre: String,
    $page: Int
) {
    Page(page: $page, perPage: 50) {  
        media(
            search: $search,
            genre: $genre,
            type: MANGA,
            countryOfOrigin: KR,
            sort: [POPULARITY_DESC],
            isAdult: false
        ) {
            id
            
            title {
                romaji
                english
            }
            coverImage {
                large
            }
            
            genres
            description(asHtml: false)
            status
            chapters
            averageScore
        }
    }
}"""
        
@st.cache_data(ttl=600)
def cari_manhwa(search="", genre="Semua", page=1):
    
    variables = {
        "search": search or None,
        "genre": genre if genre != "Semua" else None,
        "page": page
    }
    
    response = requests.post(
        url,
        json= {
            "query": query,
            "variables": variables
        }, 
        headers= {
            "Content-Type": "application/json",
            "Accept":"application/json"
        },
        timeout=20
    )
    
    response.raise_for_status()
    
    result = response.json()
    
    if "errors" in result:
        raise ValueError(result["errors"])
    
    return result["data"]["Page"]["media"]
    
    