import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.set_page_config(page_title="Netflix Data Analysis", layout="wide")
st.title("🎬 Netflix Movies & TV Shows Dashboard")
st.markdown("""
This dashboard explores the Netflix dataset to uncover trends in content types, 
top contributing countries, and release years.
""")

@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv')
    # Basic cleaning based on your analysis
    df['director'] = df['director'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    return df

df = load_data()

st.sidebar.header("Filter Options")
content_type = st.sidebar.multiselect("Select Content Type:", 
                                      options=df['type'].unique(), 
                                      default=df['type'].unique())

year_range = st.sidebar.slider("Select Release Year Range:", 
                               int(df['release_year'].min()), 
                               int(df['release_year'].max()), 
                               (2010, 2021))

filtered_df = df[(df['type'].isin(content_type)) & 
                 (df['release_year'].between(year_range[0], year_range[1]))]


col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Titles", len(filtered_df))
with col2:
    st.metric("Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
with col3:
    st.metric("TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Distribution of Content")

    type_counts = filtered_df['type'].value_counts().reset_index()
    fig_pie = px.pie(type_counts, values='count', names='type', 
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("Top 10 Countries")
    top_countries = filtered_df['country'].value_counts().head(10).reset_index()
    fig_bar = px.bar(top_countries, x='country', y='count', 
                     labels={'count': 'Number of Titles', 'country': 'Country'},
                     color='count')
    st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("Content Addition Trend Over Years")
trend_data = filtered_df.groupby('year_added').size().reset_index(name='count')
fig_line = px.line(trend_data, x='year_added', y='count', markers=True)
st.plotly_chart(fig_line, use_container_width=True)


st.subheader("Raw Data Preview")
st.dataframe(filtered_df.head(100))

