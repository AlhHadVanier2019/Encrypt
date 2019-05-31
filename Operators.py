import os
import struct

def stringtobin(message):
    """
    :param message: The string message to be turned into binary
    :return: returns the message converted to a string of bits
    """
    # creates a variable called bits total where the bits will be stored
    bitstotal = ""
    # this loop runs the for the length of the message that needs to be converted
    for i in range(len(message)):
        # when using the bin function, a '0b' is added to the start of it,the [2:0] removes it
        char = bin(ord(message[i]))[2:]
        # adds enough leading zeros to create a byte
        while len(char) < 8:
            char = "0" + char
        # adds the byte value of the character to the variable bitstotal
        bitstotal += char
    return (bitstotal)


def bintostring(binarymessage):
    """
    :param binarymessage: Converts a sequence of bits into a string. Binarymessage
    must be a string of multiple 8
    :return: returns a string.
    """
    # total is where the string will be stored
    total = ""
    # for each byte, it is converted to base 10 and then converted to an ascii value
    for i in range(len(binarymessage) // 8):
        byte = binarymessage[8 * i: 8 * (i + 1)]
        byte = int(byte, 2)
        char = chr(byte)
        # after its converted into the character, it is stored in total
        total += char
    return total


def inttobin(integertoconvert):
    """
    :param integertoconvert: the base-10 integer to convert to binary
    :return: returns the binary equivalent of the integer
    """
    # converts the number into binary and removes the '0b'
    binarynumber = bin(integertoconvert)[2:]
    # if the length of the integer is not a multiple of 8 (a byte), it adds leading 0's
    while len(binarynumber) % 8 != 0:
        binarynumber = "0" + binarynumber

    return binarynumber


def bintoint(string):
    """
    :param string: string is a string of bits that needs to be converted to an integer
    :return: returns a base 10 integer
    """
    # takes the input in bits, and converts it to base 2
    decimal = int(string, 2)
    return decimal


def hextobin(hexval):
    """
    :param hexval: The hex value to be converted to an integer
    :return: returns a base 10 integer
    """
    # takes the hexvalue converts it into base 10
    decimal = int(hexval, 16)
    # ueses intobin function to convert to binary
    result = inttobin(decimal)
    return result


def bintohex(binval):
    """
    :param binval: The string of bits to be converted
    :return: returns the hex value
    """
    # takes the binary number and converts it into base 10
    decimal = int(binval, 2)
    # takes converts the base 10 number to a hex
    result = hex(decimal)[2:]  # The 2: is because all hex numbers in python start with 0x which we don't want
    # if the hex value is less than 8, it adds leading zeros
    while len(result) < 8:
        result = "0" + result
    return result


# ---------Bitwise Operators---------
def bitxor(*bits):
    """

    :param bits: All the bytes to be XOR'd
    :return: The XOR'd value
    """
    # Convert to base 10
    allnums = []
    for icounter in range(len(bits)):
        allnums.append(bintoint(bits[icounter]))

    # XOR The numbers
    result = allnums[0]
    for icounter in range(1, len(allnums)):
        result = result ^ allnums[icounter]

    # Convert back to binary
    result = inttobin(result)

    return result

def bitadd(*bits):
    """
    :param bits: All the bytes to be added
    :return: The total value
    """
    # Convert to base 10
    allnums = []
    for icounter in range(len(bits)):
        allnums.append(bintoint(bits[icounter]))

    # Add The numbers
    result = allnums[0]
    for icounter in range(1, len(allnums)):
        result = result + allnums[icounter]

    #Convert to base 2
    result = inttobin(result)

    return result


def bitnot(bitinput):
    """
    :param bitinput: the string of bits to be "notted".
    :return: Returns a sequence of bits, the complement of bitinput
    """
    result = ""
    # checks each bit and gets the compliment of it
    for i in range(len(bitinput)):
        # if the bitinput is a 0, the result will be a 1
        if bitinput[i] == "1":
            result += "0"
        else:
            # if the bitinput is a 1, the result will be 0
            result += "1"

    return result


def bitand(*bits):
    """
    :param bits: All the bytes to be "anded"
    :return: The resulting value
    """
    # Convert to base 10
    allnums = []
    for icounter in range(len(bits)):
        allnums.append(bintoint(bits[icounter]))

    # And The numbers using the built in function
    result = allnums[0]
    for icounter in range(1, len(allnums)):
        result = result & allnums[icounter]

    # Convert to base 2
    result = inttobin(result)

    return result


# -----Bit Manipulation Functions---------
def rightrotate(strinput, amount):
    """
    :param strinput: The string of bits to be right rotated
    :param amount: The amount of times to right rotate strinput.
    :return: returns strinput rotated right 'amount' number of  times
    """
    # Get the full string
    stringfull = strinput
    string = strinput
    for i in range(amount):
        # Set the first value to the last character
        string = stringfull[len(stringfull) - 1]
        # The for loop adds in the other characters to the right
        for g in range(0, len(strinput) - 1):
            string += stringfull[g]

        stringfull = string

    return string

def leftrotate(strinput, amount):
    """
    :param strinput: is the string input of bits
    :param amount: the amount of times to rotate by
    :return: returns strinput shifted left 'amount' number of  times
    """
    stringfull = strinput
    string = strinput
    for i in range(amount):
        # Set the last character of string to the first value of stringfull
        string = stringfull[0]
        for g in range(1, len(strinput)):
            # Add in the other characters to the left
            string = stringfull[len(strinput) - g] + string

        stringfull = string

    return string


def rightshift(strinput, amount):
    """
    :param strinput: This is the string input in bits
    :param amount: Amount to shift by
    :return: Returns strinput shifted right 'amount' number of  times
    """
    # Convert to base 10
    bit = bintoint(strinput)

    # Perform the Operation using the built in function

    result = bit >> amount

    # Convert to base 2
    result = inttobin(result)

    return result

#========Miscallenous Functions dealing with bytes=========
def getbytearray(file):
    """
    This method takes a file and converts it to an array of bytes
    :param file: The file to be converted
    :return: An array of bytes
    """

    # Open the fila as binary
    with open(file, "rb") as image:
        # Read the file and use the built-in bytearray function
        contents = image.read()
        raw_byte_array = bytearray(contents)

    # Convert the integers into bytes and return the new byte array
    byte_array = []
    for i in range(len(raw_byte_array)):
        byte_array.append(inttobin(raw_byte_array[i]))

    return byte_array


def write_to_desktop(byte_array, name):
    """
    This function writes a byte array to a file on the desktop.
    :param byte_array: The byte array input to be written to a file on the desktop
    :param name: The name of the new file. Must include file extension
    :return: Nothing is returned, but a file is written to the dektop
    """

    with open(os.path.join(os.path.expanduser('~'), "Desktop", name), "wb") as hack:
        for byte in byte_array:
            newbyte = int(byte, 2)
            newbyte = struct.pack("B", newbyte)
            hack.write(newbyte)
