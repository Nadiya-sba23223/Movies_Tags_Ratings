import streamlit as st
import pandas as pd
import numpy as np
import plotly

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

# 📁 Load data
rating_sample = pd.read_csv("rating_sample.csv")
tags = pd.read_csv("tags.csv", encoding='ISO-8859-1')
movies = pd.read_csv("movies.csv", encoding='ISO-8859-1')

# 🧹 Preprocess
tags['tag'] = tags['tag'].str.lower().fillna('')
tag_options = sorted(set(tags['tag']))
movies['genres'] = movies['genres'].fillna('')

# Extract unique genres
unique_genres = sorted(set(
    g for genre_list in movies['genres'] for g in genre_list.split('|') if g != '(no genres listed)'
))

# 🔧 Sidebar Filters
with st.sidebar:
    st.header("🔎 Filter Your Discovery")
    selected_tag = st.selectbox("Search by Tag", tag_options)
    selected_genres = st.multiselect("Filter by Genre(s)", unique_genres)
    sort_by = st.radio("Sort by:", ["Average Rating", "Popularity"])

# 🔍 Filter ratings by tag
filtered = rating_sample[rating_sample['tag'].str.lower().str.contains(selected_tag, na=False)]
filtered = filtered.merge(movies, on="movieId")

# 🎭 Apply genre filter
if selected_genres:
    filtered = filtered[filtered['genres'].apply(lambda x: any(g in x for g in selected_genres))]

# 📊 Grouped summary
summary = filtered.groupby(['movieId', 'title', 'genres']).agg(
    Average_Rating=('rating', 'mean'),
    Number_of_Ratings=('rating', 'count')
).reset_index()

# 🧮 Sort
if sort_by == "Average Rating":
    summary = summary.sort_values("Average_Rating", ascending=False)
else:
    summary = summary.sort_values("Number_of_Ratings", ascending=False)

# 📊 Chart toggle
if not summary.empty:
    st.markdown(f"### 🍿 Top Movies Tagged With: `{selected_tag}`")
    if selected_genres:
        st.markdown(f"🎭 Genres: {', '.join(selected_genres)}")

    chart_type = st.radio("📈 Choose Chart Type", ["Average Rating", "Number of Ratings"])
    chart_data = summary.head(10)

    if chart_type == "Average Rating":
        fig = px.bar(chart_data, x="title", y="Average_Rating",
                     title="⭐ Top Rated Movies",
                     labels={"title": "Movie", "Average_Rating": "Avg Rating"},
                     color="Average_Rating", color_continuous_scale="Blues")
    else:
        fig = px.bar(chart_data, x="title", y="Number_of_Ratings",
                     title="🔥 Most Popular Movies",
                     labels={"title": "Movie", "Number_of_Ratings": "Ratings"},
                     color="Number_of_Ratings", color_continuous_scale="Oranges")

    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # 📋 Table output
    styled = chart_data.style.background_gradient(cmap='coolwarm')\
        .format({"Average_Rating": "{:.2f}", "Number_of_Ratings": "{:,.0f}"})
    st.dataframe(styled, use_container_width=True)
else:
    st.info("No movies match your filters. Try a different tag or genre.")