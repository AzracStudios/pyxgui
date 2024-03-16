import os
from pyxgui.utils.colors import Colors
from pyxgui.wtree_gen.xml_lexer import *
from pyxgui.wtree_gen.xml_parser import *

from pyxgui.wtree_gen.xml_to_widget import WidgetTreeGenerator

from pyxgui.renderer.window import *


def load_source(path: str):
  if not os.path.exists(path):
    print(Colors.bright_red(f"Error: {path} does not exist!"))
    return None

  with open(path, encoding="UTF-8") as f:
    return "".join(f.readlines())


def stringify_xml_tree(node: XMLNode, depth) -> str:
  res = "  " * depth
  res += f"{node}\n"
  for child in node.children:
    res += stringify_xml_tree(child, depth + 1) + "\n"
  return res


def main():
  src: str = load_source("./test_files/simple_test.xml")
  lexer = XMLLexer(src)
  tokens = lexer.tokenize()

  if not tokens:
    return

  parser = XMLParser(src, tokens)
  node = parser.parse()

  if not node:
    return

  print(stringify_xml_tree(node, 0))

  wtg = WidgetTreeGenerator(node)
  widget_tree = wtg.generate_tree()

  if not widget_tree:
    return

  print(widget_tree)


def renderer():
  win = Window()

  rect = Rect()
  win.add_child(rect)

  rect.set_dimension_constraint(ConstraintVector(Relational(50), Aspect(1) ))
  rect.set_position_constraint(ConstraintVector(Relational(50), Relational(50)))
  rect.translate_position_relative(ConstraintVector(Relational(-50), Relational(-50)))

  poppins = FontHandler("./fonts/poppins")

  text = Text("Hello world!", poppins.weight("Bold"), 25, 0, raylib.BLACK)
  rect.add_child(text)

  text.set_position_constraint(ConstraintVector(Relational(50), Relational(50)))
  text.translate_position_relative(ConstraintVector(Relational(-50), Relational(-50)))
  win.render()


if __name__ == "__main__":
  renderer()
