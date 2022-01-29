from multiprocessing.sharedctypes import Value
import pandas as pd
import streamlit as st
import pickle
import requests

st.set_page_config(
   page_title="Recommendation App",
   layout="wide",
   initial_sidebar_state="expanded",
)
similarity=pickle.load(open('similarity.pkl', 'rb'))
movies=pickle.load(open('movie_in_dict.pkl', 'rb'))
new_data=pd.DataFrame(movies)
st.title("Recommendation System")

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = get_index(movie)
    simi_vec = list(enumerate(similarity[index][1]))
    movie_list = sorted(simi_vec, reverse=True, key=lambda i: i[1])[1:6]
    movie_posters=[]
    movies_recommended=[]
    for i in movie_list:
        j = i[0]
        movie_id=new_data.iloc[j].id
        movie_posters.append(fetch_poster(movie_id))
        movies_recommended.append(new_data.iloc[j].title)
    return movies_recommended,movie_posters

def get_index(movie):
    index=0
    for i in range(4086):
        if(new_data['title'][i]==movie):
            index=i
            break
    return index

movie_selected = st.selectbox(label="Select a Movie Name from the List ",options=new_data)
curr_id=new_data[new_data['title']==movie_selected].id.values[0]
st.write('You Selected:- ')
st.image(fetch_poster(curr_id),caption=movie_selected,width=200)
if st.button('Recommend'):
    st.write('Recommended Movies for you are :- ')
    recommended_movie_names,recommended_movie_posters = recommend(movie_selected)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

