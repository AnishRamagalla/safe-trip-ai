import streamlit as st
import pandas as pd
import os
import sys

# Fix for Streamlit Cloud path issues
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import recommendation and data cleaning modules
from models.recommendation_engine import recommend_safe_countries
from analysis.data_cleaning import clean_threat_data

# Configure Streamlit page
st.set_page_config(page_title="SafeTrip AI", layout="wide")
st.title("🌍 SafeTrip AI - Your Real-Time Travel Safety Advisor")

# Load and clean the advisory data
DATA_PATH = "data/us_travel_advisories.csv"
df = None
try:
    df = clean_threat_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"❌ Data file not found at: {DATA_PATH}")
    st.stop()
except Exception as e:
    st.error(f"❌ Failed to load data: {str(e)}")
    st.stop()

# Input from user
user_input = st.text_input("Where are you planning to travel?")

# Recommendation logic with safety checks
if user_input and df is not None:
    try:
        recommended = recommend_safe_countries(user_input, df)
        if recommended is not None and not recommended.empty:
            st.subheader("🔒 Safer Alternatives:")
            st.dataframe(recommended)
        else:
            st.warning("No matching safe destinations found. Try a different country.")
    except Exception as e:
        st.error(f"⚠️ Error in recommendation engine: {str(e)}")

# Safe travel chart
if df is not None:
    st.subheader("📊 Top 10 Safest Countries")
    try:
        safest = df.sort_values("threat_numeric").head(10)
        st.bar_chart(safest.set_index("country")["threat_numeric"])
    except Exception as e:
        st.warning(f"Could not display chart: {str(e)}")
