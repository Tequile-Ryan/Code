MACRO_NAME_LENGTH = 30
RGB_VALUES_LENGTH = 3
HIDS_LENGTH = 21

BYTES_PER_KEY = 54      # 30+3+21 (Macro name, RGB values, HIDs)


def createProtocol(protocol, data):
    # Macro 1 Start Index: 5
    # Macro 2 Start Index: 62 (1*57+5)
    # Macro 3 Start Index: 119 (2*57+5)
    # Macro 4 Start Index: 176 (3*57+5)

    # CAREFUL RGB VALUES CAN BE SET ANYWHERE FROM 0 TO 255!!!

    # Iterate through up to 10 macros present

    ###############################################################################
    # SET BRIGHTNESS TO ZERO
    ###############################################################################
    protocol[5:] = bytearray(b'\xff') * 540

    for num in range(1, 11):
        if f"macro {num}" in data:
            colour = data[f"macro {num}"]["colour"]
            macroName = data[f"macro {num}"]["macro name"]
            macro = data[f"macro {num}"]["macro"]

            print("\n\nWE ARE TALKING ABOUT MACRO NUMBER: " + str(num) + "\n\n")

            # populate the protocol with the macro name
            macroNameBeginIndex = (num-1)*BYTES_PER_KEY + 5
            macroNameEndIndex = macroNameBeginIndex + len(macroName)
            protocol[macroNameBeginIndex:macroNameEndIndex] = macroName.encode()

            # populate the protocol with the RGB values
            RGBValuesBeginIndex = macroNameBeginIndex + MACRO_NAME_LENGTH
            RGBValuesEndIndex = RGBValuesBeginIndex + RGB_VALUES_LENGTH
            col1, col2, col3 = colour
            # fromhex can only take the hex number without the "0x" in font of it, so that is why we do [2:]
            protocol[RGBValuesBeginIndex:RGBValuesEndIndex] = bytearray.fromhex((hex(col1))[2:]) \
                + bytearray.fromhex((hex(col2))[2:]) \
                + bytearray.fromhex((hex(col3))[2:])
            
            # populate the protocol with key press HID data
            HIDStartIndex = RGBValuesEndIndex
            for hid in macro:
                HIDEndIndex = HIDStartIndex + 1
                protocol[HIDStartIndex:HIDEndIndex] = bytearray.fromhex(hid)
                HIDStartIndex += 1


    print(protocol)
    return protocol

            