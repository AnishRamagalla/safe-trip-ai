import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from models.recommendation_engine import recommend_safe_countries
from analysis.data_cleaning import clean_threat_data

st.set_page_config(page_title="safeTrip AI", layout="wide")
st.title("SafeTrip AI - Your Real-Time Travel Safety Advisor")

user_input = st.text_input("Where are you planning to travel?")
df = clean_threat_data("data/us_travel_advisories.csv")

if user_input:
    recommendeed = recommend_safe_countries(user_input,df)
    st.subheader(" Safer Alternatives: ")
    st.dataframe(recommended)

st.subheader("Global Threat Levels")
st.bar_chart(df.sort_values("threat_numeric")[:10].set_index("country")["threat_numeric"])
