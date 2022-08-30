from xpinyin import Pinyin
import pycantonese

p = Pinyin()
def pinyin(x: str) -> str:
   return p.get_pinyin(x, tone_marks="marks", splitter=" ")

def main():
   # Loop through all the tuples and get the second element to append it to the text
   jyuping = ""
   for text in pycantonese.characters_to_jyutping("填滿一生 全是數字"):
      jyuping += text[1] + " "
   
   return jyuping

if __name__ == "__main__":
   print(main())