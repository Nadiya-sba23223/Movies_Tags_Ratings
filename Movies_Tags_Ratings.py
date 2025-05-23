import streamlit as st
import pandas as pd
import plotly.express as px

# 🎨 Custom CSS for look and feel
st.markdown("""
    <style>
        body { background-color: #f4f8fb; }
        .stApp { background-image: linear-gradient(to bottom right, #ffffff, #e8f1f9); }
    </style>
""", unsafe_allow_html=True)

# 🎯 Stylish, centered title
st.markdown("""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        <h1 style='color: #2E86C1; font-size: 40px;'>🎯 Smart Movie Discovery for Curious Minds</h1>
    </div>
""", unsafe_allow_html=True)

# 📁 Load data
rating = pd.read_csv("rating_sample.csv")
tags_df = pd.read_csv("tags.csv", encoding='ISO-8859-1')
movies = pd.read_csv("movies.csv", encoding='ISO-8859-1')

# 🔧 Preprocessing
tags_df['tag'] = tags_df['tag'].str.lower().fillna('')
top_tags = tags_df['tag'].value_counts().head(100).index.tolist()

# 🧩 Merge ratings and tags
rating_tags = rating.merge(tags_df[['userId', 'movieId', 'tag']], on=['userId', 'movieId'], how='left')

# 🔧 Sidebar filter
st.sidebar.header("🔍 Filter by Tag")
selected_tag = st.sidebar.selectbox("Choose from Top 100 Tags", sorted(top_tags))
sort_by = st.sidebar.radio("Sort by:", ["Average Rating", "Popularity"])

# 🔍 Filter data
filtered = rating_tags[rating_tags['tag'].str.contains(selected_tag, na=False)]
filtered = filtered.merge(movies[['movieId', 'title', 'genres']], on='movieId', how='left')

# 📊 Summary
if not filtered.empty:
    summary = filtered.groupby(['movieId', 'title', 'genres']).agg(
        Average_Rating=('rating', 'mean'),
        Number_of_Ratings=('rating', 'count')
    ).reset_index()

    if sort_by == "Average Rating":
        summary = summary.sort_values("Average_Rating", ascending=False)
    else:
        summary = summary.sort_values("Number_of_Ratings", ascending=False)

    # 🎨 Chart selection
    st.markdown(f"### 🎬 Top Movies Tagged With: `{selected_tag}`")
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

    # 🧾 Styled table
    styled = chart_data.style.background_gradient(cmap='coolwarm')\
        .format({"Average_Rating": "{:.2f}", "Number_of_Ratings": "{:,.0f}"})
    st.dataframe(styled, use_container_width=True)
else:
    st.info("No matching results. Try a different tag.")