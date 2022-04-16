"""Driver code to run simulations"""

from collections import Counter
import random
from analytics import Analytics
from game import Game, GameConfiguration, SwitchPlayer, NoSwitchPlayer

if __name__ == "__main__":
    analytics = Analytics()

    def simulate_game(game_id: int) -> None:
        """Simulate a game with the standard configuration"""
        config = GameConfiguration(2, 1)
        Game(
            game_id, config,
            random.choice(
                (NoSwitchPlayer, SwitchPlayer))(config.briefcase_ids()),
            analytics).run()

    for i in range(2000):
        simulate_game(i)

    results = analytics.get_results()

    switch_results = Counter(x.player_won for x in results.values()
                             if x.player_reconsidered)
    no_switch_results = Counter(x.player_won for x in results.values()
                                if not x.player_reconsidered)

    print(
        f"Players who reconsidered won {switch_results[True]}/{sum(switch_results.values())} ({switch_results[True] / sum(switch_results.values()) * 100}%) times"
    )
    print(
        f"Players who didn't reconsider won {no_switch_results[True]}/{sum(no_switch_results.values())} ({no_switch_results[True] / sum(no_switch_results.values()) * 100}%) times"
    )
