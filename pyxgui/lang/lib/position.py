from __future__ import annotations


class Position:

  def __init__(self, idx: int, col: int, ln: int, fsrc: str) -> None:
    self.idx = idx
    self.col = col
    self.ln = ln
    self.fsrc = fsrc
    return None

  def advance(self, char: str | None = None) -> Position:
    self.idx += 1
    self.col += 1

    if char == "\n":
      self.ln += 1
      self.col = 0

    return self

  def revert(self) -> Position:
    self.idx -= 1
    self.col -= 1

    return self

  def copy(self) -> Position:
    return Position(self.idx, self.col, self.ln, self.fsrc)

  def __repr__(self) -> str:
    return f"Ln {self.ln}, Col {self.col}"
