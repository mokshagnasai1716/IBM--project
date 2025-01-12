import streamlit as st

def get_api_key():
    api_key = st.secrets["GEMINI_API_KEY"]

    if api_key is None:
        raise ValueError("API key not found. Please set GEMINI_API_KEY in secrets.toml.")
    
    return api_key

# Retrieve and print the API key
api_key = get_api_key()
print(api_key)
