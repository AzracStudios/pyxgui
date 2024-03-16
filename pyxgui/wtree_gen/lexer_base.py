from pyxgui.wtree_gen.structs import Token, Position
import pyxgui.wtree_gen.constants as const
from pyxgui.wtree_gen.error import Error, LexerError


class Lexer:

  def __init__(self, source: str, generate_next_token) -> None:
    self.source: str = source
    self.current_char: str | None = None
    self.position: Position = Position(-1, -1, 1, self.source)
    self.advance()
    self.generate_next_token = generate_next_token

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
    quote: str = self.current_char

    self.advance()

    string = ""
    while self.current_char not in (None, quote):
      string += self.current_char
      self.advance()

    if self.current_char != quote:
      return LexerError(
          "Unterminated String Literal",
          self.source,
          start_pos,
          self.position.copy().advance(),
      )

    return Token(const.TT_STRING, start_pos, value=string, end_pos=self.position.copy())

  def lex_number(self) -> Token | Error:
    start_pos: Position = self.position.copy()
    num_str: str = ""
    dot_count: int = 0

    while self.current_char in const.NUMS + ".":
      if self.current_char == ".":
        dot_count += 1

      num_str += self.current_char
      self.advance()

    if dot_count > 1:
      return LexerError(
          f"Invalid Number {num_str}", self.source, start_pos, self.position.copy()
      )

    self.revert()

    return Token(
        const.TT_NUMBER,
        start_pos,
        value=(float(num_str) if dot_count else int(num_str)),
        end_pos=self.position.copy(),
    )


  def tokenize(self) -> list[Token] | None:
    tokens = []

    while self.current_char:
      token_or_error = self.generate_next_token()
      if isinstance(token_or_error, Error):
        print(token_or_error.generate_error_text())
        return None

      tokens.append(token_or_error)
      self.advance()

    tokens.append(Token(const.TT_EOF, self.position.copy()))

    # pop spaces and new lines from head
    while True:
      if tokens[0].type in (const.TT_SPACE, const.TT_NL):
        tokens.pop(0)
        continue
      break

    return tokens
