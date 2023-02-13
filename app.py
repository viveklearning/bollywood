import streamlit as st
import pickle
import pandas as pd
import base64
from selenium import webdriver

BACKGROUND = 'heart_bg.jpg'

class MovieRecommender:

    def __init__(self) -> None:
        self.movies_dict=pickle.load(open('movies_dict.pkl','rb'))
        self.movies=pd.DataFrame(self.movies_dict)
        self.poster_paths = pickle.load(open('poster_paths.pkl','rb'))

        self.similarity=pickle.load(open('similarity.pkl','rb'))
        

    def fetch_poster(self, movie):
        movie_index = self.movies[self.movies['original_title'] == movie].index[0]
        return self.movies['poster_path'][movie_index]

    def recommend(self, movie):
        movie_index = self.movies[self.movies['original_title'] == movie].index[0]
        distances = self.similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:200]

        recommended_movies=[]
        for i in movies_list:
            recommended_movies.append(self.movies.iloc[i[0]].original_title)
        return recommended_movies  

    def findsimilar(self, name1,name2):
        movie_index = self.movies[self.movies['original_title'] == name1].index[0]
        movie_index2 = self.movies[self.movies['original_title'] == name2].index[0]
        return self.similarity[movie_index][movie_index2]

    def find_overlap(self, rec1, rec2):
        for movie1 in rec1:
            for movie2 in rec2:
                if movie1 == movie2:
                    return movie1
        return "Meri Sapnon Ki Rani kab ayegi tu"

    def add_bg(self, image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
        )  

    def find_music_video(self, movie):
        driver = webdriver.Firefox()
        extension = "C:/Users/delsi/AppData/Roaming/Mozilla/Firefox/Profiles/db6rpts6.default-release/extensions/adblockultimate@adblockultimate.net.xpi"

        driver.install_addon(extension)
        search = movie + " song"

        driver.get(f"https://www.youtube.com/results?search_query={search}")
        #video_links = driver.find_elements('xpath','//*[@id="video-title"]')
        #video_link = video_links[0].get_attribute('href')
        video_links = driver.find_element('xpath', '//*[@class="style-scope ytd-video-renderer"]')
        #driver.get(video_links[0].get_attribute('href'))
        video_links.click()
        play = driver.find_element('xpath', '//*[@class="ytp-play-button ytp-button"]')
        play.click()

        #st.video(video_links[0].get_attribute('href'), start_time=0)



if __name__ == '__main__':
    mv = MovieRecommender()

    mv.add_bg(BACKGROUND) 

    st.title('Movie Recommender')

    selected_movie_name1 = st.selectbox(
        'Select a movie that you like',
        mv.movies['original_title'].values)

    selected_movie_name2 = st.selectbox(
        'Select a movie that you like',
        mv.movies['original_title'].values,key=2)


    if st.button('Find our similarity'):
        ans = mv.findsimilar(selected_movie_name1,selected_movie_name2)
        st.subheader(ans*10*9/10)
        recommendations1 = mv.recommend(selected_movie_name1)
        recommendations2 = mv.recommend(selected_movie_name2)

        print(recommendations1)
        print(recommendations2)
        
        overlap = mv.find_overlap(recommendations1, recommendations2)   

        if ans < 0.3:
            st.subheader(f"You have different tastes but why not try {overlap} ?")
        else:
            st.subheader(f"The Movie That Connects You is : {overlap}")
            
        print(mv.poster_paths)
        st.image(mv.poster_paths[overlap])
        mv.find_music_video(overlap)
        print(mv.poster_paths["Uri: The Surgical Strike"])


    

