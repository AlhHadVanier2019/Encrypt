from random import getrandbits
import Operators as op
import socket
from time import sleep

class SHA256:
    # --------Unchanging Constants-------
    # these are constants used in the calculations
    # The list is available on wikipedia but must be in binary for the calculations
    constants = ['01000010100010100010111110011000', '01110001001101110100010010010001', '10110101110000001111101111001111',
                 '11101001101101011101101110100101', '00111001010101101100001001011011', '01011001111100010001000111110001',
                 '10010010001111111000001010100100', '10101011000111000101111011010101', '11011000000001111010101010011000',
                 '00010010100000110101101100000001', '00100100001100011000010110111110', '01010101000011000111110111000011',
                 '01110010101111100101110101110100', '10000000110111101011000111111110', '10011011110111000000011010100111',
                 '11000001100110111111000101110100', '11100100100110110110100111000001', '11101111101111100100011110000110',
                 '00001111110000011001110111000110', '00100100000011001010000111001100', '00101101111010010010110001101111',
                 '01001010011101001000010010101010', '01011100101100001010100111011100', '01110110111110011000100011011010',
                 '10011000001111100101000101010010', '10101000001100011100011001101101', '10110000000000110010011111001000',
                 '10111111010110010111111111000111', '11000110111000000000101111110011', '11010101101001111001000101000111',
                 '00000110110010100110001101010001', '00010100001010010010100101100111', '00100111101101110000101010000101',
                 '00101110000110110010000100111000', '01001101001011000110110111111100', '01010011001110000000110100010011',
                 '01100101000010100111001101010100', '01110110011010100000101010111011', '10000001110000101100100100101110',
                 '10010010011100100010110010000101', '10100010101111111110100010100001', '10101000000110100110011001001011',
                 '11000010010010111000101101110000', '11000111011011000101000110100011', '11010001100100101110100000011001',
                 '11010110100110010000011000100100', '11110100000011100011010110000101', '00010000011010101010000001110000',
                 '00011001101001001100000100010110', '00011110001101110110110000001000', '00100111010010000111011101001100',
                 '00110100101100001011110010110101', '00111001000111000000110010110011', '01001110110110001010101001001010',
                 '01011011100111001100101001001111', '01101000001011100110111111110011', '01110100100011111000001011101110',
                 '01111000101001010110001101101111', '10000100110010000111100000010100', '10001100110001110000001000001000',
                 '10010000101111101111111111111010', '10100100010100000110110011101011', '10111110111110011010001111110111',
                 '11000110011100010111100011110010']

    @staticmethod
    def create_salt():
        """
        This method simply uses a random number generator to get a random salt
        :return: A random string
        """
        saltval = op.bintohex(op.inttobin(getrandbits(128)))
        return saltval

    @staticmethod
    def hash(message, messagetype, salt=""):
        """
        This method hashes any string.
        :param message: The messaee that needs to be hashed
        :param salt: A salt is appended to a message, it is optional whether you want to include a salt while hashing
        :param messagetype: The type of message. 'string' or 'file'
        :return: The hashed message
        """
        # ---------Initial Hash Values-------
        # these hash values change for each 512 bit chunk, and start as the following
        h0 = "01101010000010011110011001100111"
        h1 = "10111011011001111010111010000101"
        h2 = "00111100011011101111001101110010"
        h3 = "10100101010011111111010100111010"
        h4 = "01010001000011100101001001111111"
        h5 = "10011011000001010110100010001100"
        h6 = "00011111100000111101100110101011"
        h7 = "01011011111000001100110100011001"

        # -----------------Padding-----------------
        # This sections initializes the first 16 "words". Each "word" is 32 bits.

        # gets the message input and turns it into binary
        if messagetype == "string":
            paddedmessage = op.stringtobin(message + salt)
        elif messagetype == "file":
            file_array = op.getbytearray(message)
            paddedmessage = ""
            for icounter in range(len(file_array)):
                paddedmessage += file_array[icounter]

        else:
            print("Message Type Invalid. Must be 'string' or 'file' defaulted to string")
            paddedmessage = op.stringtobin(message + salt)

        # takes the length of the padded message, converts it into bits, and stores it in bitsinmessage
        bitsinmessage = op.inttobin(len(paddedmessage))

        # Pad the bits in message to be of length 64
        while len(bitsinmessage) < 64:
            bitsinmessage = "0" + bitsinmessage

        # adds a one to the end of the padded message
        paddedmessage += "1"

        # adds 0's to make the length of  (paddedmessage - the length of bitsinmessage) a multiple of 512
        while (len(paddedmessage) + len(bitsinmessage)) % 512 != 0:
            paddedmessage += "0"

        # adds bits in messsage to the end of padded message
        paddedmessage += bitsinmessage

        # creates a variable called fullmessage which is the padded message and is not affected
        fullmessage = paddedmessage

        # for each 512-bit chunk of full message (represented my paddedmessage)the following happens
        for z in range(len(paddedmessage) // 512):
            # words is a list that stores the 32 bit 'words'
            words = []
            # takes the chunk and seperates it into 16, 32 bit words
            paddedmessage = fullmessage[512 * z: 512 * (z + 1)]
            for i in range(16):
                words.append(paddedmessage[32 * i: 32 * (i + 1)])

            # ----------Creating the 64 words from the first 16-------

            # creates the other 48 words using the first 16
            for i in range(16, 64):

                s0 = op.bitxor(op.bitxor(op.rightrotate(words[i - 15], 7), op.rightrotate(words[i - 15], 18)),
                               op.rightshift(words[i - 15], 3))
                s1 = op.bitxor(op.bitxor(op.rightrotate(words[i - 2], 17), op.rightrotate(words[i - 2], 19)),
                               op.rightshift(words[i - 2], 10))

                sum1 = op.bitadd(words[i - 16], s0)
                sum2 = op.bitadd(words[i - 7], s1)
                total = op.bitadd(sum1, sum2)
                while len(total) < 32:
                    total = "0" + total

                # Only take the first 32 bits, starting from the right by chopping of the first 8 bytes
                # if its bigger
                if len(total) > 32:
                    total = total[len(total) - 32:]

                # adds the new word into the list of words
                words.append(total)

            # -----Initialize variables to initial hash values, as they will change-----
            a = h0
            b = h1
            c = h2
            d = h3
            e = h4
            f = h5
            g = h6
            h = h7

            # Checks to make sure the bit length of any variable doesn't exceed 32
            for i in range(64):
                if len(a) > 32:
                    a = a[len(a) - 32:]

                if len(b) > 32:
                    b = b[len(b) - 32:]

                if len(c) > 32:
                    c = c[len(c) - 32:]

                if len(d) > 32:
                    d = d[len(d) - 32:]

                if len(e) > 32:
                    e = e[len(e) - 32:]

                if len(f) > 32:
                    f = f[len(f) - 32:]

                if len(g) > 32:
                    g = g[len(g) - 32:]

                if len(h) > 32:
                    h = h[len(h) - 32:]

                # The Main Algorithm
                S1 = op.bitxor(op.rightrotate(e, 6), op.rightrotate(e, 11), op.rightrotate(e, 25))

                # Choose Function
                ch = op.bitxor(op.bitand(e, f), op.bitand(op.bitnot(e), g))

                temp1 = op.bitadd(h, S1, ch, SHA256.constants[i], words[i])
                S0 = op.bitxor(op.rightrotate(a, 2), op.rightrotate(a, 13), op.rightrotate(a, 22))
                #The majority function
                maj = op.bitxor(op.bitand(a, b), op.bitand(a, c), op.bitand(b, c))

                temp2 = op.bitadd(S0, maj)

                # Variable Swaps and additions
                h = g
                g = f
                f = e
                e = op.bitadd(d, temp1)
                d = c
                c = b
                b = a
                a = op.bitadd(temp1, temp2)

            # Add each letter to its corresponding hash value
            h0 = op.bitadd(h0, a)
            h1 = op.bitadd(h1, b)
            h2 = op.bitadd(h2, c)
            h3 = op.bitadd(h3, d)
            h4 = op.bitadd(h4, e)
            h5 = op.bitadd(h5, f)
            h6 = op.bitadd(h6, g)
            h7 = op.bitadd(h7, h)

        # Convert to Hex, then to a string.
        h0 = str(op.bintohex(h0))
        h1 = str(op.bintohex(h1))
        h2 = str(op.bintohex(h2))
        h3 = str(op.bintohex(h3))
        h4 = str(op.bintohex(h4))
        h5 = str(op.bintohex(h5))
        h6 = str(op.bintohex(h6))
        h7 = str(op.bintohex(h7))

        # Cut off if the length of the hex string is greater than 8
        if len(h0) > 8:
            h0 = h0[len(h0) - 8:]
        if len(h1) > 8:
            h1 = h1[len(h1) - 8:]
        if len(h2) > 8:
            h2 = h2[len(h2) - 8:]
        if len(h3) > 8:
            h3 = h3[len(h3) - 8:]
        if len(h4) > 8:
            h4 = h4[len(h4) - 8:]
        if len(h5) > 8:
            h5 = h5[len(h5) - 8:]
        if len(h6) > 8:
            h6 = h6[len(h6) - 8:]
        if len(h7) > 8:
            h7 = h7[len(h7) - 8:]

        # Concatenate the strings
        finalhash = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7
        return finalhash

    @staticmethod
    def send(serverIP, message):
        """
        :param serverIP: This is the IP of the computer you want to send the message to.
        :param message: The message to be sent to the computer.
        """
        hashedmessage = SHA256.hash(message, "string")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender:
            sender.connect((serverIP, 5432))
            sender.send(bytes(hashedmessage, encoding='utf-8'))

        time.sleep(0.2)

    @staticmethod
    def server_recv():
        """
        This initializes this computer as a server which can receive messages
        from anyone using the send function above.
        """
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.bind(("0.0.0.0", 5432))
                server.listen()
                connection, address = server.accept()
                server.setblocking(False)
                with connection:
                    print(address[0], "connected")
                    print(connection.recv(4096).decode(encoding='utf-8', errors='ignore'))


