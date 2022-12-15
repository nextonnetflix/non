import streamlit as st
#from database import *
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import difflib
import hashlib

movies_data=pickle.load(open('moviesmodel.pkl','rb'))
similarity=pd.read_csv("matrix.csv").to_numpy()
scrapped_data=pd.read_csv("scrapped_data.csv")
st.set_page_config(layout="wide")
 
headerSection = st.container()
signUpSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def show_main_page():
    with mainSection:

        user_result = view_all_users()
        print(user_result)

        def recommend_movies(movie_name):
            list_of_all_titles = movies_data['title'].tolist()
            find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
            close_match = find_close_match[0]
            index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
            indexforsim = index_of_the_movie-1
            similarity_score = list(enumerate(similarity[indexforsim]))
            sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True)
            i=0
            selected_movie=sorted_similar_movies[0]
            movieslist=[]
            
            for movie in sorted_similar_movies[1:]:
                index = movie[0]
                title_from_index = movies_data[movies_data.index==index]['title'].values[0]
                score = str(int(movie[1]*100)+30)+"%"
                type = movies_data.loc[movies_data['title']==title_from_index]['type']
                description = movies_data.loc[movies_data['title']==title_from_index]['description']
                genre = movies_data.loc[movies_data['title']==title_from_index]['genre']
                cast = movies_data.loc[movies_data['title']==title_from_index]['cast']
                creators = movies_data.loc[movies_data['title']==title_from_index]['creators']
                link = scrapped_data.loc[scrapped_data['title']==title_from_index]['link']
                year = scrapped_data.loc[scrapped_data['title']==title_from_index]['year']
                img = scrapped_data.loc[scrapped_data['title']==title_from_index]['poster']
                data = {"title":title_from_index,"poster":list(img)[0],"genre":list(genre)[0],"link":list(link)[0],"description":list(description)[0],"year":list(year)[0],"type":list(type)[0],"type":list(type)[0],"cast":list(cast)[0],"creators":list(creators)[0],"score":score}
                if (i<30):
                    movieslist.append(data)
                    i+=1
            return movieslist

        #st.title('NextOnNetflix')
        #st.image("Logo.png", width=400)

        selected_movie_name=st.selectbox('Select Title',movies_data['title'].values)

        list_of_all_titles = movies_data['title'].tolist()
        find_close_match = difflib.get_close_matches(selected_movie_name, list_of_all_titles)
        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        title_from_index = movies_data[movies_data.index==index_of_the_movie]['title'].values[0]
        type = movies_data.loc[movies_data['title']==title_from_index]['type']
        description = movies_data.loc[movies_data['title']==title_from_index]['description']
        genre = movies_data.loc[movies_data['title']==title_from_index]['genre']
        cast = movies_data.loc[movies_data['title']==title_from_index]['cast']
        creators = movies_data.loc[movies_data['title']==title_from_index]['creators']
        img = scrapped_data.loc[scrapped_data['title']==title_from_index]['poster']
        link = scrapped_data.loc[scrapped_data['title']==title_from_index]['link']
        year = scrapped_data.loc[scrapped_data['title']==title_from_index]['year']
        current_movie = {"title":title_from_index,"poster":list(img)[0],"genre":list(genre)[0],"link":list(link)[0],"description":list(description)[0],"year":list(year)[0],"type":list(type)[0],"type":list(type)[0],"cast":list(cast)[0],"creators":list(creators)[0]}

        if st.button('Search'):

            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(current_movie["poster"])

            with col2:
                st.title(current_movie["title"])
                st.write('Year: ' + current_movie["year"] + ' | Type: ' + current_movie["type"])
                st.write('Description: ' + current_movie["description"])
                st.write('Cast: ' + current_movie["cast"])
                st.write('Creators: ' + current_movie["creators"])
                st.write('Genre: ' + current_movie["genre"])
                st.write('Watch Now: ' + current_movie["link"])
            st.markdown("""---""")


            recommendations=recommend_movies(selected_movie_name)
            
            st.title("More like this")

            rec1, rec2 = st.columns([1, 2])

            for i in recommendations:
                st.title(i["title"])
                st.write('Year: ' + i["year"] + ' | Type: ' + i["type"] + ' | Similarity Score: ' + recommendations[0]["score"])
                st.image(i["poster"])
                st.write('Description: ' + i["description"])
                st.write('Cast: ' + i["cast"])
                st.write('Creators: ' + i["creators"])
                st.write('Genre: ' + i["genre"])
                st.write('Watch Now: ' + i["link"])
                st.markdown("""---""")

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    
def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)
    
def LoggedIn_Clicked(userName, password):
    if login_user(userName, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")
    
def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            userName = st.text_input (label="", value="", placeholder="Enter your user name")
            password = st.text_input (label="", value="",placeholder="Enter password", type="password")
            st.button ("Login", on_click=LoggedIn_Clicked, args= (userName, password))

def show_signup_page():
    with signUpSection:
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            if st.info("Go to Login Menu to login"):
                show_login_page() 


with headerSection:
    st.image("Logo.png", width=400)
    #st.title("Streamlit Application")

    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_signup_page()
    else:
        if st.session_state['loggedIn']:
            show_logout_page()    
            show_main_page()  
        else:
            show_login_page()

            
           
        
            
