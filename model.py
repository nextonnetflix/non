import streamlit as st
import pickle
import pandas as pd

#https://media.githubusercontent.com/media/nextonnetflix/non/main/similarity.pkl

movies_data=pickle.load(open('moviesmodel.pkl','rb'))
#similarity=pickle.load(open('https://media.githubusercontent.com/media/nextonnetflix/non/main/similarity.pkl','rb'))

#import urllib.request
#similarity=pickle.load(urllib.request.urlopen("https://media.githubusercontent.com/media/nextonnetflix/non/main/similarity.pkl"))
similarity=pickle.load(open('similarity.pkl','rb'))

import difflib
def recommend(movie_name):
	list_of_all_titles = movies_data['title'].tolist()
	find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
	close_match = find_close_match[0]
	index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
	similarity_score = list(enumerate(similarity[index_of_the_movie]))
	sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True)
	i=0
	movieslist=[]
	for movie in sorted_similar_movies:
		index = movie[0]
		title_from_index = movies_data[movies_data.index==index]['title'].values[0]
		if (i<30):
			movieslist.append(title_from_index)
			i+=1
	return movieslist

st.title('Movie Recommendation System') 

selected_movie_name=st.selectbox(
'Watch your favorite movie and enjoy your day',
movies_data['title'].values)

if st.button('Recommend'):
    recommendations=recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)
