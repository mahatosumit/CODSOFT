from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

# Load and prepare data
try:
    # Load the dataset
    movies_df = pd.read_csv('./movies.csv')

    # Print column names for debugging (remove after debugging)
    print(movies_df.columns)

    # Ensure necessary columns are present
    if 'Film' not in movies_df.columns or 'Genre' not in movies_df.columns:
        raise ValueError("The dataset must include 'Film' and 'Genre' columns.")

    # Fill missing values and create a combined feature column
    movies_df['Genre'] = movies_df['Genre'].fillna('')
    movies_df['combined_features'] = movies_df['Genre']
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# Create TF-IDF matrix for cosine similarity
try:
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['combined_features'])
    cosine_sim = cosine_similarity(tfidf_matrix)
except Exception as e:
    print(f"Error creating TF-IDF matrix: {e}")
    exit()

def get_recommendations(movie_title, cosine_sim=cosine_sim):
    try:
        # Check if the movie title exists
        if movie_title not in movies_df['Film'].values:
            return [{"error": "Movie not found. Please select a valid movie."}]

        # Get index of the movie
        idx = movies_df[movies_df['Film'] == movie_title].index[0]

        # Compute similarity scores
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]  # Top 5 similar movies excluding itself

        # Get indices of recommended movies
        movie_indices = [i[0] for i in sim_scores]
        recommendations = movies_df.iloc[movie_indices][['Film', 'Genre']]
        return recommendations.to_dict('records')
    except Exception as e:
        return [{"error": f"An error occurred: {e}"}]

@app.route('/')
def home():
    try:
        # Get list of all movies for dropdown
        movie_list = movies_df['Film'].tolist()
        return render_template('index.html', movies=movie_list)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        movie = request.form.get('movie', '')
        if not movie:
            return jsonify([{"error": "Please provide a movie title."}])

        recommendations = get_recommendations(movie)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify([{"error": f"An error occurred: {e}"}])

if __name__ == '__main__':
    app.run(debug=True)
