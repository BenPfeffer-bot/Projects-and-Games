"""Game settings and core mechanics"""
from config import *
from players import create_initial_population,create_player, Player, BadPlayer, NaivePlayer, AdaptPlayer
import random

from config import *
from players import create_initial_population

class Settings:
    """This class serves as the settings and core mechanics of the game"""
    def __init__(self, population_size=INITIAL_POPULATION_SIZE):
        """
        Initialize the game settings.
        """
        self.population_size = population_size
        self.players = []
        self.round_number = 0
        self.initialize_population()
    
    
    def initialize_population(self):
        """
        Create a population of players with the initial type distribution.
        """
        self.players = create_initial_population(self.population_size)
    
    
    def make_trade(self, player1: Player, player2: Player):
        """
        Compute the trading system between two players
        """
        try:
            player1_decision = player1.decide_to_trade(player2)
            player2_decision = player2.decide_to_trade(player1)
            
            if player1_decision and player2_decision:
                if isinstance(player1, BadPlayer) and player1.scam_attempt():
                    player1.update_score(DEFECT_SCORE)
                    player1.scam_other()
                    player2.get_scammed(player1)
                elif isinstance(player2, BadPlayer) and player2.scam_attempt():
                    player2.update_score(DEFECT_SCORE)
                    player2.scam_other()
                    player1.get_scammed(player2)
                else:
                    player1.update_score(COOPERATE_SCORE)
                    player2.update_score(COOPERATE_SCORE)
            else:
                player1.update_score(NO_TRADE_SCORE)
                player2.update_score(NO_TRADE_SCORE)
        except Exception as e:
            print(f"Error in make_trade: {e}")
            print(f"Player 1: {type(player1).__name__}, Player 2: {type(player2).__name__}")
            raise

    def run_round(self):
        """
        Run a single round of the game
        """
        self.round_number += 1
        random.shuffle(self.players)
        for i in range(0, len(self.players), 2):
            if i + 1 < len(self.players):
                self.make_trade(self.players[i], self.players[i + 1])

        self.apply_evolution()

    def apply_evolution(self):
        """
        Apply evolutionary mechanisms: elimination, reproduction, and mutation
        """
        # Sort players by score
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)

        # Eliminate bottom performers
        elimination_count = int(self.population_size * ELIMINATION_THRESHOLD)
        self.players = sorted_players[:-elimination_count]

        # Reproduce top performers
        reproduction_count = int(self.population_size * REPRODUCTION_RATE)
        for _ in range(reproduction_count):
            parent = random.choice(sorted_players[:int(self.population_size/2)])
            child = create_player(parent.player_type)
            self.players.append(child)

        # Apply mutations
        for player in self.players:
            if random.random() < MUTATION_RATE:
                new_type = random.choice(PLAYER_TYPES)
                player.__class__ = eval(f"{new_type.capitalize()}Player")
                player.player_type = new_type

    def run_game(self, num_rounds):
        """
        Run the game for a specified number of rounds
        """
        for _ in range(num_rounds):
            self.run_round()

    def get_results(self):
        """
        Calculate and return the results of the game
        """
        results = {player_type: {"count": 0, "total_score": 0} for player_type in PLAYER_TYPES}

        for player in self.players:
            results[player.player_type]["count"] += 1
            results[player.player_type]["total_score"] += player.score

        for player_type in results:
            if results[player_type]["count"] > 0:
                results[player_type]["average_score"] = results[player_type]["total_score"] / results[player_type]["count"]
            else:
                results[player_type]["average_score"] = 0

        return results

    def get_detailed_stats(self):
        """
        Return detailed statistics about the current game state
        """
        stats = self.get_results()
        for player_type in PLAYER_TYPES:
            type_players = [p for p in self.players if p.player_type == player_type]
            if type_players:
                stats[player_type].update({
                    "avg_trades": sum(p.trades_made for p in type_players) / len(type_players),
                    "avg_successful_trades": sum(p.successful_trades for p in type_players) / len(type_players),
                    "avg_times_scammed": sum(p.times_scammed for p in type_players) / len(type_players),
                    "avg_times_scammed_others": sum(p.times_scammed_others for p in type_players) / len(type_players),
                })
        
        stats["round_number"] = self.round_number
        stats["total_players"] = len(self.players)
        
        return stats

# Example usage
if __name__ == "__main__":
    game = Settings(population_size=INITIAL_POPULATION_SIZE)
    game.run_game(num_rounds=DEFAULT_ROUNDS)
    results = game.get_detailed_stats()
    print("Game Results:")
    for player_type, data in results.items():
        if player_type in PLAYER_TYPES:
            print(f"{player_type}:")
            for key, value in data.items():
                print(f"  {key}: {value:.2f}")
    print(f"Total Rounds: {results['round_number']}")
    print(f"Total Players: {results['total_players']}")