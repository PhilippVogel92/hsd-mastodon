import pandas as pd
import numpy as np
from collections import defaultdict
from recommender_api.model.status_queries import (
    get_status_with_tag_ids_and_stats_by_status_id,
)
from recommender_api.model.interest_queries import get_tags_by_account_id
from recommender_api.model.account_queries import get_followed_accounts, get_blocked_accounts, get_muted_accounts


class RankingSystem:
    """Class to create a ranking system for statuses and sort the timeline of an account."""

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
    boost_for_tags = 0.2
    boost_for_blocked = -1000

    # number of allowed statuses from the same account in the timeline, more than that will be removed
    number_of_allowed_status_from_same_account = 3

    # threshold for ranking score. If a status has a lower score, it will be removed from the timeline
    ranking_score_threshold = -1.0

    def __init__(self):
        pass

    def count_account_tags_in_status(self, status, tag_ids_from_account):
        """
        Function to check if the tags of an account are in a status.
        param status: A specific status by id with joined tag_id and stats.
        param tag_ids_from_account: A list of tag ids from an account.
        return: True if the tags of an account are in a status, else False.
        """
        number_of_status_tags_in_account_tags = 0

        for tag_id in status["tag_ids"]:
            if tag_id and tag_id in tag_ids_from_account:
                number_of_status_tags_in_account_tags += 1
                print(tag_id, "is in account tags")

        return number_of_status_tags_in_account_tags

    def check_if_author_is_followed(self, status, following_list):
        """
        Function to check if the author of a status is in the account's following list.
        param status: A specific status by id with joined tag_id and stats.
        param account_id: The id of an account.
        return: True if the author of a status is in the account's following list, else False.
        """
        is_followed = False
        author_id = status["account_id"]
        if author_id in following_list:
            is_followed = True
            print("author with id:", author_id, "is followed")
        return is_followed

    def check_if_author_is_blocked(self, status, blocked_list):
        """
        Function to check if the author of a status is in the account's blocked list.
        param status: A specific status by id with joined tag_id and stats.
        param account_id: The id of an account.
        return: True if the author of a status is in the account's blocked list, else False.
        """
        is_blocked = False
        author_id = status["account_id"]
        if author_id in blocked_list:
            is_blocked = True
            print("author with id:", author_id, "is blocked")

        return is_blocked

    def check_if_author_is_muted(self, status, muted_list):
        """
        Function to check if the author of a status is in the account's muted list.
        param status: A specific status by id with joined tag_id and stats.
        param account_id: The id of an account.
        return: True if the author of a status is in the account's muted list, else False.
        """
        is_muted = False
        author_id = status["account_id"]
        if author_id in muted_list:
            is_muted = True
            print("author with id:", author_id, "is muted")

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
        tag_ids_from_account,
        following_list,
        muted_list,
        blocked_list,
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

        # maybe this can/should be done in __init__?
        self.normalize_interaction_weights()

        # calculate weighted interaction subscores
        replies_score = self.normalize_counts(replies_count) * self.replies_weight_normalized
        favourites_score = self.normalize_counts(favourites_count) * self.favourites_weight_normalized
        reblogs_score = self.normalize_counts(reblogs_count) * self.boost_weight_normalized

        # calculate ranking score based on weighted interactions
        ranking_score = replies_score + favourites_score + reblogs_score

        # add boost if status contains followed hashtags
        if tag_ids_from_account:
            ranking_score += self.count_account_tags_in_status(status, tag_ids_from_account) * self.boost_for_tags

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

    def filter_statuses_by_threshold(self, ranked_statuses, ranking_score_threshold):
        """Function to filter out statuses with a lower ranking score than the threshold.
        param ranked_statuses: A list of statuses with ranking score.
        param ranking_score_threshold: The threshold for the ranking score. Statuses with a lower ranking score will be filtered out.
        return: A list of statuses with ranking score higher than the threshold.
        """
        filtered_statuses = [status for status in ranked_statuses if status["ranking_score"] > ranking_score_threshold]
        return filtered_statuses

    def promote_author_diversity(self, statuses, number_of_allowed_status_from_same_account):
        """Function to promote author diversity.
        param statuses: A list of statuses with ranking score.
        param number_of_allowed_status_from_same_account: The number of statuses from the same account that are allowed.
        return: A list of statuses with ranking score."""

        filtered_list = []
        date_statuses = defaultdict(list)
        for status in statuses:
            date = status['created_at'].date()
            date_statuses[date].append(status)
        for date, statuses in date_statuses.items():
            statuses.sort(key=lambda x: x['ranking_score'], reverse=True)
            authors = defaultdict(int)
            for status in statuses:
                if authors[status['account_id']] < number_of_allowed_status_from_same_account:
                    filtered_list.append(status)
                    authors[status['account_id']] += 1
        return filtered_list

    def sort_statuses_by_ranking_score(self, statuses):
        """Function to sort statuses by ranking score.
        param statuses: A list of statuses with ranking score.
        return: A list of sorted status ids by ranking score."""

        # Sort statuses by ranking score
        sorted_statuses = sorted(statuses, key=lambda x: x["ranking_score"], reverse=True)

        return sorted_statuses

    def sort_timeline(self, account_id, status_ids):
        """Function to sort the timeline of a account by ranking score.
        param account_id: The id of the account. The statuses will be sorted by the tags of the account.
        param status_ids: The ids of the statuses.
        param ranking_score_threshold: The threshold for the ranking score. Statuses with a lower ranking score will be filtered out.
        return: A list of sorted status ids by ranking score.
        """

        # Get stat,uses with tag ids and stats
        statuses_with_tag_ids_and_stats = [
            get_status_with_tag_ids_and_stats_by_status_id(status_id) for status_id in status_ids
        ]

        # Get tag ids, following list, muted list and blocked list from account
        tag_ids_from_account = get_tags_by_account_id(account_id)
        following_list = get_followed_accounts(account_id)
        muted_list = get_muted_accounts(account_id)
        blocked_list = get_blocked_accounts(account_id)

        # Calculate ranking score for each status
        ranked_statuses = [
            self.calculate_ranking_score(status, tag_ids_from_account, following_list, muted_list, blocked_list)
            for status in statuses_with_tag_ids_and_stats
        ]

        # Filter out statuses from the same account
        ranked_statuses_with_author_diversity = self.promote_author_diversity(
            ranked_statuses, self.number_of_allowed_status_from_same_account
        )

        filtered_statuses = self.filter_statuses_by_threshold(ranked_statuses_with_author_diversity, self.ranking_score_threshold)

        # Sort statuses by ranking score
        sorted_statuses = self.sort_statuses_by_ranking_score(filtered_statuses)

        sorted_statuses_ids = [status["id"] for status in sorted_statuses]

        return sorted_statuses_ids
