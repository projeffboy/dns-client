import socket
import time
import ipaddress
import struct
import random


def packet(name, queryType):
        packet = struct.pack(">HHHHHH", random.getrandbits(16), 256, 1, 0, 0, 0)

        for string in name.split("."): #decompose and add name to packet
            charCount = len(string)
            packet += struct.pack("B", charCount)
            for character in string:
                packet += struct.pack("!c", character.encode('ascii'))

        packet += struct.pack(">BHH", 0, 1 if not queryType=="MX" and not queryType=="NS" else 15 if not queryType=="NS" else 2, 1)
        return packet


packet()

