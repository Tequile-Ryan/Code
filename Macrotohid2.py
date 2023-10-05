import copy


HID_dictionary = {"release all": "00",
                  "": "ff",
                  "a down": "04",
                  "A down": "04",
                  "b down": "05",
                  "B down": "05",
                  "c down": "06",
                  "C down": "06",
                  "d down": "07",
                  "D down": "07",
                  "e down": "08",
                  "E down": "08",
                  "f down": "09",
                  "F down": "09",
                  "g down": "0a",
                  "G down": "0a",
                  "h down": "0b",
                  "H down": "0b",
                  "i down": "0c",
                  "I down": "0c",
                  "j down": "0d",
                  "J down": "0d",
                  "k down": "0e",
                  "K down": "0e",
                  "l down": "0f",
                  "L down": "0f",
                  "m down": "10",
                  "M down": "10",
                  "n down": "11",
                  "N down": "11",
                  "o down": "12",
                  "O down": "12",
                  "p down": "13",
                  "P down": "13",
                  "q down": "14",
                  "Q down": "14",
                  "r down": "15",
                  "R down": "15",
                  "s down": "16",
                  "S down": "16",
                  "t down": "17",
                  "T down": "17",
                  "u down": "18",
                  "U down": "18",
                  "v down": "19",
                  "V down": "19",
                  "w down": "1a",
                  "W down": "1a",
                  "x down": "1b",
                  "X down": "1b",
                  "y down": "1c",
                  "Y down": "1c",
                  "z down": "1d",
                  "Z down": "1d",
                  "1 down": "1e",
                  "! down": "1e",
                  "2 down": "1f",
                  "@ down": "1f",
                  "3 down": "20",
                  "# down": "20",
                  "4 down": "21",
                  "$ down": "21",
                  "5 down": "22",
                  "% down": "22",
                  "6 down": "23",
                  "^ down": "23",
                  "7 down": "24",
                  "& down": "24",
                  "8 down": "25",
                  "* down": "25",
                  "9 down": "26",
                  "( down": "26",
                  "0 down": "27",
                  ") down": "27",
                  "enter down": "28",
                  "esc down": "29",
                  "backspace down": "2a",
                  "tab down": "2b",
                  "space down": "2c",
                  "- down": "2d",
                  "_ down": "2d",
                  "= down": "2e",
                  "+ down": "2e",
                  "[ down": "2f",
                  "{ down": "2f",
                  "] down": "30",
                  "} down": "30",
                  "\\ down": "31",
                  "| down": "31",
                  "; down": "33",
                  ": down": "33",
                  "' down": "34",
                  "\" down": "34",
                  "` down": "35",
                  "~ down": "35",
                  ", down": "36",
                  "< down": "36",
                  ". down": "37",
                  "> down": "37",
                  "/ down": "38",
                  "? down": "38",
                  "caps lock down": "39",
                  "f1 down": "3a",
                  "f2 down": "3b",
                  "f3 down": "3c",
                  "f4 down": "3d",
                  "f5 down": "3e",
                  "f6 down": "3f",
                  "f7 down": "40",
                  "f8 down": "41",
                  "f9 down": "42",
                  "f10 down": "43",
                  "f11 down": "44",
                  "f12 down": "45",
                  "print screen down": "46",
                  "scroll lock down": "47",
                  "pause down": "48",
                  "insert down": "49",
                  "home down": "4a",
                  "page up down": "4b",
                  "delete down": "4c",
                  "end down": "4d",
                  "page down down": "4e",
                  "right down": "4f",
                  "left down": "50",
                  "down down": "51",
                  "up down": "52",
                  "num lock down": "53",
                  "P / down": "54",
                  "P * down": "55",
                  "P - down": "56",
                  "P + down": "57",
                  "P enter down": "58",
                  "P 1 down": "59",
                  "P 2 down": "5a",
                  "P 3 down": "5b",
                  "P 4 down": "5c",
                  "P 5 down": "5d",
                  "P 6 down": "5e",
                  "P 7 down": "5f",
                  "P 8 down": "60",
                  "P 9 down": "61",
                  "P 0 down": "62",
                  "P . down": "63",
                  "ctrl down": "e0",
                  "shift down": "e1",
                  "alt down": "e2",
                  "left windows down": "e3",
                  "right ctrl down": "e4",
                  "right shift down": "e5",
                  "right alt down": "e6",
                  "right windows down": "e7",
                  }


# convert function allow to make the macro list into a Hid list
def convert(ls):
    hid_ls = []
    """for index, action in enumerate(ls):
        if action in HID_dictionary.keys():  # if there is a down action
            hid_ls.append(HID_dictionary.get(action))  # add the corresponding HID code to the list
            ascii_index = chr(index + 32)  # use the corresponding ascii char to decrease the bytes
            hid_ls.append(ascii_index)
            if "down" in action:  # just exclude release all action
                event_index = action.rfind("down") - 1  # find the range of event name in the string
                event = action[0:event_index]
                for up_index, up_action in enumerate(ls, start=index + 1):
                    if event in up_action:  # find the up action position in the list
                        ascii_up_index = chr(up_index + 32)
                        hid_ls.append(ascii_up_index)
                        break
            else:
                hid_ls.append(" ")"""

    for action in ls:
        if action in HID_dictionary.keys():
            # decHID = int(HID_dictionary.get(action), 16)
            # decHID = f"{decHID:03}"
            hid = HID_dictionary.get(action)
            hid_ls.append(hid)
        else:
            up_convert_into_down_action = action[:action.rfind("up")] + "down"
            # decHID = int(HID_dictionary.get(up_convert_into_down_action), 16)
            # decHID = f"{decHID:03}"
            hid = HID_dictionary.get(up_convert_into_down_action)
            hid_ls.append(hid)
    return hid_ls


# create_data funtion allow to apply convert function to every macro in the dictionary
def create_data(d):
    d_new = copy.deepcopy(d)
    for num in range(1, 11):
        if f"macro {num}" in d_new:
            hid_macro = convert(d[f"macro {num}"]["macro"])
            d_new[f"macro {num}"]["macro"] = hid_macro
    return d_new
