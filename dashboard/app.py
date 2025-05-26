import streamlit as st
import pandas as pd
import os
import sys

# Fix for Streamlit Cloud: add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.recommendation_engine import recommend_safe_countries
from analysis.data_cleaning import clean_threat_data

# Set Streamlit page configuration
st.set_page_config(page_title="SafeTrip AI", layout="wide")
st.title("🌍 SafeTrip AI - Your Real-Time Travel Safety Advisor")

# Load data
DATA_PATH = "data/us_travel_advisories.csv"

try:
    df = clean_threat_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"❌ Data file not found at: {DATA_PATH}")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

# Get user input
user_input = st.text_input("Where are you planning to travel?")

# Recommend safer alternatives
if user_input:
    try:
        recommended = recommend_safe_countries(user_input, df)
        if not recommended.empty:
            st.subheader("🔒 Safer Alternatives:")
            st.dataframe(recommended)
        else:
            st.warning("No similar countries found. Try another name.")
    except Exception as e:
        st.error(f"⚠️ Recommendation system failed: {str(e)}")

# Bar chart of safest destinations
st.subheader("📊 Top 10 Safest Countries (by Threat Level)")
try:
    safest = df.sort_values("threat_numeric").head(10)
    st.bar_chart(safest.set_index("country")["threat_numeric"])
except Exception as e:
    st.warning(f"Could not display chart: {str(e)}")
