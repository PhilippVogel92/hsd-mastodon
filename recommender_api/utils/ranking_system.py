from .tfidf import TFIDFRecommender
from .spacy_sim import recommend_with_spacy_for_account
import pandas as pd


class RankingSystem:
    """Class to calculate the ranking score of a status."""

    def __init__(
        self,
        nlp_model_loader,
        similarity_weight=0.5,
        interaction_weight=0.5,
        number_of_recommendations=20,
        similarity_concept="tfidf",
        sort_by_ranking_score=True,
    ):
        self.similarity_weight = similarity_weight
        self.interaction_weight = interaction_weight
        self.sort_by_ranking_score = sort_by_ranking_score
        self.number_of_recommendations = number_of_recommendations
        self.similarity_concept = similarity_concept
        self.nlp_model_loader = nlp_model_loader

    def set_similarity_weight(self, weight):
        self.similarity_weight = weight

    def set_interaction_weight(self, weight):
        self.interaction_weight = weight

    def calculate_interaction_score(self, status_df):
        """Function to calculate the interaction score of a status."""

        # Calculate the interaction score
        status_df["interaction_score"] = (
            status_df["favourites_count"] + status_df["replies_count"] + status_df["reblogs_count"]
        )

        # Normalize the interaction score to the value range [0, 1]
        max_interaction_score = status_df["interaction_score"].max()
        status_df["interaction_score"] = status_df["interaction_score"] / max_interaction_score

        return status_df

    def calculate_ranking_score(self, status_df):
        """Function to calculate the ranking score of a status."""

        # Calculate the ranking score
        status_df["ranking_score"] = (self.similarity_weight * status_df["cosine_sim"]) + (
            self.interaction_weight * status_df["interaction_score"]
        )

        if self.sort_by_ranking_score:
            # Sort the DataFrame according to the ranking score (descending)
            status_df.sort_values("ranking_score", ascending=False, inplace=True)
            status_df.reset_index(drop=True, inplace=True)

        return status_df

    def get_recommendations_with_ranking_system(self, account_id):
        if self.similarity_concept == "tfidf":
            tfidf_recommender = TFIDFRecommender(self.number_of_recommendations, self.nlp_model_loader)
            recommendations_for_account = tfidf_recommender.recommend_statuses_from_follower(account_id)
        elif self.similarity_concept == "spacy":
            recommendations_for_account = recommend_with_spacy_for_account(account_id, self.number_of_recommendations)
        else:
            raise ValueError(f"Invalid similarity concept: {self.similarity_concept}")

        # transform recommendations_for_account to a DataFrame
        recommendations_for_account_df = pd.DataFrame(recommendations_for_account)

        # Calculate the interaction score and expand the DataFrame
        recommendations_for_account_df = self.calculate_interaction_score(recommendations_for_account_df)

        # Calculate the ranking score, expand the DataFrame and sort the DataFrame by ranking score
        recommendations_with_ranking = self.calculate_ranking_score(recommendations_for_account_df)

        return recommendations_with_ranking.to_dict(orient="records")
