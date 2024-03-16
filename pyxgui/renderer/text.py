from pyxgui.renderer.widget import *


class Text(Widget):

  def __init__(
      self,
      text: str,
      font: raylib.Font,
      font_size: int,
      line_spacing: int,
      color: raylib.Color,
  ):
    super().__init__()
    self.font = font
    self.font_size = font_size
    self.line_spacing = line_spacing
    self.color = color
    self.set_text(text)

  def set_text(self, text: str):
    self.text = text
    self.set_dimension_constraint(
        ConstraintVector(
            Pixel(
                raylib.measure_text_ex(
                    self.font, self.text, self.font_size, self.line_spacing
                ).x
            ),
            Pixel(self.font_size),
        )
    )

  def render(self):
    raylib.draw_text_ex(
        self.font,
        self.text,
        raylib.Vector2(self.position.x, self.position.y),
        self.font_size,
        self.line_spacing,
        self.color,
    )
