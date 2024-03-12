from pyxgui.xml_parser.xmlnode import XMLNode


class XMLDocument:

  def __init__(self, source: str, root: XMLNode) -> None:
    self.source: str = source
    self.root: XMLNode = root
