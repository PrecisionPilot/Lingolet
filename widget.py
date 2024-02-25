from inspect import isgenerator
import tkinter as tk
from tkinter import messagebox
from internetConnection import isConnected
from pynput.keyboard import Key, Controller
from xpinyin import Pinyin
import jyutping
import time
import math
import json
import deepl
import os
import playsound as playsound
import threading
from google.cloud import translate_v2 as translate
import googleTTS
import six
from google.cloud import translate_v2 as translate

class Widget():
    def __init__(self) -> None:
        self.debugMode = False
        
        # User defined variables
        self.initSize = (600, 600)
        self.minSize = (500, 300)
        self.maxSize = (700, 600)
        self.margins = 10
        self.borderOutline = 3
        self.myFont = ("Arial", 13)
        self.icon = "Assets/icon.ico"
        # self.outerColor = (0, 0, 0)
        self.myBoldFont = (self.myFont[0], self.myFont[1], "underline", "bold")
        self.myUnderlineFont = (self.myFont[0], self.myFont[1], "underline")
        self.mySmallFont = (self.myFont[0], int(self.myFont[1] / 1.3))
        self.textHeight = self.myFont[1] * 1.75
        self.buttonHeight = 30

        # Variables
        self.soundEffects = True
        self.cantonese = False
        self.showSimplified = True
        self.key = Controller()
        self.pinyin = Pinyin()
        self.sourceLanguage = ""
        self.detectedSourceLanguage = ""
        with open("Assets/DeepL translate codes.json") as f:
            self.deeplCodes = json.load(f)
        with open("Assets/Google translate codes.json") as f:
            self.googleCodes = json.load(f)

        # Initialize DeepL API
        self.apiKey = ""
        with open("Assets/Authentication/DeepL.txt", "r") as f:
            self.apiKey = f.read()
        self.DeepLTranslator = deepl.Translator(self.apiKey)

        # Initialize Google APIs
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Assets/Authentication/Google Cloud.json'
        self.GoogleTranslate = translate.Client()


    def welcome(self):
        # Only show welcome text once
        with open("Assets/data.json", "r+") as f:
            self.data = json.load(f)
            if self.data["showWelcomePage"] == False:
                return
            else:
                f.seek(0)
                self.data["showWelcomePage"] = False
                json.dump(self.data, f)
                

        # Initialize window
        self.root = tk.Tk()
        self.root.title("Welcome!")
        self.root.iconbitmap(self.icon)
        self.root.geometry(str(self.initSize[0]) + "x" + str(self.initSize[1]))
        self.root.focus()
        self.root.resizable(False, False)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Text
        with open("Assets/welcome page.txt", "r") as f:
            self.contents = f.read().split("\n")
        self.textFrame = tk.Frame(self.root)
        self.textFrame.place(x=self.margins, y=0, width=self.initSize[0] - self.margins * 2, height=self.initSize[1])
        self.textFrame.update()
        self.initSize = (self.textFrame.winfo_width(), self.textFrame.winfo_height())
        tk.Label(self.textFrame, text=self.contents[0], justify=tk.CENTER, font=self.myBoldFont).pack()
        for i in range(1, len(self.contents)):
            # Markdown formatting
            if self.contents[i][0:3] == "## ":
                tk.Label(self.textFrame, text=self.contents[i][3:], justify=tk.LEFT, font=self.myBoldFont, wraplength=self.initSize[0]).pack(anchor="w")
            else:
                tk.Label(self.textFrame, text=self.contents[i], justify=tk.LEFT, font=self.myFont, wraplength=self.initSize[0]).pack(anchor="w")

        # Ok button
        tk.Button(self.root, text="Use Lingolet", command=self.root.destroy).grid(row=0, column=0, padx=10, pady=10, sticky="se")


        self.root.mainloop()

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
        self.root.iconbitmap(self.icon)
        self.root.geometry(str(self.minSize[0]) + "x" + str(self.minSize[1]))
        self.root.focus()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.resizable(False, False)

        # Set variables
        self.inText = inText
        self.outText = ""

        # Input text
        self.inputBox = tk.Text(self.root, font=self.myFont, borderwidth=self.borderOutline, relief=tk.SUNKEN)
        self.inputBox.insert(1.0, inText)

        # Output frame
        self.outputFrame = tk.Frame(self.root, borderwidth=self.borderOutline, relief=tk.SUNKEN)
        self.outputFrame.grid_rowconfigure(0, weight=2)
        self.outputFrame.grid_columnconfigure(0, weight=1)
        

        # Translate text, then set the label accordingly
        self.translate(sound_effect=False)

        # Key bindings
        self.root.bind("<Escape>", self.close)
        self.root.bind("<Control-Return>", self.translate)


        self.root.lift()
        self.root.mainloop()
        self.releaseKeys()
    
    def playSoundEffect(self, sound_effect: str):
        if self.soundEffects:
            threading.Thread(target=playsound.playsound, args=(f"Assets/Sound Effects/{sound_effect}",)).start()
    
    def cantonese2pinyin(self, text=""):
        self.jyuping = " ".join(jyutping.get(text))
        print(self.jyuping)
        return self.jyuping
    
    def getLanguage(self, text=""):
        return self.GoogleTranslate.detect_language(text)["language"]
    
    def code2language(self, isGoogle: bool, code: str) -> str:
        if code == "":
            return "Detect language"
        if isGoogle:
            for codeItem, languageItem in self.googleCodes.items():
                if codeItem == code:
                    return languageItem
        else:
            for codeItem, languageItem in self.deeplCodes.items():
                if codeItem == code:
                    return languageItem
        return None

    def language2code(self, isGoogle: bool, language: str) -> str:
        if language == "Detect language":
            return ""
        if isGoogle:
            for codeItem, languageItem in self.googleCodes.items():
                if languageItem == language:
                    return codeItem
            return None
        else:
            for codeItem, languageItem in self.deeplCodes.items():
                if languageItem == language:
                    return codeItem
            return None

    def translateGoogle(self, target, text):

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = self.GoogleTranslate.translate(text, target_language=target)
        return result["translatedText"]

    def translate(self, sound_effect=True, event=None):
        # Settings button
        tk.Button(self.root, text="Settings", command=self.openSettings).grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Playsound button
        self.speakerImage = tk.PhotoImage(file="Assets/Speaker.png")
        tk.Button(self.root, text="Play sound", image=self.speakerImage, command=googleTTS.playSpeech).grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        # Translate button
        # Old: tk.Button(self.inputBox, text="Translate", command=self.translate).grid(row=2, column=1, padx=10, pady=10, sticky="se")
        tk.Button(self.root, text="Translate", command=self.translate).grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        # Update "inText"
        self.inText = self.inputBox.get(1.0, tk.END)
        # Remove all trailing edges
        self.inText = self.inText.strip()
        self.inputBox.delete(1.0, tk.END)
        self.inputBox.insert(1.0, self.inText)

        # Output text
        # Set outputText's "textvariable" to "outText", then translate
        self.outputText = tk.Text(self.outputFrame, font=self.myFont)

        # No text error handling
        if self.inText == "":
            messagebox.showwarning(title="Error", message="Text field cannot be empty!")
            return

        # Get text from textbox and set it as the outText variable
        if self.debugMode:
            self.outText = "Translation"
        else:
            # Detect language if source language isn't set
            if self.sourceLanguage == "":
                self.outText = self.DeepLTranslator.translate_text(self.inText, target_lang="EN-US")
            else:
                self.outText = self.DeepLTranslator.translate_text(self.inText, source_lang=self.sourceLanguage, target_lang="EN-US")
            
            self.detectedSourceLanguage = self.outText.detected_source_lang

            if self.detectedSourceLanguage == "ZH":
                # Mandarin or Cantonese Pinyin?
                # Add Pinyin
                if self.cantonese:
                    self.outputPinyin = self.cantonese2pinyin(self.inText)
                else:
                    self.outputPinyin = self.pinyin.get_pinyin(self.inText, splitter=" ", tone_marks="marks")
                # Add simplified Chinese
                if self.showSimplified and self.getLanguage(self.inText) == "zh-TW":
                    self.outputPinyin += f"\n{self.translateGoogle('ZH-CN', self.inText)}"
                self.outText = f"{self.outputPinyin}\n\n" + self.outText.text
        
        # Generate text to speech audio file
        if self.detectedSourceLanguage == "EN":
            googleTTS.cloudTextToSpeech(self.inText, "en-US", "en-US-Wavenet-B", 1)
        elif self.detectedSourceLanguage == "ZH":
            if self.cantonese:
                googleTTS.cloudTextToSpeech(self.inText, "yue-HK", "yue-HK-Standard-B", 1)
            else:
                googleTTS.cloudTextToSpeech(self.inText, "cmn-CN", "cmn-CN-Wavenet-A", 1)
        elif self.detectedSourceLanguage == "DE":
            googleTTS.cloudTextToSpeech(self.inText, "de-DE", "de-DE-Wavenet-B", 1)
        else:
            googleTTS.textToSpeech(self.inText, self.detectedSourceLanguage.lower())

        # Polish up self.outText
        if not isinstance(self.outText, str):
            self.outText = self.outText.text

        # Calculate outputTextSize using "outputLabel" (in order to resize "outputText" text field)
        self.outputLabel = tk.Label(self.outputFrame, text=self.outText, font=self.myFont, bg="white")
        self.outputLabel.place(x=2, y=2)
        self.outputLabel.update()
        self.outputTextSize = [self.outputLabel.winfo_width(), self.outputLabel.winfo_height()]
        self.outputLabel.configure(text="")

        # Set the text to outputText and outputLabel
        self.outputText.insert(1.0, "\n\n" + self.outText)  # Newlines prevent text overlapping w/ "Translate" text
        self.resize()
        if sound_effect:
            self.playSoundEffect("1-Up.mp3")
        
    def resize(self):
        # Update text based on output text
        self.newSize = list(self.minSize)
        # If x of outputText is bigger than x of min window size, newSize = x
        if self.outputTextSize[0] > self.newSize[0]:
            self.newSize[0] = self.outputTextSize[0] + self.borderOutline * 2

            # If x exceeds max value, cap it
            if self.newSize[0] > self.maxSize[0]:
                self.newSize[0] = self.maxSize[0]
                # Since the text in one line exceeds the max window width, shrink font size
                self.outputText.configure(font=self.mySmallFont)
                # Update outputTextSize
                self.outputText.update()
                self.outputTextSize = [self.outputText.winfo_width(), self.outputText.winfo_height()]
        # If y of outputText is greater than height of outputFrame
        # Old: self.outputFrameHeight = self.newSize[1] / 2 + self.textHeight
        # self.inputBoxY = self.margins * 2 + self.buttonHeight
        # self.outputFrameHeight = ((self.newSize[1] - self.inputBoxY) / 2)
        # if self.outputTextSize[1] > self.outputFrameHeight:
        #     print("Vertical resize")
        #     print(self.outText)
        #     # outputFrameHeight needs to be enlarged to outputTextSize[1], to do so, change newSize[1] 
        #     self.newSize[1] = (self.outputTextSize[1] - self.textHeight) * 2
        #     self.newSize[1] =  math.ceil(self.newSize[1])
        #     if self.newSize[1] > self.maxSize[1]:
        #         self.newSize[1] = self.maxSize[1]
        #     print(self.newSize[1])


        # Resize contents: place the elements first, then add margins and resize the whole window
        # Update newSize to fit contents
        self.root.geometry(str(self.newSize[0] + self.margins * 2) + "x" + str(self.newSize[1] + self.margins * 2))
        
        # inputBox should be 1 margin unit from the window top extending directly to the window y (mid-point - textHeight)
        # Place source language text in input box
        self.inputBoxY = self.margins * 2 + self.buttonHeight
        self.inputBoxHeight = ((self.newSize[1] - self.inputBoxY) / 2) - self.textHeight
        self.inputBox.place(x=self.margins, y=self.inputBoxY, width=self.newSize[0], height=self.inputBoxHeight)
        self.inputBox.grid_rowconfigure(0, weight=1)
        self.inputBox.grid_columnconfigure(0, weight=1)
        # tk.Label(self.inputBox, text="Chinese", font=self.myUnderlineFont, justify=tk.LEFT, bg="white").grid(row=0, column=1, padx=10, sticky="se")

        # Create outputFrame, which begins from y (mid-point(not including top bar) - textHeight) + 1 margin unit
        # The place elements into outputFrame
        self.outputFrameY = self.inputBoxY + self.inputBoxHeight + self.margins
        self.outputFrameHeight = ((self.newSize[1] - self.inputBoxY) / 2) + self.textHeight
        self.outputFrame.place(x=self.margins, y=self.outputFrameY, width=self.newSize[0], height=self.outputFrameHeight)
        tk.Label(self.outputFrame, text="Translation:", font=self.myBoldFont, justify=tk.LEFT, bg="white").grid(row=0, column=0, padx=2, pady=2, sticky="nw")
        tk.Label(self.outputFrame, text="English", font=self.myUnderlineFont, justify=tk.LEFT, bg="white").grid(row=0, column=1, padx=2, pady=2, sticky="ne")
        # outputText y value is mid-point + 1 margin unit
        self.outputText.place(x=0, y=0, width=self.newSize[0] - self.borderOutline * 2, height=self.outputFrameHeight - self.borderOutline * 2)
        # Set outputText text field uneditable
        self.outputText.config(state=tk.DISABLED)

    def close(self, event=None):
        self.root.destroy()
    
    def releaseKeys(self):
        # Prevent key-binding bugs
        time.sleep(0.5)
        self.key.release("q")
        self.key.release(Key.alt)

    def closeSettings(self):
        self.settingsWindow.destroy()
        self.settingsWindow = None

    def openSettings(self):
        def saveSettings():
            # Apply changes
            if self.selectedPinyin.get() == "Mandarin":
                self.cantonese = False
            else:
                self.cantonese = True
            self.showSimplified = [False, True][self.selectedShowSimplified.get() == 1]
            self.sourceLanguage = self.language2code(isGoogle=False, language=self.selectedSourceLanguage.get())
            self.settingsWindow.destroy()
            self.soundEffects = [False, True][self.selectedSoundEffect.get() == 1]
            self.playSoundEffect("powerup_appears.wav")
            self.translate()

        # Open a new tkinter window to display settings
        self.settingsWindow = tk.Toplevel(self.root)
        self.settingsWindow.title("Settings")
        # self.settingsWindow.resizable(False, False)
        self.settingsWindow.configure(bg="white")
        self.settingsWindow.focus_force()
        self.settingsWindow.grab_set()
        self.settingsWindow.transient(self.root)
        self.settingsWindow.bind("<Escape>", self.closeSettings)

        # Option 1, Chinese or Cantonese romanization, dropdown menu
        self.selectedPinyin = tk.StringVar()
        if self.cantonese:  # Button shows selected option
            self.selectedPinyin.set("Cantonese")
        else:
            self.selectedPinyin.set("Mandarin")
        # Create option 1 text
        tk.Label(self.settingsWindow, text="Pinyin:     ", font=self.myFont, bg="white").grid(row=0, column=0, padx=2, pady=2, sticky="w")
        # Create option 1 dropdown menu
        self.option1 = tk.OptionMenu(self.settingsWindow, self.selectedPinyin, "Mandarin", "Cantonese")
        self.option1.configure(font=self.myFont)
        self.option1.grid(row=0, column=1, padx=2, pady=2, sticky="w")

        # Option 2, show simplified Chinese
        self.selectedShowSimplified = tk.IntVar()
        self.selectedShowSimplified.set(self.showSimplified)
        # Create option 2 text
        tk.Label(self.settingsWindow, text="Show simplified Chinese:     ", font=self.myFont, bg="white").grid(row=1, column=0, padx=2, pady=2, sticky="w")
        # Create option 2 checkbox
        self.option2 = tk.Checkbutton(self.settingsWindow, text="", bg="white", variable=self.selectedShowSimplified, onvalue=1, offvalue=0)
        self.option2.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Option 3, source language selection, dropdown menu
        self.selectedSourceLanguage = tk.StringVar()
        self.selectedSourceLanguage.set(self.code2language(isGoogle=False, code=self.sourceLanguage))
        # Create option 2 text
        tk.Label(self.settingsWindow, text="Source language:     ", font=self.myFont, bg="white").grid(row=2, column=0, padx=2, pady=2, sticky="w")
        # Create option 2 dropdown menu
        self.option2 = tk.OptionMenu(self.settingsWindow, self.selectedSourceLanguage, "Detect language")
        # Add language options based on DeepL API
        for code, language in self.deeplCodes.items():
            self.option2["menu"].add_command(label=language, command=tk._setit(self.selectedSourceLanguage, language))
        self.option2.configure(font=self.myFont)
        self.option2.grid(row=2, column=1, padx=2, pady=2, sticky="w")

        # Option 4, sound effect toggle, checkbox
        self.selectedSoundEffect = tk.IntVar()
        self.selectedSoundEffect.set(self.soundEffects)
        # Create option 3 text
        tk.Label(self.settingsWindow, text="Sound effects:     ", font=self.myFont, bg="white").grid(row=3, column=0, padx=2, pady=2, sticky="w")
        # Create option 3 checkbox
        self.option3 = tk.Checkbutton(self.settingsWindow, text="", bg="white", variable=self.selectedSoundEffect, onvalue=1, offvalue=0)
        self.option3.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        
        # Save button with some space above it
        tk.Label(self.settingsWindow, text="", font=self.myFont, bg="white").grid(row=3, column=0, padx=2, pady=2)
        tk.Button(self.settingsWindow, text="Save Changes", font=self.myFont, command=saveSettings).grid(row=4, column=1, padx=2, pady=2, sticky="sw")

# Testing purposes
def main():
    widget = Widget()
    text0 = "大手牽"
    text1 = "安靜的夜晚裡 頭腦還不想停"
    text2 = "你說藍色是你最愛的顏色 你說如果沒有愛那又如何"
    text3 = "一二三四五六七 使出必殺技，哥能否追到你，七六五四三二一，真的太可惜，喜歡的人不是你"
    text4 = "愁看殘紅亂舞 憶花底初度逢 難禁垂頭淚湧 此際幸月朦朧 愁悴如何自控 悲哀都一樣同 情意如能互通 相分不必相送"
    text5 = "安靜的夜晚裡 頭腦還不想停\n我還騎著腳踏車載著妳\n潜入了大海裡 我笑著看著妳\n片段的回憶抓著我的心\n緣分還是第一 像悲劇的電影\n我學會至少我們擁有了會經\n這是我的決定\n決定把我們變成美好的記憶\n妳付出愛我的時候\n擁抱妳的人還是我\n爭吵時我都不會走"
    widget.open(inText=text2)

def welcomeUser():
    widget = Widget()
    widget.welcome()

if __name__ == "__main__":
    main()
    # welcomeUser()


# Make it so that you can show or hide window