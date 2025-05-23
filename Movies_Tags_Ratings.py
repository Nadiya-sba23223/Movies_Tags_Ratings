import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 🎨 Page styling
st.set_page_config(page_title="Smart Movie Discovery", layout="wide")

# 💾 Load data
rating_sample = pd.read_csv("rating_sample.csv")
tags = pd.read_csv("tags.csv", encoding='ISO-8859-1')
movies = pd.read_csv("movies.csv", encoding='ISO-8859-1')

# 🧹 Clean tags and genres
tags['tag'] = tags['tag'].str.lower().fillna('')
movies['genres'] = movies['genres'].fillna('')

# 🎯 Get top 100 popular tags
top_tags = tags['tag'].value_counts().head(100).index.tolist()

# 🎭 Extract genres
unique_genres = sorted(set(
    g for genre_list in movies['genres'] for g in genre_list.split('|') if g != '(no genres listed)'
))

# 🧩 Merge ratings with tags
rating_tags = rating_sample.merge(tags, on=['userId', 'movieId'], how='left')

# 🎯 Title (centered with color)
st.markdown("""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        <h1 style='color: #2E86C1; font-size: 40px;'>🎯 Smart Movie Discovery for Curious Minds</h1>
    </div>
""", unsafe_allow_html=True)

# 🔧 Sidebar for filters
with st.sidebar:
    st.header("🔎 Filter Your Discovery")
    selected_tag = st.selectbox("Select Tag", top_tags)
    selected_genres = st.multiselect("Choose Genres", unique_genres)
    sort_by = st.radio("Sort by", ["Average Rating", "Popularity"])

# 🔍 Filter data based on tag
filtered = rating_tags[rating_tags['tag'].str.contains(selected_tag, na=False)]

# 🔗 Merge with movie metadata
filtered = filtered.merge(movies[['movieId', 'title', 'genres']], on='movieId', how='left')

# 🎭 Apply genre filter
if selected_genres:
    filtered = filtered[filtered['genres'].apply(lambda x: any(g in x for g in selected_genres))]

# 📊 Prepare summary
if not filtered.empty and all(col in filtered.columns for col in ['movieId', 'title', 'genres', 'rating']):
    summary = filtered.groupby(['movieId', 'title', 'genres']).agg(
        Average_Rating=('rating', 'mean'),
        Number_of_Ratings=('rating', 'count')
    ).reset_index()
else:
    summary = pd.DataFrame(columns=['movieId', 'title', 'genres', 'Average_Rating', 'Number_of_Ratings'])

# 🧮 Sort results
if sort_by == "Average Rating":
    summary = summary.sort_values("Average_Rating", ascending=False)
else:
    summary = summary.sort_values("Number_of_Ratings", ascending=False)

# 📈 Plot if data exists
if not summary.empty:
    st.markdown(f"### 🎬 Movies Tagged With: `{selected_tag}`")
    if selected_genres:
        st.markdown(f"🎭 Genres: {', '.join(selected_genres)}")

    chart_type = st.radio("📊 Chart Type", ["Average Rating", "Number of Ratings"])
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

    # 📋 Display table
    styled = chart_data.style.background_gradient(cmap='coolwarm')\
        .format({"Average_Rating": "{:.2f}", "Number_of_Ratings": "{:,.0f}"})
    st.dataframe(styled, use_container_width=True)
else:
    st.warning("No matching movies found for your tag and genre filters. Try a different combination.")