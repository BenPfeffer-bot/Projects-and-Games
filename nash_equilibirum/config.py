# Game Rules
INITIAL_POPULATION_SIZE = 100
DEFAULT_ROUNDS = 1000

# Player Types
PLAYER_TYPES = ["NAIVE", "ADAPT", "BAD"]
INITIAL_TYPE_DISTRIBUTION = {
    "NAIVE": 0.33,
    "ADAPT": 0.33,
    "BAD": 0.34
}

# Scoring
COOPERATE_SCORE = 1
DEFECT_SCORE = 2
NO_TRADE_SCORE = 0

# Trading Rules
NAIVE_ACCEPT_CHANCE = 1.0  # Always accepts
ADAPT_INITIAL_ACCEPT_CHANCE = 0.8
ADAPT_PENALTY = 0.1  # Reduces accept chance after being scammed
BAD_SCAM_CHANCE = 0.7

# Visualization
COLORS = {
    "NAIVE": "#3498db",  # Blue
    "ADAPT": "#2ecc71",  # Green
    "BAD": "#e74c3c"     # Red
}

# GUI Settings
WINDOW_SIZE = "1000x800"
CHART_UPDATE_INTERVAL = 10  # Update charts every 10 rounds
STATS_UPDATE_INTERVAL = 1   # Update text stats every round

# Performance
SIMULATION_SPEED = 0.01  # Delay between rounds in seconds

# Advanced Settings
MUTATION_RATE = 0.01  # Chance for a player to randomly change type
REPRODUCTION_RATE = 0.05  # Fraction of population replaced each round
ELIMINATION_THRESHOLD = 0.1  # Bottom 10% of scorers are at risk of elimination