import tkinter as tk
import serial
# importing the choosecolor package
from tkinter import colorchooser


class Controls(tk.Frame):
    BUTTON_WIDTH = 15

    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.create_btns_frame()
        self.create_new_macro_frame()
        self.parent.title("2800 Team Project")


    def create_btns_frame(self):
        #Define button font
        button_font = ("Berlin Sans FB Demi", 25)
        button_fg_color = "white"
        bg_colour = "light blue"

        self.btnsFrame = tk.Frame(self.parent)
        self.existingMacroPressBtn = tk.Button(self.btnsFrame, text="Existing Macros",
                                          width=self.BUTTON_WIDTH,
                                          command=self.existingMacroPress,
                                          bg=bg_colour,
                                          font=button_font,
                                          fg=button_fg_color)
        self.existingMacroPressBtn.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        
        brightnessFrame=tk.Frame(self.btnsFrame)
        brightnessLabel = tk.Label(brightnessFrame, text="Brightness:",
                                       width=self.BUTTON_WIDTH,
                                       bg=bg_colour,
                                       font=button_font,
                                       fg=button_fg_color)
        brightnessLabel.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.brightnessEntry = tk.Entry(brightnessFrame,
                                       font=("Berlin Sans FB Demi", 15))
        self.brightnessEntry.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=40)
        brightnessFrame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        brightnessFrame.config(bg="light blue")
        self.btnsFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def create_new_macro_frame(self):
        BUTTON_WIDTH = 15
        button_font = ("Berlin Sans FB Demi", 15)
        button_fg_color = "white"
        bg_colour = "light blue"

        # Frame to hold the DEMO 1 entry/label widgets
        self.entryFrame = tk.Frame(self.parent)
        
        self.macroLabel = tk.Label(self.entryFrame, text="Macro Name:",
                                       font=button_font)
        self.macroLabel.pack(side=tk.LEFT)
        
        self.macroEntry = tk.Entry(self.entryFrame,
                                   font=button_font)
        self.macroEntry.pack(side=tk.LEFT)
        
        self.capMacro = tk.Label(self.entryFrame, text="Capitalised macro",
                                       font=button_font)
        self.capMacro.pack(side=tk.LEFT)
        
        self.entryFrame.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER, padx=50)

        # Frame to hold the DEMO 1 entry/label widgets
        self.buttonFrame = tk.Frame(self.parent)
        self.readBtn = tk.Button(self.buttonFrame, text="Read", width=BUTTON_WIDTH, command=self.readBtnPress,
                                       bg=bg_colour,
                                       font=button_font,
                                       fg=button_fg_color)
        self.readBtn.pack()
        self.writeBtn = tk.Button(self.buttonFrame, text="Write", width=BUTTON_WIDTH, command=self.writeBtnPress,
                                       bg=bg_colour,
                                       font=button_font,
                                       fg=button_fg_color)
        self.writeBtn.pack()
        self.buttonFrame.pack(fill=tk.BOTH, expand=True, padx=190)


    def readBtnPress(self):
        macroName = self.macroEntry.get()  # Get the entered macro name
        brightnessLevel = self.brightnessEntry.get()
        print("Read pressed for macro:", macroName, "Brightness level:", brightnessLevel)

    def writeBtnPress(self):
            new_text = self.macroEntry.get().upper()  # Get the entered macro name and capitalize it
            self.capMacro.config(text=new_text)  # Change the text of the label


    def backBtnPress(self):

        self.clear_buttons()

        self.create_btns_frame()
        self.create_new_macro_frame()

    def backBtnCreate(self):
        button_font = ("Berlin Sans FB Demi", 15)
        self.backBtn = tk.Button(self.parent, text="Back", width=self.BUTTON_WIDTH,
                                 font=button_font,
                                 command=self.backBtnPress)
        self.backBtn.pack(side=tk.BOTTOM, anchor=tk.W)

    def existingMacroPress(self):
        self.clear_buttons()
        self.backBtnCreate()

        mainFrame=tk.Frame(self.parent)

        macroBtnFrame = tk.Frame(mainFrame)
        self.macroBtns = {} #each button will be stored in here. LATER CHANGE TO DICT AND STORE INSTRUCTIONS
        for i in range(1, 11):
            macro = self.newMacroBtn(macroBtnFrame, str(i))
            self.macroBtns[i] = macro
        macroBtnFrame.pack(side=tk.LEFT, anchor=tk.CENTER)

        RGBFrame = tk.Frame(mainFrame)
        self.RGBBtns = {}
        numbers = [i for i in range(1, 11)]
        for x in numbers:
            self.RGBBtns[x] = tk.Button(RGBFrame, width=self.BUTTON_WIDTH,
                                       bg="white",
                                       command = lambda y = x: self.chooseColour(y),
                                       pady=9)
            print(x)
            self.RGBBtns[x].pack()
        RGBFrame.pack(side=tk.LEFT, anchor=tk.CENTER)
        print("end of loop")
        print(self.RGBBtns.keys())
        mainFrame.pack()

    def chooseColour(self, number):
        color_code = colorchooser.askcolor(title ="Choose color")
        print(color_code[1])
        self.RGBBtns[number].configure(bg=color_code[1])
        print(number)


    def newMacroBtn(self, frame, number):
        button_font = ("Berlin Sans FB Demi", 15)
        self.macroBtn = tk.Button(frame, text = "Macro " + number, width=self.BUTTON_WIDTH, command=self.macroInstructions,
                                       font=button_font)
        self.macroBtn.pack()
        return self.macroBtn.config('text')[-1]

    def macroInstructions(self):
        self.clear_buttons()
        self.backBtnCreate()
        self.backBtn.config(command=self.existingMacroPress)

        actions = ""
        macroInstructionsFrame = tk.Frame(self.parent)
        macroInstructionsFrame.pack()
        for i in range (1, 21):
            action = "action " + str(i)
            macroInstructionsLabel = tk.Label(macroInstructionsFrame, text = action)
            macroInstructionsLabel.pack()
            actions += action + " -> "
        lastAction = "action 21"
        macroInstructionsLabel = tk.Label(macroInstructionsFrame, text = lastAction)
        macroInstructionsLabel.pack()
        actions += lastAction

        macroInstructionsFrame = tk.Frame(self.parent)
        macroInstructionsFrame.pack()

    def clear_buttons(self):
        for widgets in self.parent.winfo_children():
            widgets.destroy()

class GameApp(object):
    

    def __init__(self, master):
        BUTTON_WIDTH = 15
        button_font = ("Berlin Sans FB Demi", 15)
        button_fg_color = "white"
        bg_colour = "light blue"

        master.title("2800 Team Project")
        
        controls = Controls(master)
        controls.pack(side=tk.LEFT, fill=tk.Y)

root = tk.Tk()
root.geometry("1000x500")
#root.configure(bg="white")
app = GameApp(root)
root.mainloop()