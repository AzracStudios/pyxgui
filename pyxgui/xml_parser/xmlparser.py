import os
from pyxgui.utils.colors import Colors
from pyxgui.xml_parser.xmldoc import XMLDocument
from pyxgui.xml_parser.xmlnode import XMLNode
from pyxgui.xml_parser.position import Position
from pyxgui.xml_parser.errors import ParserError


class XMLParser:

  def __init__(self, src_path: str):
    self.document: XMLDocument | None = None
    self.current_char: str | None = None
    self.position: Position = Position(-1, -1, 1)

    self._load_xml_document(src_path)
    self._advance()

  def _load_xml_document(self, path: str) -> None:
    if not os.path.exists(path):
      print(Colors.bright_red(f"Error: {path} does not exist!"))
      return None

    with open(path, encoding="UTF-8") as f:
      source = "".join(f.readlines())
      self.document = XMLDocument(source, XMLNode(None))

  def _advance(self, advance_by: int = 1) -> Position | None:
    i = 0
    while i < advance_by:
      self.position.advance(self.current_char)
      i += 1

    if not self.document:
      print(Colors.bright_red("Error: no document was loaded"))
      return

    if self.position.idx < len(self.document.source):
      self.current_char = self.document.source[self.position.idx]
      return

    self.current_char = None

  def _peek_character(self, peek_by: int) -> str | None:
    if (i := self.position.idx + peek_by) < len(self.document.source):
      return self.document.source[i]
    return None

  def _skip_newlines(self) -> None:
    while self.current_char == "\n":
      self._advance()

    return None

  def generate_xml_tree(self) -> None:
    current_node: XMLNode | None = None
    lexical_buffer: str = ""

    while self.current_char is not None:
      if self.current_char == "<":
        position_snapshot: Position = self.position.copy()
        if lexical_buffer:
          # BUFFER EXISTS OUTSIDE A NODE
          if not current_node:
            return ParserError(
                "Text outside document",
                self.document.source,
                position_snapshot,
                self.position.copy(),
            )

          current_node.inner_text = lexical_buffer
          lexical_buffer = ""

        # END OF A TAG
        if self._peek_character(1) == "/":
          position_snapshot: Position = self.position.copy()
          self._advance(2)

          ## SCAN TAG NAME
          while self.current_char != ">":
            lexical_buffer += self.current_char
            self._advance()

          if not current_node:
            return ParserError(
                "No Tag Was Defined",
                self.document.source,
                position_snapshot,
                self.position.copy(),
            )

          if current_node.tag != lexical_buffer:
            return ParserError(
                "Tag Mismatch",
                self.document.source,
                position_snapshot,
                self.position.copy(),
            )

          # RESET BUFFER
          lexical_buffer = ""
          current_node = current_node.parent
          self._advance()
          self._skip_newlines()
          continue

        ## SET CURRENT NODE
        if not current_node:
          current_node = self.document.root
        else:
          current_node = XMLNode(current_node)

        # BEGINNING OF A TAG
        self._advance()

        ## SCAN TAG NAME
        while self.current_char != ">":
          lexical_buffer += self.current_char
          self._advance()

        current_node.tag = lexical_buffer
        lexical_buffer = ""

        self._advance()
        continue

      else:
        lexical_buffer += self.current_char
        self._advance()
