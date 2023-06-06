import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

def recommend(dataset, number_of_recommendations, user):
    toot_df =pd.DataFrame(dataset)
    
    tfidf_vectorizer = TfidfVectorizer()

    # Generate the tf-idf vectors for the corpus
    content = toot_df['content']

    tfidf_matrix = tfidf_vectorizer.fit_transform(content)
    # Transform the sentence into a tf-idf vector
    sentence_vector = tfidf_vectorizer.transform(["Netflix"])

    # Calculate the cosine similarity between the sentence vector and all toot vectors
    cosine_sim_sentence = linear_kernel(sentence_vector, tfidf_matrix).flatten()

    # Get the pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim_sentence))

    # Sort the toots based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores for the specified number of most similar toots
    sim_scores = sim_scores[:number_of_recommendations]
    sim_indices = [i[0] for i in sim_scores]
    print(sim_indices)

    # Return the recommended toots as a list of content
    list_of_content = content.iloc[sim_indices]
    return list_of_content.tolist()