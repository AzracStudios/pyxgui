import os
from pyxgui.utils.colors import Colors
from pyxgui.xml_parser.lexer import Lexer
from pyxgui.xml_parser.xml_parser import Parser
from pyxgui.xml_parser.errors import Error
from pyxgui.xml_parser.structs import XMLNode


def load_source(path: str):
  if not os.path.exists(path):
    print(Colors.bright_red(f"Error: {path} does not exist!"))
    return None

  with open(path, encoding="UTF-8") as f:
    return "".join(f.readlines())


def print_xml_tree(node: XMLNode, depth) -> str:
  res = "  " * depth
  res += f"{node}\n"
  for child in node.children:
    res += print_xml_tree(child, depth + 1) + "\n"
  return res


def main():
  src: str = load_source("./test.xml")
  lexer = Lexer(src)
  tokens = lexer.tokenize()

  # if tokens:
  #   print(tokens)

  parser = Parser(src, tokens)
  node = parser.parse_tag(None)

  if isinstance(node, Error):
    print(node.generate_error_text())
    return

  print(print_xml_tree(node, 0))


if __name__ == "__main__":
  main()
