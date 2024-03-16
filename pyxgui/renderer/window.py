from pyxgui.renderer.widget import *
from pyxgui.renderer.rect import Rect
from pyxgui.renderer.text import Text
from pyxgui.renderer.font_handler import FontHandler


class Window(Widget):

  def __init__(self):
    super().__init__()
    self.initialize_window()

  def initialize_window(self):
    # allow window resizing
    raylib.set_config_flags(raylib.ConfigFlags.FLAG_WINDOW_RESIZABLE)

    # initialize a dummy window
    raylib.init_window(100, 100, "pyXgui")

    # set window size
    current_monitor = raylib.get_current_monitor()
    monitor_dimensions = Vector2(
        raylib.get_monitor_width(current_monitor),
        raylib.get_monitor_height(current_monitor),
    )

    self.set_dimension_constraint(
        ConstraintVector(
            Pixel(monitor_dimensions.x - 100),
            Pixel(monitor_dimensions.y - 100),
        )
    )

    raylib.set_window_size(self.dimension.x, self.dimension.y)

    raylib.set_window_min_size(100, 100)
    raylib.set_window_max_size(monitor_dimensions.x, monitor_dimensions.y)

  def handle_resize(self):
    if raylib.is_window_resized():
      self.set_dimension_constraint(
          ConstraintVector(
              Pixel(raylib.get_screen_width()), Pixel(raylib.get_screen_height())
          )
      )

  def render(self):
    while not raylib.window_should_close():
      self.handle_resize()

      raylib.begin_drawing()
      raylib.clear_background(raylib.WHITE)

      for child in self.children:
        child.render()

      raylib.end_drawing()
