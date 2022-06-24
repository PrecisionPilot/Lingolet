from xpinyin import Pinyin
import pycantonese

p = Pinyin()
def pinyin(x: str) -> str:
   p.decode_pinyin
   return p.get_pinyin(x, tone_marks="marks", splitter=" ")

text = pycantonese.parse_text("安靜的夜晚裡 頭腦還不想停")
print(pycantonese.characters_to_jyutping(text))
print(p.decode_pinyin("sau4"))