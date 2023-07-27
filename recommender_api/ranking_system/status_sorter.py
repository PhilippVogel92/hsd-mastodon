class StatusSorter:
    """Class to sort statuses by ranking score."""
    
    def sort_statuses_by_ranking_score(self, statuses):
        """Function to sort statuses by ranking score.
        param statuses: A list of statuses with ranking score.
        return: A list of sorted status ids by ranking score."""

        # Sort statuses by ranking score
        sorted_statuses = sorted(statuses, key=lambda x: x["ranking_score"], reverse=True)
        
        return sorted_statuses
