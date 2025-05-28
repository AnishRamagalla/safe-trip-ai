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
from scraping.news_scraper import get_us_travel_advisories

# Try to load existing data, or scrape live if not found
DATA_PATH = "data/us_travel_advisories.csv"
df = None

try:
    if os.path.exists(DATA_PATH):
        df = clean_threat_data(DATA_PATH)
    else:
        df = get_us_travel_advisories()
        os.makedirs("data", exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
except Exception as e:
    st.error(f"❌ Failed to load or scrape data: {str(e)}")
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
