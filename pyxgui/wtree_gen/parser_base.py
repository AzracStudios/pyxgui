from pyxgui.wtree_gen.structs import Token
import pyxgui.wtree_gen.constants as const
from pyxgui.wtree_gen.error import Error, ParserError

class Parser:

  def __init__(self, source: str, tokens: list[Token]):
    self.tokens = tokens
    self.current_token: Token | None = None
    self.source = source
    self.tok_idx = -1
    self.advance()

  def advance(self, advance_by: int = 1) -> None:
    self.tok_idx += advance_by
    if self.tok_idx < len(self.tokens):
      self.current_token = self.tokens[self.tok_idx]

    return None

  def peek_tokens(self, peek_by: int) -> Token | None:
    if (i := self.tok_idx + peek_by) < len(self.tokens):
      return self.tokens[i]
    return None

  def skip(self, to_skip: list[str]) -> None:
    while self.current_token.type in to_skip:
      self.advance()
    return None
