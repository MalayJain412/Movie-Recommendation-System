import pandas as pd
import pickle

# Load pickled objects
final_df = pd.read_pickle('final_df.pkl')
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Function to recommend movies
def recommend(movie):
    try:
        movie_index = final_df[final_df['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        for i in movies_list:
            print(final_df.iloc[i[0]].title)
    except IndexError:
        print(movie + ' not found')

# Test the function
movie = input("Enter the name of the movie: ")

print("Here are some recommended movies: \n")
recommend(movie)
