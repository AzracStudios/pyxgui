"""
Provides a structure for position
Holds index, column and line
"""

from __future__ import annotations


class Position:
  """
  Structure for position
  """

  def __init__(self, idx: int, col: int, ln: int) -> None:
    self.idx: int = idx
    self.col: int = col
    self.ln: int = ln

  def advance(self, character: str | None = None) -> None:
    """
    Advances the position based on current character

    Args:
        character (str | None, optional): _description_. Defaults to None.
    """
    self.idx += 1
    self.col += 1

    if character == "\n":
      self.col = 0
      self.ln += 1

  def copy(self) -> Position:
    """
    Returns:
        Position
    """
    return Position(self.idx, self.col, self.ln)
