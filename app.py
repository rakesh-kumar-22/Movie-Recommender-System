import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f1a6197f93e2e8e0ffb89f23d7f66de4&language=en-US"
    response = requests.get(url)
    data = response.json()

    # Check if 'poster_path' exists in the data
    if 'poster_path' in data and data['poster_path']:
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        # Return a placeholder image if the poster is not available
        full_path = "https://via.placeholder.com/500x750?text=No+Poster+Available"

    return full_path


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distance = similarity[movie_index]
    recommend_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in recommend_list:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        # Fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


movies_list = pickle.load(open('movies.pkl', 'rb'))
movie_name = movies_list['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie",
    movie_name,
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
