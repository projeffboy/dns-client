#!/usr/bin/python3.9

import argparse
from client import Client

def __main__():
    arguments = {}

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-t', dest='timeout', type=int, action='store', default=5)
    parser.add_argument('-r', dest='retries', type=int, action='store', default=3)
    parser.add_argument('-p',  dest='port', type=int, action='store', default=53)

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-mx', dest='mx', action='store_true',  default=False)
    group.add_argument('-ns', dest='ns', action='store_true',  default=False)
    
    parser.add_argument(action='store', dest='server')
    parser.add_argument(action='store', dest='name')

    try:
        arguments = parser.parse_args()
    except:
        print('ERROR\tIncorrect input syntax: See above comment')
        return

    if arguments.server[0] != '@':
        print('ERROR\tIncorrect input syntax: the server name is not preceded by an @ symbol')
    elif arguments.timeout <= 0:
        print('ERROR\tIncorrect input: Timeout cannot be <= 0')
    elif arguments.retries < 0:
        print('ERROR\tIncorrect input: Retries cannot be < 0')
    else:
        arguments.server = arguments.server[1:]    
        client = Client(arguments)
        # print(client)
        client.sendQuery()


if __name__ == '__main__':
    __main__()


# python DnsClient.py -mx -t 10 -r 7 8.8.8.8 mcgill.ca 