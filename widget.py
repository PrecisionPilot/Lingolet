import tkinter as tk
from tkinter import messagebox
from tkinter import font
import deepl
from internetConnection import isConnected
import time
import math

class Widget():
    def __init__(self) -> None:
        self.debugMode = False
        
        # User defined variables
        self.minSize = (500, 300)
        self.maxSize = (700, 500)
        self.margins = 10
        self.borderOutline = 3
        self.myFont = ("Arial", 13)
        self.myBoldFont = (self.myFont[0], self.myFont[1], "underline", "bold")
        self.mySmallFont = (self.myFont[0], int(self.myFont[1] / 1.3))
        self.textHeight = self.myFont[1] * 1.75

        # Initialize deepL API
        self.key = ""
        with open("deepL auth.txt", "r") as f:
            self.key = f.read()
        self.translator = deepl.Translator(self.key)

    def open(self, inText=""):
        # Avoid hotkey bug
        time.sleep(0.5)

        # Check for internet connection
        if not isConnected():
            print("Error: No internet connection!")
            messagebox.showwarning(title="Error", message="No internet connection!")
            return

        # Initialize window
        self.root = tk.Tk()
        self.root.title("Lingolet")
        self.root.iconbitmap("icon.ico")
        self.root.geometry(str(self.minSize[0]) + "x" + str(self.minSize[1]))
        self.root.focus()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.resizable(False, False)

        # Set variables
        self.inText = inText
        self.outText = tk.StringVar()

        # Input text
        self.inputBox = tk.Text(self.root, font=self.myFont, borderwidth=self.borderOutline, relief=tk.SUNKEN)
        self.inputBox.insert(1.0, inText)

        # Output frame
        self.outputFrame = tk.Frame(self.root, borderwidth=self.borderOutline, relief=tk.SUNKEN)
        self.outputFrame.grid_rowconfigure(0, weight=2)
        self.outputFrame.grid_columnconfigure(0, weight=1)

        # Place "Translation:"
        self.translationText = tk.Label(self.outputFrame, text="Translation:", font=self.myBoldFont, justify=tk.LEFT)

        # Translate text, then set the label accordingly
        self.translate()

        # Key bindings
        self.root.bind("<Escape>", self.close)
        self.root.bind("<Control-Return>", self.translate)


        self.root.mainloop()
        
    
    def translate(self, event=None):
        # Update "inText"
        self.inText = self.inputBox.get(1.0, tk.END)
        # Remove all trailing edges
        self.inText = self.inText.strip()
        self.inputBox.delete(1.0, tk.END)
        self.inputBox.insert(1.0, self.inText)

        # Output text
        # Set outputText's "textvariable" to "outText", then translate
        self.outputText = tk.Label(self.outputFrame, textvariable=self.outText, font=self.myFont, justify=tk.LEFT, anchor="nw")

        # Button
        self.translateButton = tk.Button(self.outputFrame, text="Translate", command=self.translate)
        # Place button at bottom right corder
        self.translateButton.grid(row=2, column=1, padx=10, pady=10, sticky="se")


        # No text error handling
        if self.inText == "":
            messagebox.showwarning(title="Error", message="Text field cannot be empty!")
            return

        # Get text from textbox and set it as the outText variable
        if self.debugMode:
            self.targetText = "Translation"
        else:
            self.targetText = self.translator.translate_text(self.inText, source_lang="ZH", target_lang="EN-US")
        # Set the text ok the label
        self.outText.set(self.targetText)
        self.resize()
        
    def resize(self):
        # Update outputTextSize upon "outputText" change
        # Output Text
        self.outputText.place(x=0, y=0)
        self.outputText.configure(font=self.myFont)
        self.outputText.update()
        self.outputTextSize = [self.outputText.winfo_width(), self.outputText.winfo_height()]
        
        # Update text based on output text

        self.newSize = list(self.minSize)
        # If x of outputText is bigger than x of min window size, newSize = x
        if self.outputTextSize[0] > self.newSize[0]:
            self.newSize[0] = self.outputTextSize[0]

            # If x exceeds max value, cap it
            if self.newSize[0] > self.maxSize[0]:
                self.newSize[0] = self.maxSize[0]
                # Since the text in one line exceeds the max window width, shrink font size
                self.outputText.configure(font=self.mySmallFont)
                print("small font set")
                # Update outputTextSize
                self.outputText.update()
                self.outputTextSize = [self.outputText.winfo_width(), self.outputText.winfo_height()]
            else:
                # If text isn't too big, set font size to default
                print("normal font")
        # If y of outputText is greater than height of outputFrame
        self.outputFrameHeight = self.newSize[1] / 2 + self.textHeight
        if self.outputTextSize[1] > self.outputFrameHeight:
            print("Horizontal resize")
            print(self.outText.get())
            # outputFrameHeight needs to be enlarged to outputTextSize, to do so, change newSize[1] 
            self.newSize[1] = (self.outputTextSize[1] - self.textHeight) * 2
            self.newSize[1] =  math.ceil(self.newSize[1])
            if self.newSize[1] > self.maxSize[1]:
                self.newSize[1] = self.maxSize[1]


        # Resize contents: place the elements first, then add margins and resize the whole window
        # Update newSize to fit contents
        self.root.geometry(str(self.newSize[0] + self.margins * 2) + "x" + str(self.newSize[1] + self.margins * 2))
        print("Width:", self.root.winfo_width(), self.root.winfo_height())
        
        # inputBox should be 1 margin unit from the window top extending directly to the window y (mid-point - textHeight)
        self.inputBox.place(x=self.margins, y=self.margins, width=self.newSize[0], height=self.newSize[1] / 2 - self.textHeight - self.margins)
        
        # Update "wraplength" of outputText the same as its width for to automatically have newlines when text reaches out of the textbox
        self.outputText.configure(wraplength=self.newSize[0])
        # translationText begins from y (mid-point - textHeight) + 1 margin unit to mid-point + 1 margin unit
        self.outputFrame.place(x=self.margins, y=self.newSize[1] / 2 - self.textHeight + self.margins, width=self.newSize[0], height=self.newSize[1] / 2 + self.textHeight)
        self.translationText.place(x=0, y=0)
        # outputText y value is mid-point + 1 margin unit
        self.outputText.place(x=0, y=self.textHeight, width=self.newSize[0] - self.borderOutline * 2, height=self.newSize[1] / 2 - self.margins)
    
    def close(self, event=None):
        self.root.destroy()

# Testing purposes
def main():
    widget = Widget()
    text1 = "安靜的夜晚裡 頭腦還不想停"
    text2 = "你說藍色是你最愛的顏色 你說如果沒有愛那又如何"
    text3 = "一二三四五六七 使出必殺技，哥能否追到你，七六五四三二一，真的太可惜，喜歡的人不是你"
    text4 = "愁看殘紅亂舞 憶花底初度逢 難禁垂頭淚湧 此際幸月朦朧 愁悴如何自控 悲哀都一樣同 情意如能互通 相分不必相送"
    text5 = "安靜的夜晚裡 頭腦還不想停\n我還騎著腳踏車載著妳\n潜入了大海裡 我笑著看著妳\n片段的回憶抓著我的心\n緣分還是第一 像悲劇的電影\n我學會至少我們擁有了會經\n這是我的決定\n決定把我們變成美好的記憶\n妳付出愛我的時候\n擁抱妳的人還是我\n爭吵時我都不會走"
    widget.open(inText=text5)

if __name__ == "__main__":
    main()


# Make it so that you can show or hide window