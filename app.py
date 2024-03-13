import pandas as pd
import streamlit as st
import pickle
import requests

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'MOVIES',
    movies['title'].values
)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=0d14859567362c8ca0b09c36cd53eccd&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies_names = []
    recommended_movie_posters = []
    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies_names.append(movies.iloc[i[0]].title)
    return recommended_movies_names, recommended_movie_posters


if st.button("Recommend"):
    names, postures = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
        st.text(names[0])
        st.image(postures[0])
    with col2:
        st.text(names[1])
        st.image(postures[1])

    with col3:
        st.text(names[2])
        st.image(postures[2])
    with col4:
        st.text(names[3])
        st.image(postures[3])
    with col5:
        st.text(names[4])
        st.image(postures[4])

