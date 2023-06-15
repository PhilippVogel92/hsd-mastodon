from .tfidf import recommend_with_tfidf_for_account
from .spacy import recommend_with_spacy_for_account
import pandas as pd


def calculate_interaction_score(toot_df):
    """Function to calculate the interaction score of a toot."""

    # Calculate the interaction score
    toot_df["interaction_score"] = toot_df["favourites_count"] + toot_df["replies_count"] + toot_df["reblogs_count"]

    # Normalize the interaction score to the value range [0, 1]
    max_interaction_score = toot_df["interaction_score"].max()
    toot_df["interaction_score"] = toot_df["interaction_score"] / max_interaction_score

    return toot_df


def calculate_ranking_score(toot_df, similarity_weight, interaction_weight, sort_by_ranking_score):
    """Function to calculate the ranking score of a toot."""

    # Calculate the ranking score
    toot_df["ranking_score"] = (similarity_weight * toot_df["cosine_sim"]) + (
        interaction_weight * toot_df["interaction_score"]
    )

    if sort_by_ranking_score:
        # Sort the DataFrame according to the ranking score (descending)
        toot_df.sort_values("ranking_score", ascending=False, inplace=True)
        toot_df.reset_index(drop=True, inplace=True)

    return toot_df


def get_recommendations_with_ranking_system(account_id, number_of_recommendations, similarity_concept):
    if similarity_concept == "tfidf":
        recommendations_for_account = recommend_with_tfidf_for_account(account_id, number_of_recommendations)
    elif similarity_concept == "spacy":
        recommendations_for_account = recommend_with_spacy_for_account(account_id, number_of_recommendations)
    else:
        return None

    # Set the weights for Similarity score and Interaction score
    similarity_weight = 0.5
    interaction_weight = 0.5

    # transform recommendations_for_account to a DataFrame
    recommendations_for_account_df = pd.DataFrame(recommendations_for_account)

    # Calculate the interaction score and expand the DataFrame
    recommendations_for_account_df = calculate_interaction_score(recommendations_for_account_df)

    # Calculate the ranking score, expand the DataFrame and sort the DataFrame by ranking score
    recommendations_with_ranking = calculate_ranking_score(
        recommendations_for_account_df,
        similarity_weight,
        interaction_weight,
        sort_by_ranking_score=True,
    )
    return recommendations_with_ranking.to_dict(orient="records")
