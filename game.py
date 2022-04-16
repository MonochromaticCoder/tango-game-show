"""Game show module"""

import random
from typing import Dict, Set
from abc import ABC, abstractmethod
from analytics import Analytics


class Player(ABC):
    """Class representing a player in the game show"""
    @abstractmethod
    def update_knowledge(self, briefcase_id: int,
                         is_winning_briefcase: bool) -> None:
        """Updates the knowledge of the player about a briefcase"""

    @abstractmethod
    def pick(self) -> int:
        """Returns the choice of briefcase."""

    @abstractmethod
    def want_to_reconsider(self) -> bool:
        """Returns whether or not the player wants to pick again."""


class NoSwitchPlayer(Player):
    """A player that doesn't switch"""
    def __init__(self, briefcase_ids: Set[int]) -> None:
        self._briefcase_ids = briefcase_ids

    def update_knowledge(self, briefcase_id: int,
                         is_winning_briefcase: bool) -> None:
        pass

    def pick(self) -> int:
        return random.choice(tuple(self._briefcase_ids))

    def want_to_reconsider(self) -> bool:
        return False


class SwitchPlayer(Player):
    """A player that switches"""
    def __init__(self, briefcase_ids: Set[int]) -> None:
        self._briefcase_ids = briefcase_ids
        self._knowledge: Dict[int, bool] = {}

    def update_knowledge(self, briefcase_id: int,
                         is_winning_briefcase: bool) -> None:
        self._knowledge[briefcase_id] = is_winning_briefcase

    def pick(self) -> int:
        winning_briefcases = tuple(i for i in self._briefcase_ids
                                   if self._knowledge.get(i, False))
        if winning_briefcases:
            return random.choice(winning_briefcases)
        return random.choice(
            tuple(i for i in self._briefcase_ids if i not in self._knowledge))

    def want_to_reconsider(self) -> bool:
        return True


class GameConfiguration:
    """Class representing a configuration of the game"""
    def __init__(self, num_empty_briefcases: int,
                 num_winning_briefcases: int) -> None:
        self._briefcases = ([False] * num_empty_briefcases) + (
            [True] * num_winning_briefcases)
        random.shuffle(self._briefcases)

    def is_winning_briefcase(self, i: int) -> bool:
        """Returns whether or not the i-th briefcase is a winning one"""
        if i < 0 or i >= len(self._briefcases):
            raise ValueError("Invalid briefcase index")
        return self._briefcases[i]

    def briefcase_ids(self) -> Set[int]:
        """Returns the set of briefcase ids"""
        return set(range(len(self._briefcases)))


class Game:
    """Runs the game"""
    def __init__(self, idx: int, config: GameConfiguration, player: Player,
                 analytics: Analytics):
        self._id = idx
        self._config = config
        self._player = player
        self._analytics = analytics

    def run(self) -> bool:
        """Runs the game and returns whether or not the player won"""
        # PLayer picks a briefcase
        choice = self._player.pick()
        # Host reveals a different and non-winning briefcase
        reveal = random.choice(
            tuple(i for i in self._config.briefcase_ids()
                  if i != choice and not self._config.is_winning_briefcase(i)))
        self._player.update_knowledge(reveal, False)
        # Give the player a chance to reconsider
        if self._player.want_to_reconsider():
            self._analytics.log_reconsider(self._id)
            choice = self._player.pick()
        # Reveal the final choice
        result = self._config.is_winning_briefcase(choice)
        self._analytics.log_result(self._id, result)
        return result
