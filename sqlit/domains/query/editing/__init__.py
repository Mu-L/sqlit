"""Editing helpers for query text."""

from .deletion import EditResult
from .deletion import delete_all
from .deletion import delete_char
from .deletion import delete_char_back
from .deletion import delete_line
from .deletion import delete_line_end
from .deletion import delete_line_start
from .deletion import delete_to_end
from .deletion import delete_word
from .deletion import delete_word_back
from .deletion import delete_word_end

__all__ = [
    "EditResult",
    "delete_all",
    "delete_char",
    "delete_char_back",
    "delete_line",
    "delete_line_end",
    "delete_line_start",
    "delete_to_end",
    "delete_word",
    "delete_word_back",
    "delete_word_end",
]
