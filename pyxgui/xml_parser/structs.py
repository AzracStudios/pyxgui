from __future__ import annotations


class Position:

  def __init__(self, idx: int, col: int, ln: int, fsrc: str) -> None:
    self.idx = idx
    self.col = col
    self.ln = ln
    self.fsrc = fsrc

  def advance(self, char: str | None = None) -> Position:
    self.idx += 1
    self.col += 1

    if char == "\n":
      self.ln += 1
      self.col = 0

    return self

  def revert(self, char: str | None = None) -> Position:
    self.idx -= 1
    self.col -= 1

    if char == "\n":
      self.ln -= 1
      self.col += 1

  def copy(self) -> Position:
    return Position(self.idx, self.col, self.ln, self.fsrc)

  def __repr__(self) -> str:
    return f"Ln {self.ln}, Col {self.col}"


class Token:

  def __init__(
      self,
      tok_type: str,
      start_pos: Position,
      value: str | None = None,
      end_pos: Position | None = None,
  ) -> None:
    self.type = tok_type
    self.value = value
    self.start_pos = start_pos
    self.end_pos = self.start_pos.copy().advance() if not end_pos else end_pos

  def __repr__(self) -> str:
    return f"[{self.type}{f':{self.value}' if self.value else ''}]"


class XMLAttribute:

  def __init__(self):
    self.key: str | None = None
    self.value: str | float | None = None

  def __repr__(self) -> str:
    return f"[{self.key}:{self.value}]"


class XMLNode:

  def __init__(
      self,
      parent: XMLNode | None,
  ):
    self.tag: str | None = None
    self.inner_text: str = ""
    self.parent = parent
    self.attributes: list[XMLAttribute] = []
    self.children: list[XMLNode] = []

  def __repr__(self) -> str:
    return f"{self.tag}: {self.inner_text}" + (
        f" attrs:{', '.join([str(attr) for attr in self.attributes])}"
        if self.attributes
        else ""
    )
