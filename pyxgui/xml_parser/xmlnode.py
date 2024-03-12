from __future__ import annotations


class XMLNode:
  def __init__(self, parent: XMLNode) -> None:
    self.tag: str = ""
    self.inner_text: str = ""
    self.parent: XMLNode = parent
