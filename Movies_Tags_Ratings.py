import streamlit as st
import pandas as pd
import plotly.express as px

# 🎨 Custom page style
st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(to bottom right, #ffffff, #f0f8ff);
            font-family: 'Segoe UI', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# 🎯 Title
st.markdown("""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        <h1 style='color: #2E86C1; font-size: 40px;'>🎯 Smart Movie Discovery for Curious Minds</h1>
    </div>
""", unsafe_allow_html=True)

# 📁 Load data
rating = pd.read_csv("rating_sample.csv")
tags = pd.read_csv("tags.csv", encoding='ISO-8859-1')
movies = pd.read_csv("movies.csv", encoding='ISO-8859-1')

# 🧹 Preprocess
tags['tag'] = tags['tag'].str.lower().fillna('')
top_tags = tags['tag'].value_counts().head(100).index.tolist()

movies['genres'] = movies['genres'].fillna('')

# Extract unique genres
unique_genres = sorted(set(
    g for genre_str in movies['genres'] for g in genre_str.split('|') if g != '(no genres listed)'
))

# 🔧 Sidebar filters
with st.sidebar:
    st.header("🔎 Filter Your Discovery")
    selected_tag = st.selectbox("Search by Tag", top_tags)
    selected_genres = st.multiselect("Filter by Genre(s)", unique_genres)
    sort_by = st.radio("Sort by:", ["Average Rating", "Popularity"])

# 🔍 Merge data
rating_tags = pd.merge(rating, tags, on=["userId", "movieId"], how="left")
merged = pd.merge(rating_tags, movies, on="movieId", how="left")

# 🔍 Filter by tag
filtered = merged[merged['tag_x'].str.contains(selected_tag, na=False)]

# ✅ Ensure title and genres are present
filtered = filtered[['movieId', 'title', 'genres', 'rating']]

# 🎭 Filter by genre
if selected_genres:
    filtered = filtered[filtered['genres'].apply(lambda x: any(g in x for g in selected_genres))]

# 📊 Summarize
if not filtered.empty:
    summary = filtered.groupby(['movieId', 'title', 'genres']).agg(
        Average_Rating=('rating', 'mean'),
        Number_of_Ratings=('rating', 'count')
    ).reset_index()

    # 🧮 Sort
    if sort_by == "Average Rating":
        summary = summary.sort_values("Average_Rating", ascending=False)
    else:
        summary = summary.sort_values("Number_of_Ratings", ascending=False)

    # 📊 Chart
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

    # 📋 Styled Table
    st.dataframe(chart_data.style.background_gradient(cmap='coolwarm').format(
        {"Average_Rating": "{:.2f}", "Number_of_Ratings": "{:,.0f}"}
    ), use_container_width=True)

else:
    st.info("No matching movies found. Try a different tag or genre.")