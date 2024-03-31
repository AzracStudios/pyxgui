from __future__ import annotations
from typing import Callable

from pyxgui.lang.lib.position import Position
from pyxgui.lang.lib.token import Token, TokenType
from pyxgui.lang.lib.error import Error, LexerError


class Lexer:

  def __init__(
      self, source: str, generate_next_token: Callable[[Lexer], Token | Error]
  ) -> None:
    self.source: str = source
    self.current_char: str | None = None
    self.position: Position = Position(-1, -1, 1, self.source)
    self.advance()
    self.generate_next_token: Callable[[Lexer], Token | Error] = generate_next_token

    return None

  def advance(self) -> None:
    self.position.advance(char=self.current_char)

    if (i := self.position.idx) < len(self.source):
      self.current_char = self.source[i]
      return None

    self.current_char = None
    return None

  def revert(self) -> None:
    self.position.revert()

    if (i := self.position.idx) > 0:
      self.current_char = self.source[i]
      return None

    self.current_char = None
    return None

  def lex_string(self) -> Token | Error:
    start_pos: Position = self.position.copy()
    quote: str | None = self.current_char

    self.advance()

    string = ""
    while True:
      if self.current_char is None or self.current_char == quote:
        break
      string += self.current_char
      self.advance()

    if self.current_char != quote:
      return LexerError(
          "Unterminated String Literal",
          self.source,
          start_pos,
          self.position.copy().advance(),
      )

    return Token(
        TokenType.STRING, start_pos, value=string, end_pos=self.position.copy()
    )

  def lex_word(self) -> Token:
    word: str = ""
    start_pos: Position = self.position.copy()

    while self.current_char and (self.current_char not in " \t\n<>/="):
      word += self.current_char
      self.advance()

    self.revert()
    return Token(
        TokenType.WORD, start_pos, value=word, end_pos=self.position.copy().advance()
    )

  def lex_number(self) -> Token | Error:
    start_pos: Position = self.position.copy()
    num_str: str = ""
    dot_count: int = 0

    while self.current_char and self.current_char in "0123456789.":
      if self.current_char == ".":
        dot_count += 1

      num_str += self.current_char
      self.advance()

    self.revert()
    if dot_count > 1:
      return Token(
          TokenType.WORD,
          start_pos,
          value=num_str,
          end_pos=self.position.copy(),
      )

    return Token(
        TokenType.NUMBER,
        start_pos,
        value=(float(num_str) if dot_count else int(num_str)),
        end_pos=self.position.copy(),
    )

  def tokenize(self) -> list[Token] | None:
    tokens = []

    while self.current_char:
      token_or_error: Token | Error = self.generate_next_token(self)

      if isinstance(token_or_error, Error):
        print(token_or_error.generate_error_text())
        return None

      tokens.append(token_or_error)
      self.advance()

    tokens.append(Token(TokenType.EOF, self.position.copy()))

    # pop spaces and new lines from head
    while True:
      if tokens[0].type == TokenType.WHITESPACE:
        tokens.pop(0)
        continue
      break

    return tokens
