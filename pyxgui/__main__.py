from pyxgui.lang.xml.lexer import XMLLexer
from pyxgui.lang.xml.parser import XMLParser

def main() -> None:
  src = """<test> Hola world! 123 432 </test>
  """

  my_lexer = XMLLexer(src)

  tokens = my_lexer.tokenize()
  if tokens is None:
    return
  
  print(tokens)

  parser = XMLParser(src, tokens)
  res = parser.parse()
  if res is None:
    return
  
  print(res)

main()

