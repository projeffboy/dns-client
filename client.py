import socket
import time
import struct
import random
from dns_answer import DnsAnswer
# import traceback

class Client:
    def __init__(self, arguments):
        self.timeout = arguments.timeout
        self.retries = arguments.retries
        self.port = arguments.port
        self.queryType = 'A' if not arguments.mx and not arguments.ns\
            else 'MX' if not arguments.ns\
            else 'NS' # Either A, MX, or NS
        self.server = arguments.server
        self.name = arguments.name

    def __str__(self):
        return f'''
Name: {self.name}
Server: {self.server}
Max retries: {self.retries}
Timeout: {self.timeout}
Port: {self.port}
Query type: {self.queryType}
        '''
        
    def sendQuery(self):
        counter = 0

        print(f'''
DNSClient sending request for {self.name}
Server: {self.server}
Request type: {self.queryType}
        ''')

        serverAddressPort = (self.server, self.port)
        bufferSize = 1024
        sendPacket = dnsQuestion(self.name, self.queryType)
        # print(sendPacket)

        for counter in range(self.retries + 1): # no. retries + original attempt
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udpClientSocket:
                    udpClientSocket.settimeout(self.timeout)
                    
                    start = time.time_ns() #start timer

                    udpClientSocket.sendto(sendPacket, serverAddressPort)
                    response, _ = udpClientSocket.recvfrom(bufferSize)
                    runtime = (time.time_ns() - start) / 10E9
                    
                    if response:
                        print(f'Response received after {runtime} seconds ({counter} retries)\n')
                        # print(response)
                        DnsAnswer().print(response)
                        break
            except socket.timeout as e:
                print(e)
                #if counter == 0:
                #    traceback.print_exc()
                counter += 1
            except socket.error as e:
                print('ERROR\tA non-timeout related socket error, perhaps the remote host forcibly closed your connection')
                break
            except Exception as e:
                print(e)
                break

        if counter >= self.retries + 1:
            print(f'ERROR\tMaximum number of retries {self.retries} exceeded') 
        return  

def dnsQuestion(name, queryType): # creates header and question
    # below packet header should end with \x01\x00\x00\x01\x00\x00\x00\x00\x00\x00
    packet = struct.pack('!6H', random.getrandbits(16), 256, 1, 0, 0, 0)

    # qname
    for label in name.split('.'): # decompose and add name to packet
        packet += struct.pack('B', len(label))
        packet += struct.pack('!%ds' % len(label), label.encode())

    # qname terminator, qtype, qclass (0x0001)
    packet += struct.pack(
        '>BHH', 0, \
        1 if not queryType=='MX' and not queryType=='NS' \
        else 15 if not queryType=='NS' \
        else 2
        , 1
    )
    return packet