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
    </style>
""", unsafe_allow_html=True)

# 🎯 Centered, modern title
st.markdown("""
    <div style='text-align: center; padding: 15px 0;'>
        <h1>🎯 Smart Movie Discovery for Curious Minds</h1>
        <h4 style='color: #4A4E69;'>A sleek interface tailored for the 18–35 audience</h4>
    </div>
""", unsafe_allow_html=True)

# 📁 Load data
rating_sample = pd.read_csv("rating_sample.csv") 
all_tags = pd.read_csv("tags.csv", encoding='ISO-8859-1') 

# 🧹 Clean tag list
tag_set = sorted(set(all_tags['tag'].dropna().str.lower().unique()))

# 🧭 Tag UI
st.header("🔖 Discover Movies by Tag")
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

    # 📋 Results header
    st.markdown(f"### 🎬 Top Movies Tagged With: `{selected_tag}`")

    # ✨ Format table nicely
    styled_summary = summary.head(10).style.format({
        "Average_Rating": "{:.2f}",
        "Number_of_Ratings": "{:,}"
    }).background_gradient(cmap='PuBu')

    st.dataframe(styled_summary, use_container_width=True)

else:
    st.info("Start typing a tag to explore movie recommendations.")