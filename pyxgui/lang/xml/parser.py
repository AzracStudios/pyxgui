from pyxgui.lang.lib.parser import Parser
from pyxgui.lang.lib.token import Token, TokenType
from pyxgui.lang.xml.attrib import XMLAttribute
from pyxgui.lang.xml.node import XMLNode
from pyxgui.lang.lib.error import Error, ParserError


class XMLParser(Parser):

  def __init__(self, source: str, tokens: list[Token]) -> None:
    super().__init__(source, tokens)
    return None

  def parse_attributes(self) -> list[XMLAttribute] | ParserError:
    current_attrib = XMLAttribute()
    attributes = []

    while self.current_token and self.current_token.type == TokenType.WORD:
      current_attrib.key = str(self.current_token.value)
      self.advance()

      if self.current_token.type != TokenType.EQL:
        return ParserError("Expected '='", self.current_token)

      self.advance()

      if self.current_token.type not in (TokenType.STRING, TokenType.NUMBER):
        return ParserError("Expected number or string", self.current_token)

      current_attrib.value = self.current_token.value
      self.advance()
      self.skip([TokenType.WHITESPACE])

      attributes.append(current_attrib)
      current_attrib = XMLAttribute()

    return attributes

  def parse_children(self, parent: XMLNode) -> list[XMLNode] | Error:
    children: list[XMLNode] = []

    if (x := self.peek_tokens(1)) and x.type == TokenType.FWDSLSH:
      return children

    while (x := self.current_token) and x.type == TokenType.LANGLE:
      if (x := self.peek_tokens(1)) and x.type == TokenType.FWDSLSH:
        break

      child = self.parse_tag(parent)
      if isinstance(child, Error):
        return child

      if not child:
        continue

      children.append(child)

    return children

  def parse_inner_text(self) -> str:
    inner_text = ""

    while True and self.current_token:
      if self.current_token.type == TokenType.WORD:
        inner_text += str(self.current_token.value)
      elif self.current_token.type == TokenType.WHITESPACE:
        inner_text += " "
      elif self.current_token.type == TokenType.NUMBER:
        inner_text += str(self.current_token.value)
      elif self.current_token.type == TokenType.STRING:
        inner_text += str(self.current_token.value)
      else:
        break

      self.advance()

    return inner_text

  def parse_tag(self, parent: XMLNode | None) -> XMLNode | Error | None:
    node: XMLNode = XMLNode(parent)

    # inline_tag: LANGLE WORD (WORD EQL (STRING|NUMBER))?* FWDSLSH RANGLE
    #####
    # tag: LANGLE WORD (WORD EQL (STRING|NUMBER))?* RANGLE (tag?*) LANGLE FWDSLSH WORD RANGLE

    if not self.current_token:
      return None

    # beginning of tag
    if self.current_token.type != TokenType.LANGLE:
      return ParserError("Expected '<'", self.current_token)

    node.start_pos = self.current_token.start_pos.copy()
    self.advance()

    # comments
    if (
        self.source[
            self.current_token.start_pos.idx : self.current_token.start_pos.idx + 3
        ]
        == "!--"
    ):
      while (
          self.source[
              self.current_token.start_pos.idx : self.current_token.start_pos.idx + 3
          ]
          != "-->"
      ):
        if self.current_token is None:
          return ParserError("Comment was never closed", self.current_token)
        self.advance()
        print(self.current_token)
      else:
        self.advance(advance_by=2)
        self.skip([TokenType.WHITESPACE])
        return None

    # tag name
    if self.current_token.type != TokenType.WORD:
      return ParserError("Expected tag name", self.current_token)

    node.tag = str(self.current_token.value)

    self.advance()
    self.skip([TokenType.WHITESPACE])

    # attributes
    attribtues = self.parse_attributes()

    if isinstance(attribtues, Error):
      return attribtues

    node.attributes = attribtues

    # inline tag
    if (
        self.current_token.type == TokenType.FWDSLSH
        and (x := self.peek_tokens(1))
        and x.type == TokenType.RANGLE
    ):
      self.advance(2)
      node.end_pos = self.current_token.start_pos.copy()
      self.skip([TokenType.WHITESPACE])
      return node

    if self.current_token.type != TokenType.RANGLE:
      return ParserError("Expected '>'", self.current_token)

    self.advance()
    self.skip([TokenType.WHITESPACE])

    # parse inner text
    node.inner_text = self.parse_inner_text()
    self.skip([TokenType.WHITESPACE])

    if self.current_token.type != TokenType.LANGLE:
      return ParserError(f"Tag {node.tag} was never closed", self.current_token)

  
    # parse children
    children = self.parse_children(node)
    if isinstance(children, Error):
      return children
    node.children = children

    if (
        self.current_token.type != TokenType.LANGLE
        and (x := self.peek_tokens(1))
        and x.type != TokenType.FWDSLSH
    ):
      return ParserError(f"Tag '{node.tag}' was never closed", self.current_token)

    # tag closing
    self.advance(2)

    # check for tag mismsatch
    if self.current_token.type != TokenType.WORD:
      return ParserError("Expected tag name when closing", self.current_token)

    if self.current_token.value != node.tag:
      return ParserError(
          f"Tag name mismatch when closing: expected '{node.tag}'", self.current_token
      )

    self.advance()

    if self.current_token.type != TokenType.RANGLE:
      return ParserError("Expected '>'", self.current_token)

    self.advance()
    node.end_pos = self.current_token.start_pos.copy()

    self.skip([TokenType.WHITESPACE])

    return node


  def parse(self) -> XMLNode | Error | None:
    tag = self.parse_tag(None)

    if isinstance(tag, Error):
      print(tag.generate_error_text())
      return None

    if (x := self.current_token) and x.type != TokenType.EOF:
      err = ParserError(
          "Document must contain only one root widget", self.current_token
      )
      print(err.generate_error_text())
      return None

    return tag
