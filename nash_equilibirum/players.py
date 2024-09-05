from config import *
from config import ADAPT_INITIAL_ACCEPT_CHANCE, ADAPT_PENALTY
import random
import unittest


class Player:
    def __init__(self, player_type):
        self.player_type = player_type
        self.score = 0
        self.trades_made = 0
        self.successful_trades = 0
        self.times_scammed = 0
        self.times_scammed_others = 0
        self.scammed_by = set()

    def decide_to_trade(self, other_player):
        raise NotImplementedError("Subclass must implement abstract method")

    def update_score(self, points):
        self.score += points
        self.trades_made += 1
        if points > 0:
            self.successful_trades += 1

    def get_scammed(self, other_player):
        self.times_scammed += 1
        self.scammed_by.add(other_player)

    def scam_other(self):
        self.times_scammed_others += 1

    def get_stats(self):
        return {
            "type": self.player_type,
            "score": self.score,
            "trades_made": self.trades_made,
            "successful_trades": self.successful_trades,
            "times_scammed": self.times_scammed,
            "times_scammed_others": self.times_scammed_others
        }

class NaivePlayer(Player):
    def __init__(self):
        super().__init__("NAIVE")

    def decide_to_trade(self, other_player):
        return random.random() < NAIVE_ACCEPT_CHANCE



class AdaptPlayer(Player):
    def __init__(self):
        super().__init__("ADAPT")
        self.trust_level = ADAPT_INITIAL_ACCEPT_CHANCE

    def decide_to_trade(self, other_player):
        return random.random() < self.trust_level

    def get_scammed(self, other_player):
        super().get_scammed(other_player)
        self.trust_level = max(0, self.trust_level - ADAPT_PENALTY)



class BadPlayer(Player):
    def __init__(self):
        super().__init__("BAD")

    def decide_to_trade(self, other_player):
        return True  # Always agrees to trade

    def scam_attempt(self):
        return random.random() < BAD_SCAM_CHANCE

def create_player(player_type):
    if player_type == "NAIVE":
        return NaivePlayer()
    elif player_type == "ADAPT":
        return AdaptPlayer()
    elif player_type == "BAD":
        return BadPlayer()
    else:
        raise ValueError(f"Unknown player type: {player_type}")

def create_initial_population(population_size):
    population = []
    for _ in range(population_size):
        player_type = random.choices(PLAYER_TYPES, weights=list(INITIAL_TYPE_DISTRIBUTION.values()))[0]
        population.append(create_player(player_type))
    return population