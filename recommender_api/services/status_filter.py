from collections import defaultdict

class StatusFilter:
    """Class which provides functions to filter statuses based on a ranking score threshold or author diversity."""

    def __init__(self, number_of_allowed_status_from_same_account = 3, ranking_score_threshold = -1.0):
        self.number_of_allowed_status_from_same_account = number_of_allowed_status_from_same_account
        self.ranking_score_threshold = ranking_score_threshold
    
    def filter_statuses_by_threshold(self, ranked_statuses):
        """Function to filter out statuses with a lower ranking score than the threshold.
        param ranked_statuses: A list of statuses with ranking score.
        param ranking_score_threshold: The threshold for the ranking score. Statuses with a lower ranking score will be filtered out.
        return: A list of statuses with ranking score higher than the threshold.
        """
        filtered_statuses = [status for status in ranked_statuses if status["ranking_score"] > self.ranking_score_threshold]
        return filtered_statuses

    def promote_author_diversity(self, statuses):
        """Function which promotes author diversity by allowing only a limited number of statuses from the same account on the same day.
        param statuses: A list of statuses with ranking score.
        param number_of_allowed_status_from_same_account: The number of statuses from the same account that are allowed.
        return: A list of statuses with ranking score."""

        filtered_statuses = []
        date_statuses = defaultdict(list)
        for status in statuses:
            date = status['created_at'].date()
            date_statuses[date].append(status)
        for date, statuses in date_statuses.items():
            statuses.sort(key=lambda x: x['ranking_score'], reverse=True)
            authors = defaultdict(int)
            for status in statuses:
                if authors[status['account_id']] < self.number_of_allowed_status_from_same_account:
                    filtered_statuses.append(status)
                    authors[status['account_id']] += 1
        return filtered_statuses

