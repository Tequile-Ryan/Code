import tkinter as tk
from tkinter import Menu
import tkinter.scrolledtext as st
from tkinter.filedialog import askopenfilename, asksaveasfilename
import serial
from serial.tools import list_ports
# importing the choosecolor package
from tkinter import colorchooser
from tkinter import ttk
from tkinter import messagebox
import keyboard
import time
import threading
from typing import List
import pyautogui
import json
from functools import partial
import MacroToHid
import KeyboardLayout
import copy
from PIL import Image, ImageTk
import ProtocolRead
import Protocol


class GUI(tk.Frame):
    """
    Creates the whole GUI and implements all logic for it.
    """
    BUTTON_WIDTH = 15

    def __init__(self, parent):
        """Instantialises the GUI class

        Args:
            parent: The instance of the GUI application.
        """
        super().__init__(parent)

        self.dataInitialize()
        # convert into json string
        self.jsonData = json.dumps(self.data,indent=4)
        self.selectedPort = None
        self.parent = parent
        """self.create_btns_frame()
        self.create_new_macro_frame()"""
        self.PortSelectionPage()
        self.parent.title("2800 Team Project")
        self.ListPortsInitially()
        self.filename = ""  # initialize filename
        # Store protocol in a bytearray 545 bytes long
        self.protocol = bytearray(b'\xff') * 545

    def dataInitialize(self):
        """Initialises the data with a default initial delay
        of 500 and repeat delay of 100.
        """
        self.data = {}
        self.data["initial delay"] = "0500"
        self.data["repeat delay"] = "0100"
        self.data["brightness"] = "00"
        for num in range(1,11):
            self.data[f"macro {num}"] = {"macro name": f"macro {num}",
                                         "macro": [""],
                                         "colour": [0,0,0]}

    def PortSelectionPage(self):
        """Create the page for connecting to a port and include
        functionality to refresh the list of available ports.
        """
        BUTTON_WIDTH = 13
        KEY_WIDTH = 5
        TITLE_FONT = ("Berlin Sans FB Demi", 40)
        button_font = ("Berlin Sans FB Demi", 14)
        button_fg_color = "white"
        bg_colour = "light blue"
        keyFont = ("Berlin Sans FB Demi", 20)
        # Frame to hold port functionality
        self.SerialFrame = tk.Frame(self.parent)

        try:
            imageFile = Image.open("GG.jpg")
            smaller_image = imageFile.resize((150, 150))
            smaller_image.save("small_GG.jpg")
            self.photo = ImageTk.PhotoImage(smaller_image)
            for row in range(10):
                for col in range(20):
                    label = tk.Label(self.SerialFrame, image=self.photo, width=150, height=150)
                    label.place(x=col * 150, y=row * 150)
        except FileNotFoundError:
            print("GG")

        self.Portlabel = tk.Label(self.SerialFrame, text="Select a port:",
                                  font=button_font)
        self.Portlabel.pack(anchor=tk.S, expand=True)
        # Create a combobox that will allow selection from a list of serial ports
        self.portCombobox = ttk.Combobox(self.SerialFrame)
        self.portCombobox.pack(anchor=tk.N, side=tk.TOP, expand=True)
        self.SerialFrame.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER, padx=50)
        # self.PortsBtnFrame = tk.Frame(self.SerialFrame)
        self.refreshBtn = tk.Button(self.SerialFrame, text="Refresh", width=BUTTON_WIDTH,
                                    command=self.PortsRefreshing,
                                    bg=bg_colour,
                                    font=button_font,
                                    fg=button_fg_color)
        self.refreshBtn.pack()
        self.connectBtn = tk.Button(self.SerialFrame, text="Connect", width=BUTTON_WIDTH,
                                    command=self.PortsConnecting,
                                    bg=bg_colour,
                                    font=button_font,
                                    fg=button_fg_color)
        self.connectBtn.pack()
        self.cBtn = tk.Button(self.SerialFrame, text="Connect", width=BUTTON_WIDTH,
                              command=self.LetsGo,
                              bg=bg_colour,
                              font=button_font,
                              fg=button_fg_color)
        self.cBtn.pack()
        # self.PortsBtnFrame.pack(fill=tk.BOTH, expand=True, padx=50)

    def LetsGo(self):
        """Takes user to the macro page
        """
        self.clear_buttons()
        self.create_btns_frame()
        self.create_new_macro_frame()

    def create_btns_frame(self):
        """Creates the left hand side of the macro page that allows the user to edit
        GUI configurations.
        """
        button_font = ("Berlin Sans FB Demi", 25)
        other_button_font = ("Berlin Sans FB Demi", 15)
        enter_btn_font = ("Berlin Sans FB Demi", 17)
        auto_font = ("Berlin Sans FB Demi", 15)
        button_fg_color = "white"
        bg_colour = "light blue"
        repeatBtnWidth = 20
        repeatEntryWidth = 5

        # Frame all the components on the left of the main
        # screen will be situated in
        self.btnsFrame = tk.Frame(self.parent)

        # Repeat delay and Repeat rate frame
        self.repeatFrame = tk.Frame(self.btnsFrame, highlightbackground="black", highlightthickness=1,
                                    bg=bg_colour)
        self.repeatFrame.pack(fill=tk.X, ipady=90)

        # Create frames within repeatFrame for layout purposes.
        self.repeatFrame1 = tk.Frame(self.repeatFrame,
                                     bg=bg_colour)
        self.repeatFrame1.pack(expand=True, fill=tk.BOTH, anchor=tk.S)
        self.repeatFrame2 = tk.Frame(self.repeatFrame,
                                     bg=bg_colour)
        self.repeatFrame2.pack(expand=True, fill=tk.BOTH)

        self.initialDelayLabel = tk.Label(self.repeatFrame1, text="Initial Repeat Delay: ",

                                          bg=bg_colour,
                                          font=other_button_font,
                                          fg=button_fg_color)
        self.initialDelayLabel.pack(side=tk.LEFT, expand=True, anchor=tk.SE)
        # User should not be able to enter more than 4 characters
        self.initialDelayLenCheck = self.register(self.delayLenCheck)
        self.initialDelayEntry = tk.Entry(self.repeatFrame1, validate="key",
                                          validatecommand=(self.initialDelayLenCheck, "%P"),
                                          font=other_button_font,
                                          width=repeatEntryWidth)
        self.initialDelayEntry.bind("<Return>", lambda event: self.enterRepeat())
        self.initialDelayEntry.pack(side=tk.LEFT, expand=True, anchor=tk.SW)
        # Ensure latest initial delay entered is always displayed
        self.initialDelayEntry.insert(0, str(int(self.data["initial delay"])))
        self.repeatRateLabel = tk.Label(self.repeatFrame2, text="Repeat Rate: ",

                                        bg=bg_colour,
                                        font=other_button_font,
                                        fg=button_fg_color)
        self.repeatRateLabel.pack(side=tk.LEFT, expand=True, anchor=tk.E)
        # User should not be able to enter more than 4 characters
        self.repeatRateLenCheck = self.register(self.delayLenCheck)
        self.repeatRateEntry = tk.Entry(self.repeatFrame2, validate="key",
                                        validatecommand=(self.repeatRateLenCheck, "%P"),
                                        font=other_button_font,
                                        width=repeatEntryWidth)
        self.repeatRateEntry.bind("<Return>", lambda event: self.enterRepeat())
        self.repeatRateEntry.pack(side=tk.LEFT, expand=True, anchor=tk.W)
        self.delayErrorLabel = tk.Label(self.repeatFrame, text="",
                                        bg=bg_colour,
                                        font=other_button_font,
                                        fg="#ff0000")
        self.delayErrorLabel.pack(anchor=tk.S)
        # Ensure latest repeat rate entered is always displayed
        self.repeatRateEntry.insert(0, str(int(self.data["repeat delay"])))
        self.repeatEnterBtn = tk.Button(self.repeatFrame, text="Enter",
                                        command=self.enterRepeat,
                                        font=enter_btn_font)
        self.repeatEnterBtn.pack(anchor=tk.S, ipadx=40)

        brightnessFrame = tk.Frame(self.btnsFrame, highlightbackground="black", highlightthickness=1)
        self.brightnessLabel = tk.Label(brightnessFrame, text="Brightness: ",
                                        width=self.BUTTON_WIDTH,
                                        bg=bg_colour,
                                        font=button_font,
                                        fg=button_fg_color)
        self.brightnessLabel.pack(expand=True, anchor=tk.S)
        brightnessFrame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        brightnessFrame.config(bg="light blue")
        self.btnsFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        # Ensure latest brightness entered is always displayed
        self.brightnessValueLabel = tk.Label(brightnessFrame, text=str(int(self.data["brightness"])),
                                             width=self.BUTTON_WIDTH,
                                             bg=bg_colour,
                                             font=button_font,
                                             fg=button_fg_color)
        self.brightnessValueLabel.pack(expand=True, anchor=tk.S)
        # Create a Scale widget
        self.slider = tk.Scale(brightnessFrame, command=self.saveBrightness,
                               from_=0,
                               to=10,
                               orient="horizontal",
                               length=300)
        self.slider.set(int(self.data["brightness"]))
        self.slider.pack(expand=True, side=tk.TOP, anchor=tk.N)

    def enterRepeat(self):
        #savedBrightness = self.protocol[:2]
        initialDelay = self.initialDelayEntry.get()
        repeatDelay = self.repeatRateEntry.get()
        # User should only be able to enter a number
        if (not initialDelay.isdigit() or not repeatDelay.isdigit()) and initialDelay != "" and repeatDelay != "":
            self.delayErrorLabel.config(text="Please enter only number")
        elif initialDelay == "" or repeatDelay == "" or int(initialDelay) <= 50 or int(repeatDelay) <= 50:
            self.delayErrorLabel.config(text="The minimum time period is 51(ms)")
        else:
            """initialDelay = f"{int(initialDelay):04}"
            repeatDelay = f"{int(repeatDelay):04}" """
            self.delayErrorLabel.config(text="")
            
            # Check if the length of the initial repeat delay is less than 4
            if len(initialDelay) < 4:
                # Calculate the number of zeros needed to make the stored value of length 4 for the protocol
                zeros_needed = 4 - len(initialDelay)
                # Add the zeros in front of the number
                initialDelay = "0" * zeros_needed + initialDelay

        # Check if the length of the initial repeat delay is less than 4
            if len(repeatDelay) < 4:
                # Calculate the number of zeros needed to make the stored value of length 4 for the protocol
                zeros_needed = 4 - len(repeatDelay)
                # Add the zeros in front of the number
                repeatDelay = "0" * zeros_needed + repeatDelay

            try:
                # Overwrite new data to the json file and self.data
                f = open(self.filename, 'r')
                self.jsonData = json.load(f)
                f.close()
                self.data = self.jsonData
                if "initial delay" in self.data:
                    del self.data["initial delay"]
                self.data["initial delay"] = initialDelay
                if "repeat delay" in self.data:
                    del self.data["repeat delay"]
                self.data["repeat delay"] = repeatDelay
                self.jsonData = json.dumps(self.data, indent=4)
                """CopyD = copy.deepcopy(self.data)
                self.dataInHid = MacroToHid.create_data(CopyD)"""
                f = open(self.filename, 'w')
                f.write(f"{self.jsonData}")
                f.close()
            except FileNotFoundError:
                # Continue to overrite new data into self.data even
                # if no file is chosen
                if "initial delay" in self.data:
                    del self.data["initial delay"]
                self.data["initial delay"] = initialDelay
                if "repeat delay: " in self.data:
                    del self.data["repeat delay"]
                self.data["repeat delay"] = repeatDelay
                self.jsonData = json.dumps(self.data, indent=4)
                CopyD = copy.deepcopy(self.data)
                self.dataInHid = MacroToHid.create_data(CopyD)
            # self.protocol = savedBrightness + initialDelay + repeatDelay
            # self.protocol = Protocol.createProtocol(self.protocol, self.dataInHid)

            print(self.dataInHid)
            print(self.protocol)

            # index position 1 of protocol to be the hex value of
            # the first two digits of the initial delay.
            # self.protocol[1:2] = bytearray.fromhex(str(initialDelay[0:2]))

            # index position 2 of protocol to be the hex value of
            # the last two digits of the initial delay.
            # self.protocol[2:3] = bytearray.fromhex(str(initialDelay[2:4]))

            # Same logic as for intial delay
            # self.protocol[3:4] = bytearray.fromhex(str(repeatDelay[0:2]))
            # self.protocol[4:5] = bytearray.fromhex(str(repeatDelay[2:4]))

    def create_new_macro_frame(self):
        """
        Create the right hand side of the main configurations page.
        """
        BUTTON_WIDTH = 13
        KEY_WIDTH = 5
        TITLE_FONT = ("Berlin Sans FB Demi", 40)
        button_font = ("Berlin Sans FB Demi", 14)
        button_fg_color = "white"
        bg_colour = "light blue"
        keyFont = ("Berlin Sans FB Demi", 20)

        # Frame to hold the DEMO 1 entry/label widgets
        self.entryFrame = tk.Frame(self.parent)

        self.titleLabel = tk.Label(self.entryFrame, text="Macrolyze", font=TITLE_FONT)
        self.titleLabel.pack()

        """self.macroLabel = tk.Label(self.entryFrame, text="Macro Name:",
                                   font=button_font)
        self.macroLabel.pack(side=tk.LEFT)

        self.macroEntry = tk.Entry(self.entryFrame,
                                   font=button_font)
        self.macroEntry.pack(side=tk.LEFT)"""

        """self.capMacro = tk.Label(self.entryFrame, text="Capitalised macro",
                                 font=button_font)
        self.capMacro.pack(side=tk.LEFT)"""

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

        # Frame to hold port connection and keyboard
        self.keyAndPortFrame = tk.Frame(self.parent)
        self.keyAndPortFrame.pack(fill=tk.BOTH, expand=True)

        # Frame to hold keyboard button
        self.keyboardFrame = tk.Frame(self.keyAndPortFrame)
        self.keyboardFrame.pack(side=tk.LEFT, expand=True)

        buttons = []
        self.keys = {}
        count = 0
        # Create each configurable macro key
        for row in range(3):
            button_row = []
            for col in range(4):
                count += 1
                # These are the two switches on the keyboard according 
                # to the spec to be used for: "auxiliary functionality
                # as necessary to implement the rest of this specification."
                if row == 2 and (col == 2 or col == 3):
                    button = tk.Button(self.keyboardFrame,
                                       font=keyFont,
                                       width=KEY_WIDTH,
                                       height=1,
                                       bg="white")
                    button.grid(row=row, column=col, padx=5, pady=5)
                    button_row.append(button)
                    self.keys[count] = button
                # The 10 configurable macro keys
                else:
                    button = tk.Button(self.keyboardFrame, text=str(count),
                                       font=keyFont,
                                       command=partial(self.keyPress, count),
                                       width=KEY_WIDTH,
                                       height=1,
                                       bg="white")
                    button.grid(row=row, column=col, padx=5, pady=5)
                    button_row.append(button)
                    self.keys[count] = button
            buttons.append(button_row)
        """
        # Frame to hold port functionality
        self.SerialFrame = tk.Frame(self.keyAndPortFrame)

        self.Portlabel = tk.Label(self.SerialFrame, text="Select a port:",
                                  font=button_font)
        self.Portlabel.pack(anchor=tk.S, expand=True)
        self.portCombobox = ttk.Combobox(self.SerialFrame)
        self.portCombobox.pack(anchor=tk.N, side=tk.TOP, expand=True)
        self.SerialFrame.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER, padx=50)

        self.PortsBtnFrame = tk.Frame(self.keyAndPortFrame)
        self.refreshBtn = tk.Button(self.PortsBtnFrame, text="Refresh", width=BUTTON_WIDTH,
                                    command=self.PortsRefreshing,
                                    bg=bg_colour,
                                    font=button_font,
                                    fg=button_fg_color)
        self.refreshBtn.pack()
        self.connectBtn = tk.Button(self.PortsBtnFrame, text="Connect", width=BUTTON_WIDTH,
                                    command=self.PortsConnecting,
                                    bg=bg_colour,
                                    font=button_font,
                                    fg=button_fg_color)
        self.connectBtn.pack()
        self.PortsBtnFrame.pack(fill=tk.BOTH, expand=True, padx=50)
        """

        # Menu provides options for loading and saving to a file
        menubar = Menu(self.parent)
        root.config(menu=menubar)
        file_menu = Menu(menubar)
        file_menu.add_command(label='Open',
                              command=self.fileRead)
        file_menu.add_command(label='Save As',
                              command=self.fileWrite)
        file_menu.add_command(label='Exit',
                              command=root.destroy)
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

    def keyPress(self, num: any):
        """
        The user is taken to this page when they click 
        on a macro key to configure/view.

        Args:
            num: The number corresponding to the macro
            key pressed
        """
        BUTTON_WIDTH = 13
        KEY_WIDTH = 5
        label_font = ("Berlin Sans FB Demi", 20)
        button_font = ("Berlin Sans FB Demi", 30)
        small_button_font = ("Berlin Sans FB Demi", 17)
        button_fg_color = "white"
        bg_colour = "light blue"
        keyFont = ("Berlin Sans FB Demi", 20)

        # clear everything to create a new page
        self.clear_buttons()
        self.backBtnCreate()

        # Previous macro frame
        previousFrame = tk.Frame(self.parent, bg=bg_colour)
        previousFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor=tk.CENTER)

        previousLabel = tk.Label(previousFrame, text="Previous Macro Configuration", font=label_font)
        previousLabel.pack()

        self.macroNameLabel = tk.Label(previousFrame, text="Macro Name: ", font=label_font, wraplength=600)
        self.macroNameLabel.pack()

        macroSequenceLabel = tk.Label(previousFrame, text="Macro Sequence: ", font=label_font)
        macroSequenceLabel.pack()

        self.text_area = st.ScrolledText(previousFrame,
                                         width=40,
                                         height=8,
                                         font=("Times New Roman",
                                               15))

        self.text_area.pack()

        actions = ""
        for i in range(1, 22):
            action = "\taction " + str(i)
            actions += action + "\n"

        # Inserting Text which is read only
        self.text_area.insert(tk.INSERT, actions)
        self.text_area.configure(state='disabled')

        self.RGBColourLabel = tk.Label(previousFrame, text="Colour: ", font=label_font)
        self.RGBColourLabel.pack()

        userFrame = tk.Frame(self.parent)
        userFrame.pack(side=tk.LEFT, expand=True)

        # Frame for entry labels
        macroNameFrame = tk.Frame(userFrame)
        macroNameFrame.pack(side=tk.TOP, anchor=tk.W, expand=True)
        errorFrame = tk.Frame(userFrame)
        errorFrame.pack(side=tk.TOP, anchor=tk.W, expand=True)
        macroFrame = tk.Frame(userFrame)
        macroFrame.pack(side=tk.TOP, anchor=tk.W, expand=True)
        colourFrame = tk.Frame(userFrame)
        colourFrame.pack(side=tk.TOP, anchor=tk.W, expand=True)

        self.MacroNameLabel = tk.Label(macroNameFrame, text="Macro Name: ", font=label_font)
        self.MacroNameLabel.pack(side=tk.LEFT)
        self.MacroSeqLabel = tk.Label(macroFrame, text="Macro Sequence:            ", font=label_font,
                                      fg="black")
        self.MacroSeqLabel.pack(side=tk.LEFT,pady=20)
        RGBLabel = tk.Label(colourFrame, text="Colour:                                  ", font=label_font)
        RGBLabel.pack(side=tk.LEFT)

        # initialize macro
        self.macro = []
        # Frame for entry widgets
        self.macroNameLenCheck = self.register(self.NameLenCheck)
        self.macroNameEntry = tk.Entry(macroNameFrame, validate="key", validatecommand=(self.macroNameLenCheck, "%P"),
                                       font=label_font)
        self.macroNameEntry.bind("<Return>", lambda event, n=num: self.macroCreate(n))
        self.macroNameEntry.pack()
        self.macroNameErrorLabel = tk.Label(errorFrame, text="                              ",
                                            font=small_button_font,
                                            fg="#ff0000")
        self.macroNameErrorLabel.pack(side=tk.TOP)
        macroEditBtnFrame = tk.Frame(macroFrame)
        macroEditBtnFrame.pack(side=tk.TOP, anchor=tk.S, expand=True)
        self.recordState = False
        self.MacroRecordBtn = tk.Button(macroEditBtnFrame, width=BUTTON_WIDTH,
                                        text="Record Macro",
                                        command=lambda n=num: self.keyRecordTread(n),
                                        font=small_button_font,
                                        bg=bg_colour,
                                        fg=button_fg_color)
        self.MacroRecordBtn.pack()
        """StopBtn = tk.Button(macroEditBtnFrame, width=BUTTON_WIDTH,
                            text="Stop recording",
                            command=self.stopRecording,
                            font=small_button_font,
                            bg=bg_colour,
                            fg=button_fg_color)
        StopBtn.pack()"""

        self.RGBChooseBtn = tk.Button(colourFrame, width=self.BUTTON_WIDTH,
                                      bg="white",
                                      command=lambda: self.ChooseColour(num),
                                      pady=9)
        self.RGBChooseBtn.pack(pady=60)

        ''' initialize data
            if the file has been opened, data will be read from the file
            else data should be a null dictionary 
        '''
        if self.filename != "":
            f = open(self.filename, 'r')
            self.data = json.load(f)
            f.close()
        CopyD = copy.deepcopy(self.data)
        self.dataInHid = MacroToHid.create_data(CopyD)
        print(self.data)
        if f"macro {num}" in self.data:
            # notice that here self.colour is a tuple, but after converting into json, it will be an array
            self.colour = tuple(self.data[f"macro {num}"]["colour"])
            self.macroName = self.data[f"macro {num}"]["macro name"]
            self.macro = self.data[f"macro {num}"]["macro"]
            if self.macroNameEntry.get() == "":
                self.macroNameEntry.insert(0, self.macroName)
            self.colourHex = f"#{self.colour[0]:02X}{self.colour[1]:02X}{self.colour[2]:02X}"
            self.RGBChooseBtn.configure(bg=self.colourHex)
            self.macroNameLabel.config(text="Macro Name: " + self.macroName)
            self.RGBColourLabel.config(text="Colour: " + f"{self.colour}")
            self.updateAction()

        # Create macro button
        self.createMacroBtn = tk.Button(userFrame, text="Create Macro",
                                   command=partial(self.macroCreate, num),
                                   font=button_font,
                                   bg=bg_colour,
                                   fg=button_fg_color,)
        self.createMacroBtn.pack(side=tk.BOTTOM)

    def NameLenCheck(self,macro_name):
        """Return true if length of macro name less than 30 chars
        
        Args:
            macro_name: The name of the macro
        """
        if len(macro_name) <= 30:
            return True
        else:
            return False

    def delayLenCheck(self,delay):
        """Return true if length of delay less than 4 chars
        
        Args:
            macro_name: The delay entered
        """
        if len(delay) <= 4:
            return True
        else:
            return False

    def keyRecordTread(self,num):
        """Creates a thread to avoid interrupting by the keyboard
        module

        Args:
            num: The number of the macro
        """
        if not self.recordState:
            self.is_recording = True
            self.macro = [""]
            self.recording_thread = threading.Thread(target=lambda n=num: self.keyRecord(n))
            self.recording_thread.start()
            self.createKeyboard(num)
            self.text_area.config(state="normal")
            self.text_area.delete(1.0, tk.END)
            self.text_area.config(state="disabled")
            self.MacroRecordBtn.configure(text="Stop Recording")
            self.createMacroBtn.configure(state="disabled")
            self.RGBChooseBtn.configure(state="disabled")
            self.MacroSeqLabel.config(text="Stop recording =>            ",
                                      fg="red")
        else:
            self.stopRecording()
            self.MacroRecordBtn.configure(text="Record Macro")
            self.createMacroBtn.configure(state="normal")
            self.RGBChooseBtn.configure(state="normal")
            self.MacroSeqLabel.config(text="Macro Sequence:            ",
                                      fg="black")
        self.recordState = not self.recordState

    ''' the main loop of key recording:
        keyboard.read_event() is to get the action and when this function works, the program will wait for it to run.
        Then use self.act to obtain the action.
        Use macroPressLimit function to check if the action is legal.
        Also, when pressing stop record or after record 20 keys (macroNumLimit function), self.is_recording will be
        False. Then keyRecord will be over. 
        If the action is legal, the action should be displayed on the text box and then appended into an array where
        store the macro.
        Lastly, checkReleasing function just release all keys that haven't been released.
        (By the way, in stopRecording function, keyboard press function from another module pyautogui is used
        to create an action (this action will not be recorded) for keyboard.read_event() to end this loop. This is
        because keyboard.read_event() cannot be skipped (though stop button is pressed, stop button cannot stop
        the current loop).)
    '''
    def keyRecord(self,num):
        while self.is_recording:
            # when recording, macro name can't be written
            self.macroNameEntry.config(state="disabled")
            event = keyboard.read_event()
            self.act = f"{event.name} {event.event_type}"
            self.macroPressLimit()
            if self.is_recording and not self.repeat and self.isNotReleased < 7 and self.isPressed:
                print(self.isNotReleased)
                if "" in self.macro:
                    self.macro.remove("")
                self.macro.append(self.act)
                self.updateAction()
            self.macroNumLimit()
        self.isMacroBlank()
        self.macroNameEntry.config(state="normal")
        self.checkReleasing()
        self.macroCreate(num)

    def isMacroBlank(self):
        """Ensures that if there is no macro sequence specified for
        that macro, no macro sequence is displayed. 
        """
        if self.macro == [""]:
            self.text_area.config(state="normal")
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END,"")
            self.text_area.config(state="disabled")

    def checkReleasing(self):
        """Release all keys that haven't been released."""

        """for i in range(0, len(self.macro)):
            downPosition = self.macro[i].rfind("down")
            if downPosition != -1:
                eventName = self.macro[i][0: downPosition - 1]
                isReleased = False
                for j in range(i, len(self.macro)):
                    if eventName in self.macro[j] and self.macro[j].endswith("up"):
                        isReleased = True
                if not isReleased:
                    self.macro.append(f"{eventName} up")
                    self.updateAction() """
        if self.macro != [""]:
            release_all_position = len(self.macro) - 1
            while release_all_position >= 0:
                if self.macro[release_all_position] == "release all":
                    release_all_position += 1
                    break
                release_all_position -= 1
            # if release_all_position < len(self.macro):
            for i in range(release_all_position,len(self.macro)):
                downPosition = self.macro[i].rfind("down")
                # This action is not a down (pressed) action,
                # so need to make sure it is eventually released
                if downPosition != -1:
                    eventName = self.macro[i][0: downPosition - 1]
                    isReleased = False
                    for j in range(i, len(self.macro)):
                        # The action has already been released
                        if eventName in self.macro[j] and self.macro[j].endswith("up"):
                            isReleased = True
                    # Action hasn't been released so need to make 
                    # 21st action "release all"
                    if not isReleased:
                        self.macro.append(f"release all")
                        self.updateAction()
                        break

    # check if the number of macro actions is out of limitation
    def macroNumLimit(self):
        """Check if the number of macro actions is out of limit.
        Can only be 20 actions entered with the 21st action being
        "release all"
        """
        if len(self.macro) >= 20:
            self.is_recording = False

    def macroPressLimit(self):
        """Check if the number of keys pressed at the same time
        is out of limit
        """
        # check if there is a repeat action
        self.repeat = False
        self.isPressed = False
        for i in range(0, len(self.macro)):
            if self.macro[i].endswith("down"):
                downPosition = self.macro[i].rfind("down")
                eventName = self.macro[i][0: downPosition - 1]
                isReleased = False
                for j in range(i, len(self.macro)):
                    # The action has already been released
                    if eventName in self.macro[j] and self.macro[j].endswith("up") or self.macro[j] == "release all":
                        isReleased = True
                    # Two up (released) actions of the same key
                    # without a down action of that key between them
                    elif f"{eventName} up" == self.act:
                        self.isPressed = True
                # Down action repeating?
                if not isReleased and self.macro[i] == self.act:
                    self.repeat = True
            if self.macro[i].endswith("up"):
                upPosition = self.macro[i].rfind("up")
                eventName = self.macro[i][0:upPosition - 1]
                isHolding = False
                for j in range(i, len(self.macro)):
                    if eventName in self.macro[j] and self.macro[j].endswith("down"):
                        isHolding = True
                if not isHolding and self.macro[i] == self.act:
                    self.repeat = True
        if self.act.endswith("down"):
            self.isPressed = True
        if self.act == "release all":
            self.isPressed = True  # This is an special condition
        # check how many keys are pressed in the same time
        numPressed = 0
        numReleased = 0
        releasePosition = 0
        releasePositionCheck = len(self.macro) - 1
        while releasePositionCheck >= 0:
            if self.macro[releasePositionCheck] == "release all":
                releasePosition = releasePositionCheck + 1
                break
            releasePositionCheck = releasePositionCheck - 1
        print(f"release: {releasePosition}")
        for i in range(releasePosition, len(self.macro)):
            if self.macro[i].endswith("down"):
                numPressed += 1
        for i in range(releasePosition, len(self.macro)):
            if self.macro[i].endswith("up"):
                numReleased += 1
        if self.act.endswith("up"):
            numReleased += 1
        if self.act.endswith("down"):
            numPressed += 1
        # Number of keys currently pressed in the macro action
        # sequence. Cannot have more than 6 keys pressed
        # according to the spec
        self.isNotReleased = numPressed - numReleased

    def updateAction(self):
        """Displays the macro action sequence entered on the GUI"""
        self.text_area.config(state="normal")
        self.text_area.delete(1.0, tk.END)
        actions = ""
        if self.macro != [""]:
            for i in range(1, len(self.macro) + 1):
                if i <= 21:
                    print(f"macro: {self.macro[i-1]}")
                    action = "\taction " + str(i) + ": " + self.macro[i - 1]
                    print(action)
                    actions += action + "\n"
                else:
                    action = "\t           " + self.macro[i - 1]
                    print(action)
                    actions += action + "\n"
        self.text_area.insert(tk.END, actions)
        self.text_area.yview_moveto(1.0)
        self.text_area.config(state="disabled")

    def macroCreate(self, num: any):
        """Create the macro by storing it in a dictionary and
        update the file chosen to save the macro (if there is
        a file chosen). Also displays these macro settings on
        the left hand side of the macro page.

        Args:
            num: The number corresponding to the macro
        """
        self.macroName = self.macroNameEntry.get()
        includeUsChar = True
        for i,char in enumerate(self.macroName):
            print(ord(char))
            if ord(char) < 32 or ord(char) > 126:
                includeUsChar = False
                break
        print(includeUsChar)
        # Warnings if user input is incorrect
        if len(self.macroName) == 0:
            self.macroNameErrorLabel.config(text="Macro name must be between 1 and 30 characters")
        elif includeUsChar == False:
            self.macroNameErrorLabel.config(text="Macro name must be characters in US keyboard")
        else:
            self.macroNameErrorLabel.config(text="")
            self.macros = self.macro
            if f"macro {num}" in self.data:
                del self.data[f"macro {num}"]
            self.data[f"macro {num}"] = {"macro name": self.macroName,
                                         "colour": list(self.colour),
                                         "macro": self.macros}
            # Though there's no file, jsonData will be saved before GUI is closed
            self.jsonData = json.dumps(self.data, indent=4)
            DataCopy = copy.deepcopy(self.data)
            print(self.data)
            self.dataInHid = MacroToHid.create_data(DataCopy)
            print(f"data: {self.data}")
            print(self.dataInHid)
            print(self.jsonData)
            self.colour = tuple(self.data[f"macro {num}"]["colour"])
            self.macroName = self.data[f"macro {num}"]["macro name"]
            self.macro = self.data[f"macro {num}"]["macro"]
            self.colourHex = f"#{self.colour[0]:02X}{self.colour[1]:02X}{self.colour[2]:02X}"
            self.RGBChooseBtn.configure(bg=self.colourHex)
            self.macroNameLabel.config(text="Macro Name: " + self.macroName)
            self.RGBColourLabel.config(text="Colour: " + f"{self.colour}")
            if self.filename != "":
                f = open(self.filename, 'w')
                f.write(f"{self.jsonData}")
                f.close()

    def stopRecording(self):
        """When finished recording the macro sequence, close
        the virtual keyboard
        """
        self.is_recording = False
        pyautogui.press('esc')
        if self.virtualKeyboard:
            self.virtualKeyboard.destroy()

    def saveBrightness(self, level):
        """Stores the brightness level set by the slider in
        the json file and displays it on the GUI.

        Args:
            level: The brightness level
        """
        protLevel = level
        value = int(level)

        if len(protLevel) < 2:
            # Calculate the number of zeros needed to make the stored value of length 2 for the protocol
            zeros_needed = 2 - len(protLevel)
            # Add the zeros in front of the number
            protLevel = "0" * zeros_needed + str(protLevel)

        # repeatData = self.protocol[2:10]
        # self.protocol = str(protLevel) + repeatData
        # self.protocol[0:1] = bytearray.fromhex(str(protLevel))
        # print(self.protocol)

        if value == 10:
            self.brightnessValueLabel.configure(text="AUTO")
        else:
            self.brightnessValueLabel.configure(text=str(value))
        try:
            f = open(self.filename, 'r')
            self.jsonData = json.load(f)
            f.close()
            self.data = self.jsonData
            if "brightness" in self.data:
                del self.data["brightness"]
            self.data["brightness"] = protLevel
            self.jsonData = json.dumps(self.data, indent=4)
            CopyD = copy.deepcopy(self.data)
            self.dataInHid = MacroToHid.create_data(CopyD)
            f = open(self.filename, 'w')
            f.write(f"{self.jsonData}")
            f.close()
        # if no file continue to store the brightness level in
        # a dictionary
        except FileNotFoundError:
            if "brightness" in self.data:
                del self.data["brightness"]
            self.data["brightness"] = protLevel
            self.jsonData = json.dumps(self.data, indent=4)
            CopyD = copy.deepcopy(self.data)
            self.dataInHid = MacroToHid.create_data(CopyD)

    def button_click(self, row, col):
        """Handle click button events

        Args:
            row: The row of the button
            col: The column of the button
        """
        print(f"Button clicked: Row {row}, Column {col}")

    def fileWrite(self):
        """Prompt user to choose a file and save data to it
        in the json format"""
        self.filename = asksaveasfilename(defaultextension=".json",
                                          filetypes=[("Text Files", "*.json"), ("All Files", "*.*")])
        f = open(self.filename, 'w')
        f.write(f"{self.jsonData}")
        print(self.filename)
        print("File written")
        f.close()

    def fileRead(self):
        """Prompt user to choose a file to read from and load
        the data into the main display of the GUI
        """
        self.filename = askopenfilename()
        self.initialDelayEntry.delete(0,"end")
        self.repeatRateEntry.delete(0,"end")
        if not self.isTextFile(self.filename):
            messagebox.showerror("Error", "Please select a text file！")
        else:
            f = open(self.filename, 'r')
            d = {}
            try:
                d = json.load(f)
                isJson = True
            except json.decoder.JSONDecodeError:
                isJson = False
            f.close()
            if isJson == False:
                messagebox.showerror("Error", "The file must contain only JSON format.")
            else:
                if self.isReadable(d):
                    self.data = d

        self.initialDelayEntry.insert(0,str(int(self.data["initial delay"])))
        self.repeatRateEntry.insert(0,str(int(self.data["repeat delay"])))
        self.slider.set(int(self.data["brightness"]))
        print(self.filename)
        print("File Read")

    def isReadable(self,d):
        """Check if the data loaded from the file and stored
        in a dictionary is in the correct format
        """
        errorMessage = ""
        if "brightness" in d:
            if not d["brightness"].isdigit() or int(d["brightness"]) > 11 or int(d["brightness"]) < 0:
                errorMessage += "The brightness in this file is illegal\n"
        if "initial delay" in d:
            if not d["initial delay"].isdigit():
                errorMessage += "The initial delay in the file include character except for number\n"
            elif int(d["initial delay"]) <= 50:
                errorMessage += "The initial delay in the file is lower than 50 ms\n"
        if "repeat delay" in d:
            if not d["repeat delay"].isdigit():
                errorMessage += "The repeat delay in the file include character except for number\n"
            elif int(d["repeat delay"]) <= 50:
                errorMessage += "The repeat delay in the file is lower than 50 ms\n"
        for num in range(10):
            if f"macro {num}" in d:
                if "macro name" in d[f"macro {num}"]:
                    includeUsChar = True
                    for i,char in enumerate(d[f"macro {num}"]["macro name"]):
                        # ASCII of the US keyboard
                        if ord(char) < 32 or ord(char) > 126:
                            includeUsChar = False
                            break
                    if len(d[f"macro {num}"]["macro name"]) == 0:
                        errorMessage += f"Macro {num} name in the file is not between 1 and 30 characters long\n"
                    elif includeUsChar == False:
                        errorMessage += f"Macro {num} name in the file includes characters out of US keyboard\n"
                if "macro" in d[f"macro {num}"]:
                    if not isinstance(d[f"macro {num}"]["macro"], list):
                        errorMessage += f"Macro {num} actions in the file is not in a list\n"
                    """
                    else:
                        for i,action in enumerate(d[f"macro {num}"]["macro"]):
                            if action not in MacroToHid.HID_dictionary:
                                errorMessage += f"Macro {num} actions includes illegal action\n"
                                break
                                """
                if "colour" in d[f"macro {num}"]:
                    if not isinstance(d[f"macro {num}"]["colour"], list):
                        errorMessage += f"Macro {num} RGB in the file are not in a list\n"
                    else:
                        if len(d[f"macro {num}"]["colour"]) != 3:
                            errorMessage += f"Macro {num} RGB are not in three numbers\n"
                        else:
                            for i, action in enumerate(d[f"macro {num}"]["colour"]):
                                if not isinstance(action, int):
                                    errorMessage += f"Macro {num} colour includes non-integer\n"
                                    break
                                elif int(action) > 255 or int(action) < 0:
                                    errorMessage += f"Macro {num} colour includes illegal number\n"
                                    break
                                
        if errorMessage != "":
            messagebox.showerror("Error",errorMessage)
            return False
        else:
            return True


    def isTextFile(self,filename):
        """Check if the file can be read
        
        Args:
            filename: The name of the file
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read() # just check if the file can be read
                return True
        except UnicodeDecodeError:
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    def ListPortsInitially(self):
        """List the serial ports detected"""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.portCombobox['values'] = ports

    def PortsRefreshing(self):
        "Refresh the list of serial ports"
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.portCombobox['values'] = ports

    def isSerialConnected(self):
        """If the serial communication has been interrupted,
        take the user back to the port selection page
        """
        while True:
            try:
                while True:
                    i = self.serialSet.in_waiting

            except serial.SerialException as e:
                if self.serialSet is None or not self.serialSet.is_open:
                    messagebox.showerror("Error", "Serial communication has been interrupted!")
                    self.clear_buttons()
                    self.PortSelectionPage()
                    break

            except KeyboardInterrupt:
                if self.serialSet is None or not self.serialSet.is_open:
                    messagebox.showerror("Error", "Serial communication has been interrupted!")
                    self.clear_buttons()
                    self.PortSelectionPage()
                    break

            finally:
                self.serialSet.close()
            """if self.serialSet is None or not self.serialSet.is_open:
                messagebox.showerror("Error", "Serial communication has been interrupted!")
                self.clear_buttons()
                self.PortSelectionPage()
                break"""


    def PortsConnecting(self):
        """Connect to the port"""

        self.selectedPort = self.portCombobox.get()
        try:
            self.serialSet = serial.Serial(self.selectedPort, 57600, timeout=1)
            self.LetsGo()
            self.monitor_thread = threading.Thread(target=self.isSerialConnected)
            self.monitor_thread.start()
        except serial.SerialException as e:
            self.serialSet = None
            print("error: ", e)

    def readBtnPress(self):
        """macroName = self.macroEntry.get() + '\n'  # Get the entered macro name
        self.serialSet.write(macroName.encode())"""
        self.brightnessLabel.config(text=f"Brightness: {self.slider.get()}")
        brightnessLevel = self.brightnessLabel.cget("text")
        print("Brightness level:", brightnessLevel)
        print(self.serialSet.in_waiting)
        
        s = chr(2) + chr(1) + chr(80) + chr(1) + chr(60) + "GG" + chr(255) * 28 + chr(255) * 3 + chr(255) * 21 +\
            "GG" + chr(255) * 28 + chr(255) * 3 + chr(255) * 21 \
            + "GG" + chr(255) * 28 + chr(255) * 3 + chr(255) * 21 \
            + "GG" + chr(255) * 28 + chr(255) * 3 + chr(255) * 21 \
            + "GG" + chr(255) * 28 + chr(255) * 3 + chr(255) * 21 \
            + "GG" + chr(255) * 28 + chr(255) * 3 + chr(255) * 21 \
            + "GG" + chr(255) * 28 + chr(255) * 3 + chr(255) * 21 \
            + "GG" + chr(255) * 28 + chr(255) * 3 + chr(255) * 21 \
            + "GG" + chr(255) * 28 + chr(255) * 3 + chr(255) * 21 \
            + "GG" + chr(255) * 28 + chr(255) * 3 + chr(255) * 21
        print(len(s))

        ProtocolRead.newData(self.data, s)
        print(self.data)
        

    def writeBtnPress(self):

        print(self.filename)

        # Using readlines()
        """ file = open(self.filename, 'r')
        data = file.read()
        data += "\r"
        print("BEFORE SENDING: " + data)"""

        #self.protocol += "\n\r"
        CopyD = copy.deepcopy(self.data)
        self.dataInHid = MacroToHid.create_data(CopyD)
        self.protocol = Protocol.createProtocol(self.protocol, self.dataInHid)
        print("SELF.DATAINHID")
        print(self.dataInHid)
        # str = "Hello"
        # self.serialSet.write(self.protocol.encode())


        # print("Read pressed for macro:", macroName, "Brightness level:", brightnessLevel)
        self.serialSet.write(self.protocol)
        # self.serialSet.write(self.protocol)

        


        print(self.serialSet.in_waiting)
        time.sleep(1)

        try:
            data_bytes = self.serialSet.read(1100)  # Read data as bytes
            print("DATA BYTES ARE:")
            print(data_bytes)
            print(len(data_bytes))
            if data_bytes:
                print()
                #new_text = data_bytes.decode('utf-8', errors='replace')  # Decode as UTF-8
                #print("DATA RECEIVED: " + new_text)
            else:
                print("No data received from the serial port.")
        except UnicodeDecodeError as e:
            print("Error decoding serial data:", e)

        """try:
            data_bytes = self.serialSet.readline().strip()  # Read data as bytes
            if data_bytes:
                new_text = data_bytes.decode('utf-8', errors='replace')  # Decode as UTF-8
                self.capMacro.config(text=new_text)  # Change the text of the label
            else:
                print("No data received from the serial port.")
        except UnicodeDecodeError as e:
            print("Error decoding serial data:", e)"""

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

        mainFrame = tk.Frame(self.parent)

        macroBtnFrame = tk.Frame(mainFrame)
        self.macroBtns = {}  # each button will be stored in here. LATER CHANGE TO DICT AND STORE INSTRUCTIONS
        for i in range(1, 11):
            macro = self.newMacroBtn(macroBtnFrame, str(i))
            self.macroBtns[i] = macro
        macroBtnFrame.pack(side=tk.LEFT, anchor=tk.CENTER)

        for i in self.macroBtns.keys():
            print(str(i) + " => " + self.macroBtns[i])

        RGBFrame = tk.Frame(mainFrame)
        self.RGBBtns = {}
        numbers = [i for i in range(1, 11)]
        for x in numbers:
            self.RGBBtns[x] = tk.Button(RGBFrame, width=self.BUTTON_WIDTH,
                                        bg="white",
                                        command=lambda y=x: self.chooseColour(y),
                                        pady=9)
            self.RGBBtns[x].pack()
        RGBFrame.pack(side=tk.LEFT, anchor=tk.CENTER)
        print("end of loop")
        for i in self.RGBBtns.keys():
            print(str(i) + " => " + str(self.RGBBtns[i]))
        mainFrame.pack()

    def ChooseColour(self, num):
        self.colorCode = colorchooser.askcolor(title="Choose color")
        print(self.colorCode[0])
        if self.colorCode[1] is not None:
            self.RGBChooseBtn.configure(bg=f"{self.colorCode[1]}")
        print(num)
        self.colour = self.colorCode[0]
        self.macroCreate(num)

    def chooseColour(self, number):
        color_code = colorchooser.askcolor(title="Choose color")
        print(color_code[0])
        self.RGBBtns[number].configure(bg=color_code[1])
        print(number)

    def newMacroBtn(self, frame, number):
        button_font = ("Berlin Sans FB Demi", 15)
        self.macroBtn = tk.Button(frame, text="Macro " + number, width=self.BUTTON_WIDTH,
                                  command=self.macroInstructions,
                                  font=button_font)
        self.macroBtn.pack()
        return self.macroBtn.config('text')[-1]

    def macroInstructions(self):
        self.clear_buttons()
        self.backBtnCreate()

        actions = ""
        macroInstructionsFrame = tk.Frame(self.parent)
        macroInstructionsFrame.pack()
        for i in range(1, 21):
            action = "action " + str(i)
            macroInstructionsLabel = tk.Label(macroInstructionsFrame, text=action)
            macroInstructionsLabel.pack()
            actions += action + " -> "
        lastAction = "action 21"
        macroInstructionsLabel = tk.Label(macroInstructionsFrame, text=lastAction)
        macroInstructionsLabel.pack()
        actions += lastAction

        macroInstructionsFrame = tk.Frame(self.parent)
        macroInstructionsFrame.pack()

    def clear_buttons(self):
        for widgets in self.parent.winfo_children():
            widgets.destroy()

    def createKeyboard(self,num):
        self.keyBtn = []  # initialize keyBtn
        self.keyState = []
        self.virtualKeyboard = tk.Toplevel(self.parent)
        self.virtualKeyboard.title("Virtual Keyboard")
        self.virtualKeyboard.geometry("1338x405")
        self.virtualKeyboard.geometry("+500+500")
        self.virtualKeyboard.resizable(False, False)  # not allow users to adjust the window size
        for row in range(len(KeyboardLayout.text)):
            self.keyBtn.append([])  # initialize keyBtn[row]
            self.keyState.append([])
            for col in range(len(KeyboardLayout.text[row])):
                self.keyState[row].append(False)
                self.keyBtn[row].append(tk.Button(self.virtualKeyboard,
                                                  width=KeyboardLayout.width[row][col],
                                                  height=KeyboardLayout.height[row][col],
                                                  text=KeyboardLayout.text[row][col],
                                                  command=lambda r=row, c=col, n=num: self.KeyboardAction(r, c, n),
                                                  bg="#FFFFFF")
                                        )
                self.keyBtn[row][col].place(x=KeyboardLayout.x[row][col], y=KeyboardLayout.y[row][col])

    def KeyboardAction(self, row, col, num):
        self.keyState[row][col] = not self.keyState[row][col]
        if row == 5 and col == 12:
            self.keyboardAct = "release all"
            for r in range(len(KeyboardLayout.text)):
                for c in range(len(KeyboardLayout.text[row])):
                    self.keyBtn[r][c].configure(bg="#FFFFFF")
                    self.keyState[r][c] = False
        elif self.keyState[row][col]:
            self.keyboardAct = f"{KeyboardLayout.event[row][col]} down"
            self.keyBtn[row][col].configure(bg="#808080")  # set to gray stands for "hold pressing"
        else :
            self.keyboardAct = f"{KeyboardLayout.event[row][col]} up"
            self.keyBtn[row][col].configure(bg="#FFFFFF")  # set to white stands for "no pressing currently"
        self.keyboardRecord(num)

    # almost same as keyRecord function.
    def keyboardRecord(self,num):
        if self.is_recording:
            self.act = self.keyboardAct
            self.macroPressLimit()
            if self.is_recording and not self.repeat and self.isNotReleased < 7 and self.isPressed:
                print(self.isNotReleased)
                if "" in self.macro:
                    self.macro.remove("")
                self.macro.append(self.act)
                self.updateAction()
            self.macroNumLimit()
        """if not self.is_recording:
            self.checkReleasing()
            self.macroCreate(num)"""
    # YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY!
    # Bugs to fix tmr: 1 sometimes the max press key number larger than 6 when using both real and virtual keyboard
    # 2 shouldn't allow to record two up action repeatedly
    # 3 try to return 0 after close during record
    # 4 scrolling the text area
    # 5 make a default data like if users haven't enter repeat delay, it should be the default value
    # 6 synchronize the label after pressing create
    # 7 make a new line when the macro name is too long
    # 8 after stopping record, just close keyboard
    # 9 set the maximum number of repeat delay and initial delay
    # 10 avoid record button for twice without stop button 防止重复按记录按钮
    # 11 the last action cannot come out until I press the stop button
    # 12 if users change the file content to illegal one, the file should not be read
    # 13 if there is a serial disconnection, there shouldn't be a collision
    # 14 there is no macro validation check in file error check

class GameApp(object):

    def __init__(self, master):
        BUTTON_WIDTH = 15
        button_font = ("Berlin Sans FB Demi", 15)
        button_fg_color = "white"
        bg_colour = "light blue"

        master.title("2800 Team Project")

        gui = GUI(master)
        gui.pack(side=tk.LEFT, fill=tk.Y)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1350x700")
    # root.configure(bg="white")
    app = GameApp(root)
    root.mainloop()