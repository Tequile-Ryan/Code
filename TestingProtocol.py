hidData = {'macro 3': {'macro name': 'sdfsdf', 'colour': (81, 92, 240),
                       'macro': ['07', '09', '07', '16', '07', '07', '16', '16', '09', '16']},
                       'macro 1': {'macro name': 'fsdfsd', 'colour': (138, 209, 112),
                                   'macro': ['0a', '09', '0b', '0a', '09', '09', '0b', '0a', '09', '0a']},
                                   'macro 7': {'macro name': 'fsdfs', 'colour': (238, 83, 83),
                                               'macro': ['09', '07', '16', '04', '0a', '0a', '0b', '0b', '0c', '0c', '17', '15', '16', '04', '1a', '08', '09', '07', '09', '07', '00']}}



string = "He"
protocol = bytearray(string.encode('ASCII'))
print(protocol)
protocol += b'\x65'
protocol += b'\xFF'
print(protocol)
protocol += bytearray.fromhex('65')
protocol += bytearray.fromhex('ff')
print(protocol)
print(len(protocol))
print(hex(65))
print(type(protocol))
protocol[5:6] = bytearray(b'\x65')
print(protocol)
print(len(protocol))
protocol += str(3).encode()
print("ENCODED STRING IS: ")
print(str(33).encode())
protocol += str(33).encode()
print(protocol)
print("chr is: " + str(chr(3)))
print(ord('3'))
print(hex(51))
print(protocol)
protocol += bytearray.fromhex('33')
print("PROTOCOL IS: ")
print(protocol)
print(len(protocol))

delay = "7089"
print(delay)
print(delay[0:2])
print(delay[2:4])

protocol[3:4] = bytearray(b'\x65')
print(protocol)
print(protocol[2])
print(protocol[2:3])

print("PROTOCOL WAS: ")
print(protocol)
protocol1 = protocol
protocol1 += bytearray(b'\x65')
print(protocol1)
print(protocol)

"""
print()
print()
print()


example = bytearray(b'\x65')
print(example[0])
print(example[0:1])
example[0:1] = bytearray(b'\x64')
print(example)
"""

index=(2-1)*57+5
print(index)


int1 = 67
int2 = 89

totalInt = str(int1)+str(int2)
totalInt = int(totalInt)
print(totalInt)
print(type(totalInt))


# Use bytearray() method to convert list to byte_arry

# print(hidData)
# print(type(hidData))

print(bytearray.fromhex("33"))
print(hex(255))
num = (hex(255))[2:]
#print(num)
print(bytearray.fromhex((hex(255))[2:]))

output = bytearray(b'\x02UUXV\xff\xffTeq\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xd9h\xc8\t\t\x07\x07\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffTequile\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc4}}\x04\x04\x16\x16\x07\x07\t\t\n\n\x0b\x0b\xff\xff\xff\xff\xff\xff\xff\xff\xffpracspracspracspracspracs\xff\xff\xff\xff\xff\xf9HM\xe0\x06\xe0\x06\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffKEY 7\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf1PP99\x07\x07\x0e\x0e\x07\x07\r\r\x16\x16\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffWhat is this\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffj\xd7\xbe\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\xff\xff\xfffloccinaucinihilipilification!\xdeX\xe9\x07\x07\x0b\x0b\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
dictionary = {'macro 10': {'macro name': 'floccinaucinihilipilification!', 'colour': [222, 88, 233], 'macro': ['07', '07', '0b', '0b']}, 'macro 3': {'macro name': 'pracspracspracspracspracs', 'colour': [249, 72, 77], 'macro': ['e0', '06', 'e0', '06']}, 'macro 9': {'macro name': 'What is this', 'colour': [106, 215, 190], 'macro': ['14', '14', '14', '14', '14', '14', '14', '14', '14', '14', '14', '14', '14', '14', '14', '14', '14', '14']}, 'macro 2': {'macro name': 'Tequile', 'colour': [196, 125, 125], 'macro': ['04', '04', '16', '16', '07', '07', '09', '09', '0a', '0a', '0b', '0b']}, 'macro 7': {'macro name': 'KEY 7', 'colour': [241, 80, 80], 'macro': ['39', '39', '07', '07', '0e', '0e', '07', '07', '0d', '0d', '16', '16']}, 'brightness: ': '05', 'macro 1': {'macro name': 'Teq', 'colour': [217, 104, 200], 'macro': ['09', '09', '07', '07']}, 'initial delay: ': '5857', 'repeat delay: ': '5655'}
print(len(output))
print(output[0:7])
print(output[7:61])
print(len(output[7:61]))
macro1 = dictionary[f"macro 1"]["macro"]
print(macro1)
print(type(macro1))

print(output[61:115])
print(len(output[7:61]))
macro2 = dictionary[f"macro 2"]["macro"]
print(macro2)

print(output[439:493])
print(len(output[439:493]))
macro2 = dictionary[f"macro 9"]["macro"]
print(macro2)


#b'\xffXXUU\xff\xffTeq\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xd9h\xc8\t\t\x07\x07\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffTeuile\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc4}\x04\x04\x16\x16\x07\x07\t\t\n'


"""
for hid in macro:
                # HIDEndIndex = HIDStartIndex + j
                # protocol[HIDStartIndex:HIDEndIndex] = bytearray.fromhex(hid)
                print(hid)
                print(type(hid))

                j += 1
                """

print("test")
code = bytearray(b'\xff\x00\x04\x00\x00\xff\xffTeq\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xd9h\xc8\t\t\x07\x07\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffTequile\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc4}}\x04\x04\x16\x16\x07\x07\t\t\n\n\x0b\x0b\xff\xff\xff\xff\xff\xff\xff\xff\xffpracspracspracspracspracs\xff\xff\xff\xff\xff\xf9HM\xe0\x06\xe0\x06\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
print(len(code))

thing1 = bytearray(b'\xff\x00U\x00\x00key1\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xd9h\xc8\t\t\x07\x07\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffkey2\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc4}}\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffkey3\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf9HM\xe0\x06\xe0\x06\xe0\x04\x04\xe0\x04\x04\x04\x04\x04\x04\x04\x04\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffKEY 7\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf1PP99\x07\x07\x0e\x0e\x07\x07\r\r\x16\x16\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffWhat is this\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffj\xd7\xbe\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\xff\xff\xfffloccinaucinihilipilification!\xdeX\xe9\x07\x07\x0b\x0b\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
thing2 = bytearray(b'\xff\x00U\x00\x00key1\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xd9h\xc8\t\t\x07\x07\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffkey2\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc4}}\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffkey3\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf9HM\xe0\x06\xe0\x06\xe0\x04\x04\xe0\x04\x04\x04\x04\x04\x04\x04\x04\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffKEY 7\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf1PP99\x07\x07\x0e\x0e\x07\x07\r\r\x16\x16\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffWhat is this\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffj\xd7\xbe\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\xff\xff\xfffloccinaucinihilipilification!\xdeX\xe9\x07\x07\x0b\x0b\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')

x  = thing1 == thing2

print(f"The msg nmatches {x}\n")