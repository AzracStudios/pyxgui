from pyxgui.renderer.widget import *


class Rect(Widget):

  def __init__(self):
    super().__init__()
    self.border_radius = 0
    self.color = raylib.GREEN
    self.outline = 0

  def render(self):
    raylib.draw_rectangle_rounded(
        raylib.Rectangle(
            self.position.x, self.position.y, self.dimension.x, self.dimension.y
        ),
        self.border_radius,
        25,
        self.color,
    )

    self.render_children()

