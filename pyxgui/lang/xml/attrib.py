class XMLAttribute:

  def __init__(self) -> None:
    self.key: str | None = None
    self.value: str | int | float | None = None

    return None

  def __repr__(self) -> str:
    return f"[{self.key}:{self.value}]"
