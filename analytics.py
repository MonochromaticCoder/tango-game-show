"""Analytics module"""

from collections import defaultdict
from typing import Dict

class AnalyticsEntry:
    """Class representing the analytics entry for a game"""
    def __init__(self,
                 player_reconsidered: bool = False,
                 player_won: bool = False) -> None:
        self.player_reconsidered = player_reconsidered
        self.player_won = player_won


class Analytics:
    """Class for capturing analytics"""
    def __init__(self) -> None:
        self._results: Dict[int, AnalyticsEntry] = defaultdict(AnalyticsEntry)

    def log_reconsider(self, game_id: int) -> None:
        """Log a reconsideration event"""
        self._results[game_id].player_reconsidered = True

    def log_result(self, game_id: int, player_won: bool) -> None:
        """Log the final reuslt of a game"""
        self._results[game_id].player_won = player_won

    def get_results(self) -> Dict[int, AnalyticsEntry]:
        """Returns the results"""
        return self._results
