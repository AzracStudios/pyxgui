from os import path

from pyxgui.cli.load_art import load_art


def main() -> None:
  file_path: str = path.abspath(__file__)
  last_slash: int = file_path.rfind("/")
  file_path = path.join(file_path[:last_slash], "art.txt")

  print(load_art(file_path, "1.0"))

  return None


main()
