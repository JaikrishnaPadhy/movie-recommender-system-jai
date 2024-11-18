import streamlit as st
import pickle
import pandas as pd
import requests
import gdown

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkOGVmMzJhNmU5OTQzMWZjZGQyMTVlNTU1MDVkYzMyMSIsIm5iZiI6MTczMTk1MTcyOC4yNzcyNzA2LCJzdWIiOiI2NzNiNzRkOWU4MzFmOGFhNDllMzUyYjIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.sChfk8Knt_zE3Ks8A31QPJ3Tu-oP6NwOT6lnGrCnspU"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

file_id = '1Vit4Hpi1WU-ORgrxmG3QIO3Ws5CKp7kX'
pickle_url = f'https://drive.google.com/uc?id={file_id}'

gdown.download(pickle_url, 'similarity.pkl', quiet=False)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# a = requests.get(pickle_url)
# with open("similarity.pkl", "wb") as f:
#     f.write(a.content)
#
# with open ("similarity.pkl", "rb") as f:
#     similarity = pickle.load(f)


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'Select your movie',
movies['title'].values)

if st.button('Recommend'):
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

