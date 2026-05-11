"""Config layer for the puzzle game."""

from __future__ import annotations

from src.types import Difficulty, Color

# Puzzle dimensions
GRID_SIZE = 4
WORDS_PER_PUZZLE = GRID_SIZE * GRID_SIZE
WORDS_PER_GROUP = 4
MAX_MISTAKES = 4

# Difficulty configuration
DIFFICULTY_LEVELS = {
    Difficulty.EASY: Color.YELLOW,
    Difficulty.MEDIUM: Color.GREEN,
    Difficulty.HARD: Color.BLUE,
    Difficulty.EXPERT: Color.PURPLE,
}

DIFFICULTY_ORDER = [
    Difficulty.EASY,
    Difficulty.MEDIUM,
    Difficulty.HARD,
    Difficulty.EXPERT,
]

# Default puzzle data (fallback)
DEFAULT_DAILY_PUZZLES = {
    "2024-01-01": {
        "id": "puzzle-001",
        "date": "2024-01-01",
        "words": [
            "HAWK", "FALCON", "EAGLE", "HARRIER",
            "TIGER", "LION", "CHEETAH", "LEOPARD",
            "JUPITER", "MARS", "VENUS", "SATURN",
            "OAK", "PINE", "MAPLE", "BIRCH"
        ],
        "categories": [
            {"name": "Birds of Prey", "description": "Raptors", "difficulty": "easy", "color": "yellow"},
            {"name": "Big Cats", "description": "Feline predators", "difficulty": "easy", "color": "yellow"},
            {"name": "Planets", "description": "In our solar system", "difficulty": "medium", "color": "green"},
            {"name": "Trees", "description": "Woody plants", "difficulty": "medium", "color": "green"}
        ]
    }
}
