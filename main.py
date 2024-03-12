from pyxgui.xml_parser import XMLParser, XMLNode, Error

parser = XMLParser("./test.xml")
parser.generate_xml_tree()
node = parser.document.root

if isinstance(node, XMLNode):
  print(f"{node.tag}: {node.inner_text}")
elif isinstance(node, Error):
  print(node.generate_error_text())