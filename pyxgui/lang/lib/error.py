from pyxgui.lang.lib.position import Position
from pyxgui.lang.lib.token import Token
from pyxgui.lang.xml.node import XMLNode
from pyxgui.lib.ansi_colors import ANSIColors


class Error:

  def __init__(
      self,
      message: str,
      src: str,
      start_pos: Position,
      end_pos: Position,
      error_type: str,
      help_text: str | None = None,
  ) -> None:
    self.message: str = message
    self.src: str = src
    self.start_pos: Position = start_pos
    self.end_pos: Position = end_pos
    self.type: str = error_type
    self.help_text: str | None = help_text
    return None

  def generate_error_text(self) -> str:
    res: str = f"{ANSIColors.bright_red(f'{self.type} @ {str(self.start_pos)}')}\n"
    res += f"{ANSIColors.bright_black('> ')}{ANSIColors.red(self.message)}\n\n"
    res += self.generate_code_preview()

    if self.help_text:
      res += ANSIColors.green(
          f"\n\n{ANSIColors.bright_green('Hint:')} {ANSIColors.green(self.help_text)}"
      )

    return f"{res}"

  def generate_code_preview(self) -> str:
    result: str = ""

    # the start index will be the first reverse index of \n
    # from start position. if it doesn't exist, then it is 0
    idx_start: int = max(self.src.rfind("\n", 0, self.start_pos.idx), 0)

    # the end index will be the first \n to appear after the start index
    # if it doesn't exist, then it is the last index of source.
    idx_end: int = self.src.find("\n", idx_start + 1)
    if idx_end < 0:
      idx_end = len(self.src)

    line_count: int = self.end_pos.ln - self.start_pos.ln + 1
    if self.end_pos.ln > 1:
      line_count += 1

    for i in range(line_count):
      spaces: int = len(str(self.start_pos.ln + line_count))
      num_str: str = str(self.start_pos.ln + i)
      spaces_str: str = " " * (spaces - len(num_str) + 1)

      line_number: str = f"{num_str}{spaces_str}| "
      line: str = self.src[idx_start:idx_end].replace("\n", "")

      col_start: int = self.start_pos.col if i == 0 else 0
      col_end: int = self.end_pos.col if i == line_count - 1 else len(line) - 1

      # print the line previous to where the error starts
      if self.start_pos.ln > 1 and i == 0:
        prev_line_start = max(self.src.rfind("\n", 0, idx_start), 0)
        prev_line_end = max(self.src.find("\n", prev_line_start + 1), 0)
        prev_line = self.src[prev_line_start:prev_line_end].replace("\n", "")
        if prev_line.replace(" ", "") != "":
          result += (
              ANSIColors.bright_black(f"{self.start_pos.ln + i - 1}{spaces_str}| ")
              + self.src[prev_line_start:prev_line_end].replace("\n", "")
              + "\n"
          )

      if self.end_pos.ln < self.start_pos.ln + i:
        line = f"{ANSIColors.bright_black(line)}"
        result += ANSIColors.bright_black(line_number) + line + "\n"

      else:
        line_colored = ANSIColors.white(line[0:col_start])
        line_colored += ANSIColors.bright_white(line[col_start : col_end + 1])
        line_colored += ANSIColors.bright_black(line[col_end + 1 : len(line)])
        line = line_colored

        result += ANSIColors.bright_black(line_number) + line + "\n"
        result += f"{' ' * (len(line_number) - 4)}"
        result += f"{ANSIColors.bright_black('  | ')}{' ' * col_start}"
        result += f"{ANSIColors.bright_red('^') * (col_end - col_start+1)}\n"

      idx_start = idx_end
      idx_end = self.src.find("\n", idx_start + 1)
      if idx_end < 0:
        idx_end = len(self.src)

    return result.replace("\t", "")


class ParserError(Error):

  def __init__(self, msg: str, token: Token):
    super().__init__(
        msg,
        token.start_pos.fsrc,
        token.start_pos,
        token.end_pos,
        "Parser Error",
    )


class LexerError(Error):

  def __init__(self, msg: str, src: str, start_pos: Position, end_pos: Position):
    super().__init__(msg, src, start_pos, end_pos, "Lexer Error")


class WidgetError(Error):

  def __init__(self, msg: str, node: XMLNode):
    if not (node.start_pos and node.end_pos): return
    super().__init__(
        msg,
        node.start_pos.fsrc,
        node.start_pos,
        node.end_pos,
        "Widget Error",
    )
