import streamlit as st
import pickle
import pandas as pd
import requests
#
def fetch_poster(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    return movies['poster_path'][movie_index]

def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters = []
    for i in movies_list:
        # movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].original_title)
        # recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies  #,recommended_movies_posters

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))


st.title('Movie recommender system')

selected_movie_name = st.selectbox(
    'Select a movie that you liked',
    movies['original_title'].values)

if st.button('Recommend'):
    names = recommend(selected_movie_name)
    col1, col2, col3,col4,col5 = st.columns(5,gap="small")

    with col1:
        st.subheader(names[0])
        st.image(fetch_poster(names[0]))

    with col2:
        st.subheader(names[1])
        st.image(fetch_poster(names[1]))

    with col3:
        st.subheader(names[2])
        st.image(fetch_poster(names[2]))

    with col4:
        st.subheader(names[3])
        st.image(fetch_poster(names[3]))

    with col5:
        st.subheader(names[4])
        st.image(fetch_poster(names[4]))


