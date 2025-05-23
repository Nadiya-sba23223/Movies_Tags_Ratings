import streamlit as st
import pandas as pd
import numpy as np

# 🎨 Add custom CSS for style and background
st.markdown("""
    <style>
        body {
            background-color: #f4f8fb;
        }
        .stApp {
            background-image: linear-gradient(to bottom right, #ffffff, #e8f1f9);
        }
    </style>
""", unsafe_allow_html=True)

# 🎯 Centered, stylish title
st.markdown("""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        <h1 style='color: #2E86C1; font-size: 40px;'>🎯 Smart Movie Discovery for Curious Minds</h1>
    </div>
""", unsafe_allow_html=True)


# Load your preprocessed data
rating_sample = pd.read_csv("rating_sample.csv") 
all_tags = pd.read_csv("tags.csv", encoding='ISO-8859-1') 

# Preprocess tags
tag_set = sorted(set(all_tags['tag'].dropna().str.lower().unique()))

# UI
st.title("🔖 Discover Movies by Tag")
selected_tag = st.selectbox("Start typing a tag (e.g. time travel, based on a book)", tag_set)
sort_option = st.radio("Sort results by:", ["Average Rating", "Popularity"])

# Filter and summarize
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

    st.markdown(f"### 🎬 Top Movies Tagged With: `{selected_tag}`")
    st.dataframe(summary.head(10), use_container_width=True)
else:
    st.info("Start typing a tag to explore movie recommendations.")
