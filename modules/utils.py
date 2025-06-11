import pandas as pd
import streamlit as st
from crewai import LLM

@st.cache_data
def load_data():
    return pd.read_csv('data/Superstore.csv', encoding='windows-1252')

def load_llm(model_name="gemini/gemini-2.0-flash"):
    return LLM(
        model=model_name,
        temperature=0.7,
        api_key=st.secrets['GEMINI_API_KEY']
    )