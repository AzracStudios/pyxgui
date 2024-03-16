from pyxgui.wtree_gen.lexer_base import *


class XMLLexer(Lexer):

  def __init__(self, source: str) -> None:
    super().__init__(source, self.generate_next_token)

  def lex_word(self) -> Token:
    word: str = ""
    start_pos: Position = self.position.copy()

    while self.current_char not in " \t\n<>/=":
      word += self.current_char
      self.advance()

    self.revert()
    return Token(
        const.TT_WORD, start_pos, value=word, end_pos=self.position.copy().advance()
    )

  def generate_next_token(self) -> Token | Error:
    if self.current_char in "\t ":
      return Token(const.TT_SPACE, self.position.copy())

    if self.current_char == "\n":
      return Token(const.TT_NL, self.position.copy())

    if self.current_char == "<":
      return Token(const.TT_LANGLE, self.position.copy())

    if self.current_char == ">":
      return Token(const.TT_RANGLE, self.position.copy())

    if self.current_char == "/":
      return Token(const.TT_FWDSLSH, self.position.copy())

    if self.current_char == "=":
      return Token(const.TT_EQL, self.position.copy())

    if self.current_char in "\"'":
      return self.lex_string()

    if self.current_char in const.NUMS + ".":
      return self.lex_number()

    return self.lex_word()
