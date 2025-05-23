import streamlit as st
import pandas as pd
import numpy as np

# 🎨 Add custom CSS for style and background
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }
        .stApp {
            background-image: linear-gradient(to bottom right, #ffffff, #e0f7fa);
        }
        h1 {
            color: #5E60CE;
        }
        .stRadio > div {
            background-color: #f0f8ff;
            border-radius: 8px;
            padding: 10px;
        }
        thead tr th {
            background-color: #2E86C1;
            color: white;
            font-size: 16px;
            text-align: center;
        }
        tbody tr td {
            text-align: center;
            font-size: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# 🎯 Centered title
st.markdown("""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        <h1 style='color: #2E86C1; font-size: 40px;'>🎯 Smart Movie Discovery for Curious Minds</h1>
    </div>
""", unsafe_allow_html=True)

# 📁 Load data
rating_sample = pd.read_csv("rating_sample.csv") 
all_tags = pd.read_csv("tags.csv", encoding='ISO-8859-1') 

# 🧹 Clean tag list
tag_set = sorted(set(all_tags['tag'].dropna().str.lower().unique()))

# 🧭 Tag UI
selected_tag = st.selectbox("Start typing a tag (e.g. time travel, based on a book)", tag_set)
sort_option = st.radio("Sort results by:", ["Average Rating", "Popularity"])

# 📊 Filter logic
if selected_tag:
    filtered = rating_sample[rating_sample['tag'].str.lower().str.contains(selected_tag, na=False)]

    summary = filtered.groupby(['movieId', 'title', 'genres']).agg(
        Average_Rating=('rating', 'mean'),
        Number_of_Ratings=('rating', 'count')
    ).reset_index()

    if sort_option == "Average Rating":
        summary = summary.sort_values(by="Average_Rating", ascending=False)
    else:
        summary = summary.sort_values(by="Number_of_Ratings", ascending=False)

    # 🎨 Rename for display
    summary_display = summary.rename(columns={
        "title": "🎬 Movie Title",
        "genres": "🎭 Genre",
        "Average_Rating": "⭐ Rating",
        "Number_of_Ratings": "👥 Number of Votes"
    })

    # 📋 Results header
    st.markdown(f"### 🎬 Top Movies Tagged With: `{selected_tag}`")

    # 🖥️ Display results
    st.dataframe(summary_display.head(10), use_container_width=True)

else:
    st.info("Start typing a tag to explore movie recommendations.")