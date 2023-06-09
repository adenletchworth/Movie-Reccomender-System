from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def processInput(user_description: str, user_genre: str):
    
    # Importing movie data
    full_movie_data = pd.read_csv('movies_combined.csv')

    # Getting features from dataframe
    description_df = full_movie_data['Description']
    title_df = full_movie_data['Title']
    genre_df = full_movie_data['Genre']

    # Getting stop words 
    stop_words = set(stopwords.words('english'))
    # Initializing lemmatizer class
    lz = WordNetLemmatizer()

    # Tokenizing user description input
    input_tokens = word_tokenize(user_description)
    # Filtering and lemmatizing the tokenized user description input
    input_words = [lz.lemmatize(word.lower()) for word in input_tokens if word.lower() not in stop_words]

    
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    # Encode movie descriptions and user input
    encoded_descriptions = model.encode(description_df)
    encoded_user_description = model.encode([' '.join(input_words)])
    # Encode movie genres and user input
    encoded_genres = model.encode(genre_df)
    encoded_user_genre = model.encode([user_genre])

    # Calculate cosine similarity for movie versus input
    similarity_description_scores = cosine_similarity(encoded_descriptions, encoded_user_description)
    similarity_genre_scores = cosine_similarity(encoded_genres, encoded_user_genre)

    # Assign weights
    description_weight = .6
    genre_weight = .4

    # Calculate weighted similarity scores
    weighted_scores = (description_weight * similarity_description_scores) + (genre_weight * similarity_genre_scores)

    # Sort movies based on weighted similarity scores
    sorted_indices = weighted_scores.argsort(axis=0)[::-1].flatten()

    # Find the most similar movies with the highest score
    most_similar_indices = sorted_indices[0:3]

    # Get the most similar movie titles, descriptions, and genres
    most_similar_movie_titles = title_df[most_similar_indices]
    most_similar_movie_descriptions = description_df[most_similar_indices].apply(str.strip)
    most_similar_movie_genres = genre_df[most_similar_indices]

    return most_similar_movie_titles, most_similar_movie_descriptions, most_similar_movie_genres


""""
user_input = 'While exploring her new home, a girl named Coraline (Dakota Fanning) discovers a secret door, behind which lies an alternate world that closely mirrors her own but, in many ways, is better. She rejoices in her discovery, until Other Mother (Teri Hatcher) and the rest of her parallel family try to keep her there forever. Coraline must use all her resources and bravery to make it back to her own family and life.'
user_genre = 'Kids & family, Fantasy, Animation'

most_similar_movie_titles, most_similar_movie_descriptions, most_similar_movie_genres = processInput(user_input, user_genre)

most_similar_results = zip(most_similar_movie_titles,most_similar_movie_descriptions,most_similar_movie_genres)

for title,description,genre in most_similar_results:
    print("Title:", title)
    print("Description:", description)
    print("Genre:", genre)
    print()

    """

