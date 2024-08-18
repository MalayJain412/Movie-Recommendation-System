
import pandas as pd
import pickle
import streamlit as st

# Load pickled objects
final_df = pd.read_pickle('final_df.pkl')
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Function to recommend movies
def recommend(movie):
    try:
        # Check if the movie is provided and not empty
        if not movie:
            return ["Please enter a movie title."]
        
        # Find the movie index
        movie_index = final_df[final_df['title'] == movie].index[0]
        distances = similarity[movie_index]
        
        # Get top 5 similar movies
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies = [final_df.iloc[i[0]].title for i in movies_list]
        return recommended_movies
    
    except IndexError:
        return [f"Movie '{movie}' not found."]
    except Exception as e:
        return [f"An error occurred: {str(e)}"]

# Streamlit app
st.write("Enter Your Movie:")
x = st.text_input("Movie")

if st.button("Click Me"):
    # Call the recommend function
    recommendations = recommend(x)
    
    # Debugging: Display what's returned by recommend()
    st.write("Debug info:", recommendations)
    
    # Display the recommendations
    st.write("Here are some recommended movies:")
    for movie in recommendations:
        st.write(f"- {movie}")

# # Test the function
# movie = input("Enter the name of the movie: ")

# print("Here are some recommended movies: \n")
# recommend(movie)
