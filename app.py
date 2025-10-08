
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Netflix Content Trends Analysis")

# File uploader
uploaded_file = st.file_uploader("📁 Upload Netflix Dataset CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Data cleaning
    df.drop_duplicates(inplace=True)
    df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')
    df['Year'] = df['Release_Date'].dt.year
    df.fillna({'Country': 'Unknown', 'Type': 'Unknown', 'Category': 'Unknown'}, inplace=True)

    # Preprocess
    genre_df = df[['Type', 'Year']].dropna().copy()
    genre_df['Type'] = genre_df['Type'].str.split(', ')
    genre_df = genre_df.explode('Type')
    
    country_df = df[['Country']].copy()
    country_df['Country'] = country_df['Country'].str.split(', ')
    country_df = country_df.explode('Country')

    # Overview metrics
    st.subheader("📌 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Titles", len(df))
    col2.metric("Year Range", f"{df['Year'].min()} - {df['Year'].max()}")
    col3.metric("Top Country", df['Country'].value_counts().idxmax())

    # Visualization 1: Movies vs TV Shows Over Time
    st.subheader("🎬 Movies vs TV Shows Over the Years")
    fig1, ax1 = plt.subplots(figsize=(10,4))
    sns.countplot(data=df, x="Year", hue="Category", palette="Set2", ax=ax1)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # Visualization 2: Top Genres Over Time
    st.subheader("🎭 Top 8 Genres Trend")
    top_genres = genre_df['Type'].value_counts().nlargest(8).index.tolist()
    filtered_genres = genre_df[genre_df['Type'].isin(top_genres)]
    fig2, ax2 = plt.subplots(figsize=(12,5))
    sns.countplot(data=filtered_genres, x="Year", hue="Type", ax=ax2)
    plt.xticks(rotation=45)
    ax2.legend(title="Genre", bbox_to_anchor=(1.01, 1))
    st.pyplot(fig2)

    # Visualization 3: Country Contributions
    st.subheader("🌍 Top 10 Contributing Countries")
    top_countries = country_df['Country'].value_counts().nlargest(10)
    fig3, ax3 = plt.subplots(figsize=(10,4))
    sns.barplot(x=top_countries.index, y=top_countries.values, palette="coolwarm", ax=ax3)
    plt.xticks(rotation=45)
    ax3.set_ylabel("Number of Titles")
    st.pyplot(fig3)

    # Visualization 4: Top 10 Directors
    st.subheader("🎥 Top 10 Directors on Netflix")
    top_directors = df['Director'].dropna().value_counts().head(10)
    fig4, ax4 = plt.subplots(figsize=(10,4))
    sns.barplot(x=top_directors.values, y=top_directors.index, palette="magma", ax=ax4)
    ax4.set_xlabel("Number of Titles")
    st.pyplot(fig4)

    # Visualization 5: Movie Duration
    st.subheader("⏱️ Movie Duration Distribution")
    movie_df = df[df['Category'] == 'Movie'].copy()
    movie_df['Minutes'] = movie_df['Duration'].str.extract(r'(\d+)').astype(float)
    movie_df = movie_df.dropna(subset=['Minutes'])
    if not movie_df.empty:
        fig5, ax5 = plt.subplots(figsize=(10,4))
        sns.histplot(movie_df['Minutes'], bins=30, kde=True, color='green', ax=ax5)
        ax5.set_xlabel("Duration (minutes)")
        st.pyplot(fig5)
    else:
        st.warning("⚠️ No valid movie durations found to plot.")

    # Visualization 6: TV Show Seasons
    st.subheader("📺 TV Show Season Counts")
    tv_df = df[df['Category'] == 'TV Show'].copy()
    tv_df['Seasons'] = tv_df['Duration'].str.extract(r'(\d+)').astype(float)
    tv_df = tv_df.dropna(subset=['Seasons'])
    if not tv_df.empty:
        fig6, ax6 = plt.subplots(figsize=(10,4))
        sns.countplot(x='Seasons', data=tv_df, palette="Blues", order=tv_df['Seasons'].value_counts().index[:10], ax=ax6)
        st.pyplot(fig6)
    else:
        st.warning("⚠️ No valid season count data found to plot.")

    # Footer
    st.markdown("---")
    st.markdown("Created by **Your Name** · Built with Streamlit")
else:
    st.info("👈 Please upload a Netflix dataset CSV file to begin.")
