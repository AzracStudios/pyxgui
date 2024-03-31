from pyxgui.lang.lib.lexer import Lexer
from pyxgui.lang.lib.token import Token, TokenType
from pyxgui.lang.lib.error import Error


def generate_next_token(self: Lexer) -> Token | Error:
  if self.current_char is None:
    return Token(TokenType.WHITESPACE, self.position.copy())

  if self.current_char in "\n\t ":
    return Token(TokenType.WHITESPACE, self.position.copy())

  if self.current_char == "<":
    return Token(TokenType.LANGLE, self.position.copy())

  if self.current_char == ">":
    return Token(TokenType.RANGLE, self.position.copy())

  if self.current_char == "/":
    return Token(TokenType.FWDSLSH, self.position.copy())

  if self.current_char == "=":
    return Token(TokenType.EQL, self.position.copy())

  if self.current_char in "\"'":
    return self.lex_string()

  if self.current_char in "01234567890.":
    return self.lex_number()

  return self.lex_word()


class XMLLexer(Lexer):

  def __init__(self, source: str) -> None:
    super().__init__(source, generate_next_token)
