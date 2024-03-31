def load_art(file_path: str, version: str) -> str:
  """Load ASCII Art From File Path

  Args:
      file_path (str): path to art file
      version (str): version that has to be inserted in the art

  Returns:
      str: final art after inserting the version information
  """

  with open(file_path, "r", encoding="UTF-8") as f:
    lines = "".join(f.readlines())
    version_index = lines.index("$")

    art_bfr_version = lines[:version_index]
    art_aftr_version = lines[version_index + 1 :]

    final_art = art_bfr_version + version + art_aftr_version
    final_art = final_art.replace("\\u001b[37;1m", "\u001b[37;1m")
    final_art = final_art.replace("\\u001b[0m", "\u001b[0m")
    return final_art
