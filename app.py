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

def findsimilar(name1,name2):
    movie_index = movies[movies['original_title'] == name1].index[0]
    movie_index2 = movies[movies['original_title'] == name2].index[0]
    return similarity[movie_index][movie_index2]


movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))


st.title('Movie recommender system')

selected_movie_name = st.selectbox(
    'Select a movie that you liked',
    movies['original_title'].values)

selected_movie_name2 = st.selectbox(
    'Select a movie that you liked',
    movies['original_title'].values,key=2)


ans=findsimilar(selected_movie_name,selected_movie_name2)

#including the song

# this one is using spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Authenticate with Spotify
# auth = SpotifyOAuth(client_id='b4f22aa81b18415b935e04cb57efb948',
#                      client_secret='a8f11d194b4b4797b418a1cf08c4d86e',
#                      redirect_uri='http://localhost:8501/callback/')
# sp = spotipy.Spotify(auth_manager=auth)
#
# # Search for the movie and retrieve its soundtrack
# movie_name = "The Dark Knight"
# results = sp.search(q=f"{movie_name} soundtrack", type='album')
# soundtrack = results['albums']['items'][0]
#
# # Get the first track from the soundtrack
# first_track = sp.album_tracks(soundtrack['id'])['items'][0]
#
# # Play the first track on Spotify
# sp.start_playback(uris=[first_track['uri']])





if st.button('find our similarity'):
    st.subheader(ans*10*9/10)

    # names = recommend(selected_movie_name)
    # col1, col2, col3,col4,col5 = st.columns(5,gap="small")
    #
    # with col1:
    #     st.subheader(names[0])
    #     st.image(fetch_poster(names[0]))
    #
    # with col2:
    #     st.subheader(names[1])
    #     st.image(fetch_poster(names[1]))
    #
    # with col3:
    #     st.subheader(names[2])
    #     st.image(fetch_poster(names[2]))
    #
    # with col4:
    #     st.subheader(names[3])
    #     st.image(fetch_poster(names[3]))
    #
    # with col5:
    #     st.subheader(names[4])
    #     st.image(fetch_poster(names[4]))



# to play using youtube
    
# import os
# import webbrowser
# 
# def play_song_on_youtube(movie_title):
#     search_query = movie_title + ' soundtrack'
#     webbrowser.open('https://www.youtube.com/results?search_query=' + search_query)
# 
# movie_title = 'The Shawshank Redemption'
# 
# play_song_on_youtube(movie_title)

