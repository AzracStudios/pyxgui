import os
from pyxgui.utils.colors import Colors
import pyray as raylib


class FontHandler:

  def __init__(self, fonts_directory: str):
    self.fonts_dir = fonts_directory
    self.cache = {}
    self.load()

  def load(self):
    if not os.path.exists(self.fonts_dir):
      print(Colors.bright_red(f"Unable to load font, directory does not exist"))
      return

    font_files = os.listdir(self.fonts_dir)

    for file in font_files:
      name = file.split("-")[-1].split(".")[0]
      # self.cache[name] = load_font_ex(os.path.join(self.fonts_dir, file), 300, 0, 250)
      self.cache[name] = raylib.load_font(os.path.join(self.fonts_dir, file))
      raylib.set_texture_filter(
          self.cache[name].texture, raylib.TextureFilter.TEXTURE_FILTER_TRILINEAR
      )

  def weight(self, weight: str):
    return self.cache.get(weight, None)
