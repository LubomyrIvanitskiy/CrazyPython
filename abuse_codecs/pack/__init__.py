import codecs

from typing import Tuple
mapping = {
      'якнє': 'else',
  'як': 'if',
  'то': 'print',
  'Так': 'True',
  'Ніт': 'False',
  'це': 'def'
}
def custom_encode(text: str) -> Tuple[bytes, int]:
    return text.encode('utf8'), len(text)

def custom_decode(binary: bytes) -> Tuple[str, int]:
    txt = binary.tobytes().decode("utf-8")
    for w in mapping:
      txt = txt.replace(w, mapping[w])
    return txt, len(binary) #''.join(binary), len(binary)

def custom_search_function(encoding_name):
    return codecs.CodecInfo(custom_encode, custom_decode, name='zapovit')

codecs.register(custom_search_function)