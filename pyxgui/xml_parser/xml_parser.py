from pyxgui.xml_parser.structs import Token, XMLAttribute, XMLNode
from pyxgui.xml_parser.errors import Error, ParserError
import pyxgui.xml_parser.constants as const


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

  def parse_attributes(self) -> XMLAttribute:
    current_attrib = XMLAttribute()
    attributes = []

    while self.current_token.type == const.TT_WORD:
      current_attrib.key = self.current_token.value
      self.advance()

      if self.current_token.type != const.TT_EQL:
        return ParserError("Expected '='", self.current_token)

      self.advance()

      if self.current_token.type not in (const.TT_STRING, const.TT_NUMBER):
        return ParserError("Expected number or string", self.current_token)

      current_attrib.value = self.current_token.value
      self.advance()
      self.skip([const.TT_SPACE])

      attributes.append(current_attrib)
      current_attrib = XMLAttribute()

    return attributes

  def parse_children(self, parent: XMLNode) -> list[XMLNode] | Error:
    children: list[XMLNode] = []

    if self.peek_tokens(1).type != const.TT_FWDSLSH:
      while self.current_token.type == const.TT_LANGLE:
        if self.peek_tokens(1).type == const.TT_FWDSLSH:
          break

        child = self.parse_tag(parent)
        if isinstance(child, Error):
          return child

        children.append(child)
        continue

    return children

  def parse_inner_text(self):
    inner_text = ""
    while True:
      if self.current_token.type == const.TT_WORD:
        inner_text += self.current_token.value
      elif self.current_token.type == const.TT_SPACE:
        inner_text += " "
      elif self.current_token.type == const.TT_NUMBER:
        inner_text += str(self.current_token.value)
      else:
        break

      self.advance()

    return inner_text

  def parse_tag(self, parent: XMLNode | None) -> XMLNode:
    node: XMLNode = XMLNode(parent)

    # inline_tag: LANGLE WORD (WORD EQL (STRING|NUMBER))?* FWDSLSH RANGLE
    #####
    # tag: LANGLE WORD (WORD EQL (STRING|NUMBER))?* RANGLE (tag?*) LANGLE FWDSLSH WORD RANGLE

    # beginning of tag
    if self.current_token.type != const.TT_LANGLE:
      return ParserError("Expected '<'", self.current_token)

    self.advance()

    # tag name
    if self.current_token.type != const.TT_WORD:
      return ParserError("Expected tag name", self.current_token)

    node.tag = self.current_token.value

    self.advance()
    self.skip([const.TT_SPACE])

    # attributes
    attribtues = self.parse_attributes()

    if isinstance(attribtues, Error):
      return attribtues

    node.attributes = attribtues

    # inline tag
    if (
        self.current_token.type == const.TT_FWDSLSH
        and self.peek_tokens(1).type == const.TT_RANGLE
    ):
      self.advance(2)
      self.skip([const.TT_SPACE, const.TT_NL])
      return node

    if self.current_token.type != const.TT_RANGLE:
      return ParserError("Expected '>'", self.current_token)

    self.advance()
    self.skip([const.TT_SPACE, const.TT_NL])

    # parse inner text
    node.inner_text = self.parse_inner_text()
    self.skip([const.TT_SPACE, const.TT_NL])

    if self.current_token.type == const.TT_LANGLE:
      # parse children
      children = self.parse_children(node)
      if isinstance(children, Error):
        return children
      node.children = children

      # tag closing
      self.advance(2)

      # check for tag mismsatch
      if self.current_token.type != const.TT_WORD:
        return ParserError("Expected tag name when closing", self.current_token)

      if self.current_token.value != node.tag:
        return ParserError(
            f"Tag name mismatch when closing: expected {node.tag}", self.current_token
        )

      self.advance()

      if self.current_token.type != const.TT_RANGLE:
        return ParserError("Expected '>'", self.current_token)

      self.advance()
      self.skip([const.TT_SPACE, const.TT_NL])

      return node
