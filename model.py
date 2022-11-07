import streamlit as st
import pickle
import pandas as pd

movies_data=pickle.load(open('moviesmodel.pkl','rb'))

import difflib
def recommend(movie_name):
	list_of_all_titles = movies_data['title'].tolist()
	find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
	return find_close_match

st.title('Movie Recommendation System') 

selected_movie_name=st.selectbox(
'Watch your favorite movie and enjoy your day',
movies_data['title'].values)

if st.button('Recommend'):
    recommendations=recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)