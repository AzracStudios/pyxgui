from pyxgui.wtree_gen.error import Error, WidgetError

from pyxgui.wtree_gen.structs import XMLNode

from pyxgui.wtree_gen.widgets.widget import Widget
from pyxgui.wtree_gen.widgets.text import TextWidget


class WidgetTreeGenerator:

  def __init__(self, xml_tree: XMLNode):
    self.xml_tree = xml_tree

  def traverse_node(self, parent: XMLNode):
    # generate widget if it is a core element
    # generate pointer if it is a custom widget
    # traverse children and populate current node

    widget: Widget | None = None

    # generate text widget
    if parent.tag == "text":
      # text widgets are not allowed to have children
      # generate error if children are present
      
      if len(parent.children) != 0:
        return WidgetError("The text widget cannot have children", parent.children[0])
      widget = TextWidget(parent.inner_text)

    return widget

  def generate_tree(self) -> XMLNode | None:
    tree = self.traverse_node(self.xml_tree)
    if isinstance(tree, Error):
      print(tree.generate_error_text())
      return None
    
    return tree