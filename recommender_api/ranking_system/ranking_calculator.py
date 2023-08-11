import pandas as pd
import numpy as np

class RankingCalculator:
    """ Calculates the ranking score of a given status for a specific account."""

    # if we might gain more users, we can scale the ranking score with this factor
    # low values cause higher variance on low interaction counts
    scalibility_factor = 1.0

    # interaction weights: set to whatever feels right. Will be normalized anyway ;)
    replies_weight = 3.0
    favourites_weight = 2.0
    reblogs_weight = 1.0

    # Not normalized. Higher values cause a higher loss in ranking score over time
    age_weight = 0.3

    # normalized interaction weights
    replies_weight_normalized = 0.0
    favourites_weight_normalized = 0.0
    boost_weight_normalized = 0.0

    # flat boosts added to ranking score, if they apply
    boost_for_following = 0.2
    boost_for_interests = 0.2
    boost_for_blocked = -1000
    
    def count_account_interests_in_status(self, status, interest_ids_from_account):
        """
        Function to check if the interests of an account are in a status.
        param status: A specific status by id with joined interest_id and stats.
        param interest_ids_from_account: A list of interest ids from an account.
        return: True if the interests of an account are in a status, else False.
        """
        number_of_status_interests_in_account_interests = 0

        for interest_id in status["interest_ids"]:
            if interest_id and interest_id in interest_ids_from_account:
                number_of_status_interests_in_account_interests += 1

        return number_of_status_interests_in_account_interests

    def check_if_author_is_followed(self, status, following_list):
        """
        Function to check if the author of a status is in the account's following list.
        param status: A specific status by id with joined interest_id and stats.
        param account_id: The id of an account.
        return: True if the author of a status is in the account's following list, else False.
        """
        is_followed = False
        author_id = status["account_id"]
        if author_id in following_list:
            is_followed = True

        return is_followed

    def check_if_author_is_blocked(self, status, blocked_list):
        """
        Function to check if the author of a status is in the account's blocked list.
        param status: A specific status by id with joined interest_id and stats.
        param account_id: The id of an account.
        return: True if the author of a status is in the account's blocked list, else False.
        """
        is_blocked = False
        author_id = status["account_id"]
        if author_id in blocked_list:
            is_blocked = True

        return is_blocked

    def check_if_author_is_muted(self, status, muted_list):
        """
        Function to check if the author of a status is in the account's muted list.
        param status: A specific status by id with joined interest_id and stats.
        param account_id: The id of an account.
        return: True if the author of a status is in the account's muted list, else False.
        """
        is_muted = False
        author_id = status["account_id"]
        if author_id in muted_list:
            is_muted = True

        return is_muted

    def normalize_counts(self, count):
        if count is None:
            count = 0
        return 1 - (1 / (1 + np.log1p(count / self.scalibility_factor)))

    def normalize_age(self, count):
        return 1 / (1 + np.log1p(count * self.age_weight))

    def normalize_interaction_weights(self):
        # Calculate the sum of the input values
        weight_sum = self.replies_weight + self.favourites_weight + self.reblogs_weight

        # Scale the values proportionally
        self.replies_weight_normalized = self.replies_weight / weight_sum
        self.favourites_weight_normalized = self.favourites_weight / weight_sum
        self.boost_weight_normalized = self.reblogs_weight / weight_sum
    
    
    def calculate_ranking_score(
        self,
        status,
        interest_ids_from_account,
        following_list,
        muted_list,
        blocked_list,
    ):
        """
        Function to calculate the ranking score of a status.

        :param status: A specific status by id with joined interest_id and stats.
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

        # maybe this can/should be done in __init__?
        self.normalize_interaction_weights()

        # calculate weighted interaction subscores
        replies_score = self.normalize_counts(replies_count) * self.replies_weight_normalized
        favourites_score = self.normalize_counts(favourites_count) * self.favourites_weight_normalized
        reblogs_score = self.normalize_counts(reblogs_count) * self.boost_weight_normalized

        # calculate ranking score based on weighted interactions
        ranking_score = replies_score + favourites_score + reblogs_score

        # add boost if status contains followed interests
        if interest_ids_from_account:
            ranking_score += self.count_account_interests_in_status(status, interest_ids_from_account) * self.boost_for_interests

        # add boost if user follows th status author
        if self.check_if_author_is_followed(status, following_list):
            ranking_score += self.boost_for_following

        # surpress blocked or muted authors
        if self.check_if_author_is_blocked(status, blocked_list) or self.check_if_author_is_muted(status, muted_list):
            ranking_score += self.boost_for_blocked

        # calculate age score
        age_score = self.normalize_age(days_since_status_update)

        # calculate final ranking score based on age of the status
        ranking_score = ranking_score * age_score

        # Add ranking score to status
        status["ranking_score"] = ranking_score

        return status