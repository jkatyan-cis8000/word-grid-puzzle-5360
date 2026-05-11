"""Type definitions for the word grid puzzle game."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class Difficulty(Enum):
    """Difficulty levels for puzzle categories."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class Color(Enum):
    """Colors corresponding to difficulty levels."""
    YELLOW = "yellow"  # Easy
    GREEN = "green"    # Medium
    BLUE = "blue"      # Hard
    PURPLE = "purple"  # Expert


@dataclass(frozen=True)
class Word:
    """A single word in the puzzle."""
    text: str


@dataclass(frozen=True)
class Category:
    """A category that groups words together."""
    name: str
    description: str
    difficulty: Difficulty
    color: Color


@dataclass(frozen=True)
class Puzzle:
    """A complete puzzle with words and categories."""
    id: str
    date: str
    words: List[Word]
    categories: List[Category]


@dataclass(frozen=True)
class Group:
    """A selected group of words."""
    words: Tuple[Word, ...]
    category: Category | None = None


@dataclass(frozen=True)
class GameState:
    """The current state of a game session."""
    puzzle_id: str
    selected_words: Tuple[Word, ...]
    found_groups: List[Group]
    mistakes: int
    max_mistakes: int = 4
