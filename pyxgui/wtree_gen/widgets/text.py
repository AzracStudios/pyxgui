from pyxgui.wtree_gen.widgets.widget import Widget

class TextWidget(Widget):
  def __init__(self, text:str):
    super().__init__()
    self.text = text

  def render(self):
    pass

