from __future__ import annotations

from pyxgui.lang.lib.position import Position
from pyxgui.lang.xml.attrib import XMLAttribute

class XMLNode:

  def __init__(
      self,
      parent: XMLNode | None,
  ):
    self.tag: str | None = None
    self.inner_text: str = ""

    self.parent = parent

    self.attributes: list[XMLAttribute] = []
    self.children: list[XMLNode] = []

    self.start_pos: Position | None = None
    self.end_pos: Position | None = None

  def __repr__(self) -> str:
    res = f"{self.tag}: {self.inner_text}"
    if not self.attributes:
      return res

    res += "\nattrs:"
    attribs = [str(attr) for attr in self.attributes]
    res += ", ".join(attribs)

    return res
