import pandas as pd
import streamlit as st
import gzip
import pickle
import re

# Function to load compressed pickle files
def load_compressed_pickle(file_path):
    with gzip.open(file_path, 'rb') as f:
        return pickle.load(f)

# Load pickled objects
final_df = load_compressed_pickle('final_df.pkl.gz')
similarity = load_compressed_pickle('similarity.pkl.gz')

# Create the 'modified_title' column if it doesn't exist
if 'modified_title' not in final_df.columns:
    final_df['modified_title'] = final_df['title'].apply(lambda x: re.sub(r'[^a-zA-Z0-9]', '', x).lower())

# Function to recommend movies
def recommend(movie, n):
    try:
        if not movie:
            return ["Please enter a movie title."]
        
        movie_normalized = re.sub(r'[^a-zA-Z0-9]', '', movie).lower()
        movie_index = final_df[final_df['modified_title'] == movie_normalized].index[0]
        distances = similarity[movie_index]
        
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:n+1]
        recommended_movies = [final_df.iloc[i[0]].title for i in movies_list]
        return recommended_movies
    
    except IndexError:
        return [f"Movie '{movie}' not found."]
    except Exception as e:
        return [f"An error occurred: {str(e)}"]

# Streamlit app
st.title("Movie Recommendation Site** 😍")
st.header("Welcome to your personal movie recommendation site 🎬")
st.write("Type in the name of a movie, and we'll provide you with similar recommendations!")
st.write("Note: Currently will take input of foreign movies only")

# Search bar with dynamic suggestions
# search_query = st.text_input("Movie Name (e.g., 'Inception')", placeholder="Enter movie name here...")
# filtered_movies = final_df['title'][final_df['title'].str.contains(search_query, case=False, na=False)].tolist()[:]
filtered_movies = final_df['title'].tolist()[:]
selected_movie = st.selectbox("Enter Movies Names: ", options=filtered_movies, index=0 if filtered_movies else None)

number = st.number_input("Number of recommendations", min_value=1, step=1, value=5)
st.write(f"Number of movies to be predicted: {number}")

if st.button("Recommend"):
    recommendations = recommend(selected_movie, number)
    
    st.write(f"Here are some recommended movies similar to {selected_movie} 🎬:")
    for movie in recommendations:
        st.write(f"- {movie}")
        
# Feedback section with custom CSS class
st.markdown('<div class="feedback-section">', unsafe_allow_html=True)

feedback = st.radio("Give your feedback:", ["👍 Thumbs Up", "👎 Thumbs Down"], index=0)

if feedback == "👍 Thumbs Up":
    st.write("You selected: 👍")
    st.write("Thanks for your feedback! 😊")
elif feedback == "👎 Thumbs Down":
    st.write("You selected: 👎")
    st.write("Thanks for your feedback! 😊 We will try to improve. 🤔")

# # Test the function
# movie = input("Enter the name of the movie: ")

# print("Here are some recommended movies: \n")
# recommend(movie)
