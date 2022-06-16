from fnmatch import translate
import tkinter as tk
from tkinter import messagebox
from tkinter import font
import deepl
from internetConnection import isConnected

class Widget():
    def __init__(self) -> None:
        self.debugMode = False
        
        # width x height
        self.minSize = (400, 250)
        self.maxSize = (600, 500)
        self.inText = None
        self.outText = None

        # Initialize deepL API
        self.key = ""
        with open("deepL auth.txt", "r") as f:
            self.key = f.read()
        self.translator = deepl.Translator(self.key)

        # Other variables
        self.connected = True

    def open(self, inText=""):
        # Initialize window
        self.root = tk.Tk()
        self.root.title("Screen OCR")
        self.root.iconbitmap("icon.ico")
        self.root.geometry(str(self.minSize[0]) + "x" + str(self.minSize[1]))
        self.root.focus()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.resizable(False, False)

        # Set variables
        self.inText = inText
        self.outText = tk.StringVar()
        self.myFont = ("Arial", 12)
        self.textHeight = self.myFont[1] * 1.75

        # Button
        self.translateButton = tk.Button(self.root, text="Translate", command=self.translate)
        # Place button at bottom right corder
        self.translateButton.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        # Input text
        self.inputBox = tk.Text(self.root, font=self.myFont)
        self.inputBox.place(x=0, y=0, width=self.minSize[0], height=self.minSize[1] / 2 - self.textHeight)
        self.inputBox.insert(tk.END, inText)

        # Output Text
        # Set outputText's "textvariable" to "outText", then translate
        # Translate text, then set the label accordingly
        self.outputText = tk.Label(self.root, textvariable=self.outText, font=self.myFont, justify=tk.LEFT)
        self.outputText.place(x=0, y=self.minSize[1] / 2)
        self.translate()

        # Key bindings
        self.root.bind("<Escape>", self.close)
        self.root.bind("<Return>", self.translate)


        # Open widget if connected, otherwise close it
        if self.connected or self.debugMode:
            self.root.mainloop()
        else:
            self.close()
        
        
    
    def translate(self, event=None):
        # Update "self.inText"
        self.inText = self.inputBox.get(1.0, tk.END)

        # No text error handling
        if self.inText == "":
            messagebox.showwarning(title="Error", message="Text field cannot be empty!")
            return

        # Check if there's internet connnection
        if isConnected():
            # Get text from textbox and set it as the outText variable
            if self.debugMode:
                self.targetText = "Translation"
            else:
                self.targetText = self.translator.translate_text(self.inText, source_lang="ZH", target_lang="EN-US")
            # Set the text ok the label
            self.outText.set(self.targetText)
            self.resize()
        else:
            self.connected = False
            messagebox.showwarning(title="Error", message="No Internet connection!")
        
    def resize(self):
        # Update outputTextSize upon "outputText" change
        self.outputText.update()
        self.outputTextSize = [self.outputText.winfo_width(), self.outputText.winfo_height()]
        
        # Update size based on texts
        self.newSize = list(self.minSize)
        # If x of text is bigger than x of newSize, newSize = x
        if self.outputTextSize[0] > self.newSize[0]:
            # If x exceeds max value, cap it
            if self.newSize[0] > self.maxSize[0]:
                self.newSize[0] = self.maxSize[0]
            self.newSize[0] = self.outputTextSize[0]
        # Do same thing with y
        if self.outputTextSize[1] > self.newSize[1]:
            if self.newSize[1] > self.maxSize[1]:
                self.newSize[1] = self.maxSize[1]
            self.newSize[1] = self.outputTextSize[1]

        #Update newSize to fit contents
        self.root.geometry(str(self.newSize[0]) + "x" + str(self.newSize[1]))
        #Resize contents
        self.inputBox.place(x=0, y=0, width=self.newSize[0], height=self.newSize[1] / 2 - self.textHeight)


    
    def close(self, event=None):
        self.root.destroy()

def main():
    widget = Widget()
    widget.open(inText="其实一切都如故")

if __name__ == "__main__":
    main()


# Make it so that you can show or hide window