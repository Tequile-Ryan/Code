MACRO_NAME_LENGTH = 30
RGB_VALUES_LENGTH = 3
HIDS_LENGTH = 21

BYTES_PER_KEY = 54      # 30+3+21 (Macro name, RGB values, HIDs)


def createProtocol(protocol, data):
    # Macro 1 Start Index: 5
    # Macro 2 Start Index: 62 (1*57+5)
    # Macro 3 Start Index: 119 (2*57+5)
    # Macro 4 Start Index: 176 (3*57+5)

    # Iterate through up to 10 macros present

    protocol[5:] = bytearray(b'\xff') * 540

    if "brightness" in data:
        protocol[0:1] = bytearray([int(data["brightness"])])
        print("BRIGHTNESS IS")
        print(bytearray([int(data["brightness"])]))

    if "initial delay" in data:
        byteArray1, byteArray2 = sixteenBitToBytes(data["initial delay"])
        protocol[1:3] = byteArray1 + byteArray2

    if "repeat delay" in data:
        byteArray1, byteArray2 = sixteenBitToBytes(data["repeat delay"])
        protocol[3:5] = byteArray1 + byteArray2

    for num in range(1, 11):
        if f"macro {num}" in data:
            colour = data[f"macro {num}"]["colour"]
            macroName = data[f"macro {num}"]["macro name"]
            macro = data[f"macro {num}"]["macro"]

            # populate the protocol with the macro name
            macroNameBeginIndex = (num-1)*BYTES_PER_KEY + 5
            macroNameEndIndex = macroNameBeginIndex + len(macroName)
            protocol[macroNameBeginIndex:macroNameEndIndex] = macroName.encode()

            # populate the protocol with the RGB values
            RGBValuesBeginIndex = macroNameBeginIndex + MACRO_NAME_LENGTH
            RGBValuesEndIndex = RGBValuesBeginIndex + RGB_VALUES_LENGTH
            # col1, col2, col3 = colour
            # fromhex can only take the hex number without the "0x" in font of it, so that is why we do [2:]
            # fromhex converts the hex number into a decimal number (ASCII)
            print(colour)
            for col in colour:
                print(type(col))
            protocol[RGBValuesBeginIndex:RGBValuesEndIndex] = bytearray([colour[0]]) \
                + bytearray([int(colour[1])]) \
                + bytearray([int(colour[2])])
                        
            # populate the protocol with key press HID data
            HIDStartIndex = RGBValuesEndIndex
            for hid in macro:

                HIDEndIndex = HIDStartIndex + 1
                protocol[HIDStartIndex:HIDEndIndex] = bytearray.fromhex(hid)
                HIDStartIndex += 1

    print(protocol)
    return protocol


def sixteenBitToBytes(number):
    """Converts 16 bit integer into corresponding tuple of two
    single byte bytearrays where the bytes read together as 16
    bits correspond to the original 16 bit integer
    """

    byte1 = (int(number) >> 8) & 0xff
    byte2 = int(number) & 0xff

    return (bytearray([byte1]), bytearray([byte2]))





            