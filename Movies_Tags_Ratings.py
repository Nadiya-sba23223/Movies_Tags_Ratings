import streamlit as st
import pandas as pd
import numpy as np

st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🎯 Smart Movie Discovery for Curious Minds</h1>", unsafe_allow_html=True)

rating_sample = pd.read_csv("rating_sample.csv")
tags = pd.read_csv("tags.csv", encoding='ISO-8859-1')
movies = pd.read_csv("movies.csv", encoding='ISO-8859-1')

# Preprocess
tags['tag'] = tags['tag'].str.lower().fillna('')
tag_options = sorted(set(tags['tag']))
movies['genres'] = movies['genres'].fillna('')

# Genre filter: extract all unique genres
unique_genres = sorted(set(g for genre_list in movies['genres'] for g in genre_list.split('|') if g != '(no genres listed)'))

# Sidebar for filters
with st.sidebar:
    st.header("🔎 Filter Your Discovery")
    selected_tag = st.selectbox("Search by Tag", tag_options)
    selected_genres = st.multiselect("Filter by Genre(s)", unique_genres)
    sort_by = st.radio("Sort by:", ["Average Rating", "Popularity"])

# Filter ratings by tag match
filtered = rating_sample[rating_sample['tag'].str.lower().str.contains(selected_tag, na=False)]

# Merge with movie metadata
filtered = filtered.merge(movies, on="movieId")

# Apply genre filter
if selected_genres:
    filtered = filtered[filtered['genres'].apply(lambda x: any(g in x for g in selected_genres))]

# Aggregate summary
summary = filtered.groupby(['movieId', 'title', 'genres']).agg(
    Average_Rating=('rating', 'mean'),
    Number_of_Ratings=('rating', 'count')
).reset_index()

# Sort
if sort_by == "Average Rating":
    summary = summary.sort_values("Average_Rating", ascending=False)
else:
    summary = summary.sort_values("Number_of_Ratings", ascending=False)

# Display Results
st.markdown(f"### 🎬 Top Movies Tagged With: `{selected_tag}`")
if selected_genres:
    st.markdown(f"🎭 Genres: {', '.join(selected_genres)}")

if summary.empty:
    st.warning("No movies found with these filters.")
else:
    st.dataframe(
        summary.head(10).style.background_gradient(cmap='Blues'),
        use_container_width=True
    )