from .tfidf import TFIDFRecommender
import pandas as pd
import numpy as np
from recommender_api.model.status_queries import (
    get_status_with_tag_ids_and_stats_by_status_id,
    get_status_stats_by_status_id,
)

from recommender_api.model.tag_queries import get_tags_by_account_id


class RankingSystem:
    """Class to create a ranking system for statuses and sort the timeline of an account."""

    def __init__(self):
        pass

    def are_account_tags_in_status(self, status, tag_ids_from_account):
        """
        Function to check if the tags of an account are in a status.
        param status: A specific status by id with joined tag_id and stats.
        param tag_ids_from_account: A list of tag ids from an account.
        return: True if the tags of an account are in a status, else False.
        """
        found_status_tags_in_account_tags = False

        for tag_id in status["tag_ids"]:
            if tag_id and tag_id in tag_ids_from_account:
                found_status_tags_in_account_tags = True
                print(tag_id, "is in account tags")

        return found_status_tags_in_account_tags

    def calculate_ranking_score(
        self,
        status,
        tag_ids_from_account,
        weight_for_favourites_count=1.5,
        weight_for_replies_count=15.0,
        weight_for_reblogs_count=2.0,
        weight_for_time=1.1,
        boost_for_tags=100,
    ):
        """
        Function to calculate the ranking score of a status.

        :param status: A specific status by id with joined tag_id and stats.
        :param weight_for_favourites_count: Weight for favourites count.
        :param weight_for_replies_count: Weight for replies count.
        :param weight_for_reblogs_count: Weight for reblogs count.
        :param weight_for_time: Weight for time.
        :return: A specific status with a ranking score.

        """

        favourites_count = status["favourites_count"]
        replies_count = status["replies_count"]
        reblogs_count = status["reblogs_count"]
        updated_at = status["updated_at"]

        # calculate the time in days since the status was updated
        days_since_status_update = (pd.Timestamp.now() - updated_at).days

        # Logging for debugging
        print(
            "------- Start calculating ranking score for status:",
            status["id"],
            "-------",
        )
        print("Days since status update:", days_since_status_update)
        print("Favourites count:", favourites_count)
        print("Replies count:", replies_count)
        print("Reblogs count:", reblogs_count)
        print("Tags in account:", tag_ids_from_account)
        print("Tags in status:", status["tag_ids"])

        interaction_weight = 1

        # Check if the status has any interactions
        if replies_count and reblogs_count and favourites_count:
            # Prevent log(0) error
            if replies_count != 0 or reblogs_count != 0 or favourites_count != 0:
                interaction_weight = np.log(
                    weight_for_replies_count * replies_count
                    + weight_for_favourites_count * favourites_count
                    + weight_for_reblogs_count * reblogs_count
                )

        print("Interaktion_weight:", interaction_weight)

        # Calculation of ranking score with a log function
        ranking_score = interaction_weight * (
            1 / (np.log(weight_for_time * (days_since_status_update + 1)))
        )

        # Flat boost for tags in account if the account has minimum one tag
        if tag_ids_from_account and self.are_account_tags_in_status(
            status, tag_ids_from_account
        ):
            ranking_score = ranking_score + boost_for_tags
            print("Status boosted because of tags in account.")

        # Add ranking score to status
        status["ranking_score"] = ranking_score

        print("Status with ranking score:", status)
        print("------- End calculating ranking score for status -------")
        return status

    def sort_timeline(
        self, account_id, status_ids, nlp_model_loader, number_of_recommendations=20
    ):
        """Function to sort the timeline of a account by ranking score.
        param account_id: The id of the account.
        param status_ids: The ids of the statuses.
        param nlp_model_loader: The nlp model loader.
        param number_of_recommendations: The number of recommendations.
        return: A list of sorted status ids by ranking score.
        """

        # Mock Data
        status_ids = [
            "110589714508600527",
            "110594975367510259",
            "110595013146537691",
            "110611101938508635",
        ]

        # Get statuses with tag ids and stats
        statuses_with_tag_ids_and_stats = [
            get_status_with_tag_ids_and_stats_by_status_id(status_id)
            for status_id in status_ids
        ]

        # Set Limit of recommendations
        statuses_with_tag_ids_and_stats = statuses_with_tag_ids_and_stats[
            :number_of_recommendations
        ]

        # Get tag ids from account
        tag_ids_from_account = get_tags_by_account_id(account_id)

        # Calculate ranking score for each status
        ranked_statuses = [
            self.calculate_ranking_score(status, tag_ids_from_account)
            for status in statuses_with_tag_ids_and_stats
        ]

        # Sort statuses by ranking score
        sorted_statuses = sorted(
            ranked_statuses, key=lambda x: x["ranking_score"], reverse=True
        )

        # Get status ids from sorted statuses
        sorted_statuses_ids = [status["id"] for status in sorted_statuses]

        """ 
        # Example usage of the TFIDFRecommender
        tfidf_recommender = TFIDFRecommender(number_of_recommendations, nlp_model_loader)
        recommendations_for_account = tfidf_recommender.recommend_statuses_from_follower(account_id)
        """

        return sorted_statuses_ids
