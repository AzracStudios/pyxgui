from __future__ import annotations

from pyxgui.lang.lib.position import Position


class Token:

  def __init__(
      self,
      tok_type: str,
      start_pos: Position,
      value: str | int | float | None = None,
      end_pos: Position | None = None,
  ) -> None:
    self.type = tok_type
    self.value = value
    self.start_pos = start_pos
    self.end_pos = self.start_pos.copy().advance() if not end_pos else end_pos
    return None

  def __repr__(self) -> str:
    return f"[{self.type}{f':{self.value}' if self.value else ''}]"


class TokenType:
  STRING = "STRING"
  WORD = "WORD"
  NUMBER = "NUMBER"
  EOF = "EOF"
  WHITESPACE = "WHITESPACE"
  LANGLE = "LANGLE"
  RANGLE = "RANGLE"
  FWDSLSH = "FWDSLSH"
  EQL = "EQL"
  