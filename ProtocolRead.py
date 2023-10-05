# import MacroToHid
# import json


swappedData = {
    "00": "release all",
    "ff": "",
    "04": "A down",
    "05": "B down",
    "06": "C down",
    "07": "D down",
    "08": "E down",
    "09": "F down",
    "0a": "G down",
    "0b": "H down",
    "0c": "I down",
    "0d": "J down",
    "0e": "K down",
    "0f": "L down",
    "10": "M down",
    "11": "N down",
    "12": "O down",
    "13": "P down",
    "14": "Q down",
    "15": "R down",
    "16": "S down",
    "17": "T down",
    "18": "U down",
    "19": "V down",
    "1a": "W down",
    "1b": "X down",
    "1c": "Y down",
    "1d": "Z down",
    "1e": "1 down",
    "1f": "2 down",
    "20": "3 down",
    "21": "4 down",
    "22": "5 down",
    "23": "6 down",
    "24": "7 down",
    "25": "8 down",
    "26": "9 down",
    "27": "0 down",
    "28": "enter down",
    "29": "esc down",
    "2a": "backspace down",
    "2b": "tab down",
    "2c": "space down",
    "2d": "_ down",
    "2e": "+ down",
    "2f": "{ down",
    "30": "} down",
    "31": "| down",
    "33": ": down",
    "34": "\" down",
    "35": "~ down",
    "36": "< down",
    "37": "> down",
    "38": "? down",
    "39": "caps lock down",
    "3a": "f1 down",
    "3b": "f2 down",
    "3c": "f3 down",
    "3d": "f4 down",
    "3e": "f5 down",
    "3f": "f6 down",
    "40": "f7 down",
    "41": "f8 down",
    "42": "f9 down",
    "43": "f10 down",
    "44": "f11 down",
    "45": "f12 down",
    "46": "print screen down",
    "47": "scroll lock down",
    "48": "pause down",
    "49": "insert down",
    "4a": "home down",
    "4b": "page up down",
    "4c": "delete down",
    "4d": "end down",
    "4e": "page down down",
    "4f": "right down",
    "50": "left down",
    "51": "down down",
    "52": "up down",
    "53": "num lock down",
    "54": "P / down",
    "55": "P * down",
    "56": "P - down",
    "57": "P + down",
    "58": "P enter down",
    "59": "P 1 down",
    "5a": "P 2 down",
    "5b": "P 3 down",
    "5c": "P 4 down",
    "5d": "P 5 down",
    "5e": "P 6 down",
    "5f": "P 7 down",
    "60": "P 8 down",
    "61": "P 9 down",
    "62": "P 0 down",
    "63": "P . down",
    "e0": "ctrl down",
    "e1": "shift down",
    "e2": "alt down",
    "e3": "left windows down",
    "e4": "right ctrl down",
    "e5": "right shift down",
    "e6": "right alt down",
    "e7": "right windows down"
}

def newData(d,s):
    d["brightness"] = str(ord(s[0]))
    d["initial delay"] = str(256 * ord(s[1]) + ord(s[2]))
    d["repeat delay"] = str(256 * ord(s[3]) + ord(s[4]))
    for num in range(10):
        d[f"macro {num + 1}"]["macro name"] = s[5 + num * 54: 35 + num * 54].replace(chr(255), "")
        RGB = []
        RGB.append(ord(s[35 + num * 54]))
        RGB.append(ord(s[36 + num * 54]))
        RGB.append(ord(s[37 + num * 54]))
        d[f"macro {num + 1}"]["colour"] = RGB
        macro = []
        for i in range(21):
            if s[i + 38 + num * 54] != chr(255):
                decHID = ord(s[i + 35 + num * 54])
                hexHID = hex(decHID)
                strHID = hexHID.replace("0x", "")
                macro.append(swappedData[strHID])
        d[f"macro {num + 1}"]["macro"] = macro


"""f = open("reversedHID.txt", "w")
jsonData = json.dumps(swappedData, indent=4)
f.write(jsonData)
f.close()"""

print(swappedData)
