from recommender_api.model.status_queries import (
    get_status_with_interest_ids_and_stats_by_status_id,
)
from recommender_api.model.interest_queries import get_interests_by_account_id
from recommender_api.model.account_queries import get_followed_accounts, get_blocked_accounts, get_muted_accounts
from recommender_api.services.status_filter import StatusFilter
from recommender_api.services.status_sorter import StatusSorter
from recommender_api.services.ranking_calculator import RankingCalculator

class RankingSystem:
    """
    A class representing the Ranking System for sorting and ranking statuses in HSD-Mastodon .

    The Ranking System uses a calculator to determine the ranking score of statuses based on
    interactions, user interests, follow relationships, and status age. It provides methods to calculate
    ranking scores, filter statuses, and sort statuses based on ranking scores.

    Attributes:
        ranking_calculator (RankingCalculator): A calculator for calculating the overall ranking score of a status.
        status_filter (StatusFilter): A filter for filtering statuses based on ranking score thresholds and author diversity.
        status_sorter (StatusSorter): A sorter for sorting statuses by ranking score.
    """

    def __init__(self):
        self.ranking_calculator = RankingCalculator()
        self.status_filter = StatusFilter()
        self.status_sorter = StatusSorter()

    def calculate_ranking_score(self, status, interest_ids_from_account, following_list, muted_list, blocked_list):
        return self.ranking_calculator.calculate_ranking_score(status, interest_ids_from_account, following_list, muted_list, blocked_list)

    def promote_author_diversity(self, statuses):
        return self.status_filter.promote_author_diversity(statuses)
    
    def filter_statuses_by_threshold(self, statuses):
        return self.status_filter.filter_statuses_by_threshold(statuses)

    def sort_statuses_by_ranking_score(self, statuses):
        return self.status_sorter.sort_statuses_by_ranking_score(statuses)

    def sort_timeline(self, account_id, status_ids):
        """Function to sort the timeline of a account by ranking score.
        param account_id: The id of the account. The statuses will be sorted by the interests of the account.
        param status_ids: The ids of the statuses.
        return: A list of sorted status ids by ranking score.
        """
        
        statuses_with_interest_ids_and_stats = [
            get_status_with_interest_ids_and_stats_by_status_id(status_id) for status_id in status_ids
        ]

        interest_ids_from_account = get_interests_by_account_id(account_id)
        following_list = get_followed_accounts(account_id)
        muted_list = get_muted_accounts(account_id)
        blocked_list = get_blocked_accounts(account_id)
        
        ranked_statuses = [
            self.calculate_ranking_score(status, interest_ids_from_account, following_list, muted_list, blocked_list) for status in statuses_with_interest_ids_and_stats
        ]

        ranked_and_filtered_statuses = self.promote_author_diversity(ranked_statuses)
        ranked_and_filtered_statuses = self.filter_statuses_by_threshold(ranked_and_filtered_statuses)
        sorted_statuses = self.sort_statuses_by_ranking_score(ranked_and_filtered_statuses)
        sorted_statuses_ids = [status["id"] for status in sorted_statuses]

        return sorted_statuses_ids




