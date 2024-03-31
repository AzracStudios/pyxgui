# ANSI COLORS
#? REF: https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html


class ANSIColors:
  # Generates code for standard ANSI color codes along with a basic test
  # PS: I am too lazy to write the functions out myself :)

  @staticmethod
  def generate_code() -> str:
    colors = [
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
    ]

    code = ""

    for i in range(len(colors)):
      code += f"""
    @staticmethod
    def {colors[i]}(text: str) -> str:
        return f\'\\u001b[{30 + i}m{'{'}text{'}'}\\u001b[0m\'

    @staticmethod
    def bright_{colors[i]}(text: str) -> str:
        return f\'\\u001b[{30 + i};1m{'{'}text{'}'}\\u001b[0m\'
"""
      
    return code

  @staticmethod
  def black(text: str) -> str:
    return f"\u001b[30m{text}\u001b[0m"

  @staticmethod
  def bright_black(text: str) -> str:
    return f"\u001b[30;1m{text}\u001b[0m"

  @staticmethod
  def red(text: str) -> str:
    return f"\u001b[31m{text}\u001b[0m"

  @staticmethod
  def bright_red(text: str) -> str:
    return f"\u001b[31;1m{text}\u001b[0m"

  @staticmethod
  def green(text: str) -> str:
    return f"\u001b[32m{text}\u001b[0m"

  @staticmethod
  def bright_green(text: str) -> str:
    return f"\u001b[32;1m{text}\u001b[0m"

  @staticmethod
  def yellow(text: str) -> str:
    return f"\u001b[33m{text}\u001b[0m"

  @staticmethod
  def bright_yellow(text: str) -> str:
    return f"\u001b[33;1m{text}\u001b[0m"

  @staticmethod
  def blue(text: str) -> str:
    return f"\u001b[34m{text}\u001b[0m"

  @staticmethod
  def bright_blue(text: str) -> str:
    return f"\u001b[34;1m{text}\u001b[0m"

  @staticmethod
  def magenta(text: str) -> str:
    return f"\u001b[35m{text}\u001b[0m"

  @staticmethod
  def bright_magenta(text: str) -> str:
    return f"\u001b[35;1m{text}\u001b[0m"

  @staticmethod
  def cyan(text: str) -> str:
    return f"\u001b[36m{text}\u001b[0m"

  @staticmethod
  def bright_cyan(text: str) -> str:
    return f"\u001b[36;1m{text}\u001b[0m"

  @staticmethod
  def white(text: str) -> str:
    return f"\u001b[37m{text}\u001b[0m"

  @staticmethod
  def bright_white(text: str) -> str:
    return f"\u001b[37;1m{text}\u001b[0m"

  @staticmethod
  def test_palette() -> None:
    string: str = "███"

    print(
        "\n",
        ANSIColors.black(string),
        ANSIColors.red(string),
        ANSIColors.green(string),
        ANSIColors.yellow(string),
        ANSIColors.blue(string),
        ANSIColors.magenta(string),
        ANSIColors.cyan(string),
        ANSIColors.white(string),
        "\n",
        ANSIColors.bright_black(string),
        ANSIColors.bright_red(string),
        ANSIColors.bright_green(string),
        ANSIColors.bright_yellow(string),
        ANSIColors.bright_blue(string),
        ANSIColors.bright_magenta(string),
        ANSIColors.bright_cyan(string),
        ANSIColors.bright_white(string),
        "\n",
        sep="",
    )

    return None