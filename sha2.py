##------------------------------Type Conversion-------------------------
def stringtobin(message):
    bitstotal = "" # creates a variable called bits total where the bits will be stored
    for i in range(len(message)):
        char = bin(ord(message[i]))[2:]
        while len(char) < 8:
            char = "0" + char
        bitstotal += char
    return (bitstotal)

def bintostring(binarymessage):
    total = ""
    for i in range(len(binarymessage)// 8):
        byte = binarymessage[8 * i : 8 * (i + 1) ]
        byte = int(byte,2)
        char = chr(byte)
        total += char
    return total

def inttobin(integertoconvert):
    binarynumber = bin(integertoconvert)[2:]
    while len(binarynumber) %8 != 0:
        binarynumber = "0" + binarynumber
        
    return binarynumber

def bintoint(string):
    decimal = int(string, 2)
    return decimal

def hextobin (hexval):
    decimal = int(hexval, 16)
    result = inttobin(decimal)
    return result

def bintohex (binval):
    decimal = int(binval, 2)
    result = hex(decimal)[2:]
    while len(result) < 8:
        result = "0" + result
    return result
    
#---------Bitwise Operators---------
def bitxor (input1, input2):
    #Convert to base 10
    bit1 = bintoint (input1)
    bit2 = bintoint (input2)

    #XOR the numbers
    result = bit1 ^ bit2 

    #Convert to base 2
    result = inttobin(result)
    return result

def bitadd (input1, input2):
    #Convert to base 10
    bit1 = bintoint (input1)
    bit2 = bintoint (input2)

    #Add the numbers
    result = bit1 + bit2
    #Convert to base 2
    result = inttobin(result)
    return result

def bitnot (bitinput):
    result = ""
    for i in range (len(bitinput)):
        if bitinput[i] == "1":
            result += "0"
        else:
            result += "1"

    return result

def bitand (input1, input2):
    #Convert to base 10
    bit1 = bintoint (input1)
    bit2 = bintoint (input2)

    #"AND" the numbers
    result = bit1 & bit2
    #Convert to base 2
    result = inttobin(result)
    return result

#-----Bit Manipulation Functions---------
def rightrotate (strinput, amount):
    #Get the full string
    stringfull = strinput
    string = strinput
    for i in range(amount):
        #Set the first value to the last character
        string = stringfull[len(stringfull) - 1]
        #The for loop adds in the other characters to the right
        for g in range (0, len(strinput) - 1):
            string += stringfull[g]

        stringfull = string

    return string

#Leftrotate is not used in the hash function. I realized this after I made it
def leftrotate (strinput, amount):
    stringfull = strinput
    string = strinput
    for i in range(amount):
        #Set the last character of string to the first value of stringfull
        string = stringfull[0]
        for g in range (1, len(strinput)):
            #Add in the other characters to the left
            string = stringfull[len(strinput) - g] + string

        stringfull = string

    return string

def rightshift (strinput, amount):
    #Convert to base 10
    bit = bintoint (strinput)

    #Perform the Operation
    result = bit >> amount

    #Convert to base 2 
    result = inttobin(result)

    return result
    
#----------------------The Function------------------------
def shahash(message,fbits_per_word):
    #---------Initial Hash Values-------
    h0 = hextobin("0x6a09e667")
    h1 = hextobin("0xbb67ae85")
    h2 = hextobin("0x3c6ef372")
    h3 = hextobin("0xa54ff53a")
    h4 = hextobin("0x510e527f")
    h5 = hextobin("0x9b05688c")
    h6 = hextobin("0x1f83d9ab")
    h7 = hextobin("0x5be0cd19")

    #--------Initial Constants-------
    constants = [hextobin("0x428a2f98"), hextobin("0x71374491"), hextobin("0xb5c0fbcf"), hextobin("0xe9b5dba5"),
                 hextobin("0x3956c25b"), hextobin("0x59f111f1"), hextobin("0x923f82a4"), hextobin("0xab1c5ed5"),
                 hextobin("0xd807aa98"), hextobin("0x12835b01"), hextobin("0x243185be"), hextobin("0x550c7dc3"),
                 hextobin("0x72be5d74"), hextobin("0x80deb1fe"), hextobin("0x9bdc06a7"), hextobin("0xc19bf174"),
                 hextobin("0xe49b69c1"), hextobin("0xefbe4786"), hextobin("0x0fc19dc6"), hextobin("0x240ca1cc"),
                 hextobin("0x2de92c6f"), hextobin("0x4a7484aa"), hextobin("0x5cb0a9dc"), hextobin("0x76f988da"),
                 hextobin("0x983e5152"), hextobin("0xa831c66d"), hextobin("0xb00327c8"), hextobin("0xbf597fc7"),
                 hextobin("0xc6e00bf3"), hextobin("0xd5a79147"), hextobin("0x06ca6351"), hextobin("0x14292967"),
                 hextobin("0x27b70a85"), hextobin("0x2e1b2138"), hextobin("0x4d2c6dfc"), hextobin("0x53380d13"),
                 hextobin("0x650a7354"), hextobin("0x766a0abb"), hextobin("0x81c2c92e"), hextobin("0x92722c85"),
                 hextobin("0xa2bfe8a1"), hextobin("0xa81a664b"), hextobin("0xc24b8b70"), hextobin("0xc76c51a3"),
                 hextobin("0xd192e819"), hextobin("0xd6990624"), hextobin("0xf40e3585"), hextobin("0x106aa070"),
                 hextobin("0x19a4c116"), hextobin("0x1e376c08"), hextobin("0x2748774c"), hextobin("0x34b0bcb5"),
                 hextobin("0x391c0cb3"), hextobin("0x4ed8aa4a"), hextobin("0x5b9cca4f"), hextobin("0x682e6ff3"),
                 hextobin("0x748f82ee"), hextobin("0x78a5636f"), hextobin("0x84c87814"), hextobin("0x8cc70208"),
                 hextobin("0x90befffa"), hextobin("0xa4506ceb"), hextobin("0xbef9a3f7"), hextobin("0xc67178f2")]

    #-----------------Padding-----------------
    #This sections initializes the first 16 "words". Each "word" is 32 bits.
    #The words array o
    words = []

    paddedmessage = stringtobin(message)
    bitsinmessage = inttobin(len(paddedmessage))
    paddedmessage += "1"


    while (len(paddedmessage) + len(bitsinmessage)) % 512 != 0:
        paddedmessage += "0"

    paddedmessage += bitsinmessage
    fullmessage = paddedmessage
    
    for z in range (len(paddedmessage) // 512):
        words = []
        paddedmessage = fullmessage[512 * z: 512 * (z+1)]
        for i in range (int(fbits_per_word/2)):
            words.append(paddedmessage [fbits_per_word * i : fbits_per_word * (i + 1) ])

        #----------Creating the 64 words from the first 16-------
        for i in range(16, 64):
            s0 = bitxor(bitxor(rightrotate (words[i-15], 7), rightrotate (words[i-15], 18)), rightshift(words[i-15], 3))
            s1 = bitxor(bitxor(rightrotate (words[i-2], 17), rightrotate (words[i-2], 19)), rightshift(words[i-2], 10))

            sum1 = bitadd (words[i-16], s0)
            sum2 = bitadd (words[i-7], s1)
            total = bitadd (sum1,sum2)
            while len(total) < 32:
                total = "0" + total

        #Only take the first 32 bits, starting from the right
            if len(total) > 32:
                total = total[8:]
            
            words.append (total)

        for i in range(len(words)):
            print(str((i+1)) + ") " + str(words[i]))

    #-----Initialize variables to initial hash values, as they will change-----
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        
        for i in range (0, 64):
            if len(a)> 32:
                a = a[8:]
            if len(b)> 32:
                b = b[8:]
            if len(c)> 32:
                c = c[8:]
            if len(d)> 32:
                d = d[8:]
            if len(e)> 32:
                e = e[8:]
            if len(f)> 32:
                f = f[8:]
            if len(g)> 32:
                g = g[8:]
            if len(h)> 32:
                h = h[8:]

            #The Main Algorithm
            S1 = bitxor(bitxor(rightrotate(e, 6), rightrotate(e, 11)), rightrotate(e, 25))
            ch = bitxor(bitand (e, f), bitand(bitnot(e), g))
            temp1 = bitadd(bitadd(bitadd(bitadd(h, S1), ch), constants[i]), words[i])
            S0 = bitxor(bitxor(rightrotate(a, 2), rightrotate(a, 13)), rightrotate(a, 22))
            maj = bitxor(bitxor(bitand(a, b), bitand(a, c)), bitand(b, c))
            temp2 = bitadd(S0, maj)

            h = g
            g = f
            f = e
            e = bitadd(d, temp1)
            d = c
            c = b
            b = a
            a = bitadd(temp1, temp2)

        h0 = bitadd(h0, a)
        h1 = bitadd(h1, b)
        h2 = bitadd(h2, c)
        h3 = bitadd(h3, d)
        h4 = bitadd(h4, e)
        h5 = bitadd(h5, f)
        h6 = bitadd(h6, g)
        h7 = bitadd(h7, h)

    #Convert to Hex, then to a string.
    h0 = str(bintohex(h0))
    h1 = str(bintohex(h1))
    h2 = str(bintohex(h2))
    h3 = str(bintohex(h3))
    h4 = str(bintohex(h4))
    h5 = str(bintohex(h5))
    h6 = str(bintohex(h6))
    h7 = str(bintohex(h7))

    #Cut off if the length is greater than 8
    if len(h0) > 8:
        h0 = h0[len(h0)-8:]
    if len(h1) > 8:
        h1 = h1[len(h1)-8:]
    if len(h2) > 8:
        h2 = h2[len(h2)-8:]
    if len(h3) > 8:
        h3 = h3[len(h3)-8:]
    if len(h4) > 8:
        h4 = h4[len(h4)-8:]
    if len(h5) > 8:
        h5 = h5[len(h5)-8:]
    if len(h6) > 8:
        h6 = h6[len(h6)-8:]
    if len(h7) > 8:
        h7 = h7[len(h7)-8:]

        
    #Concatenate the strings
    finalhash = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7
    return finalhash
   
bits_per_word = 32
print(shahash('abc',bits_per_word))






