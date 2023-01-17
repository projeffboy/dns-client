import struct

class DnsAnswer: # also handles header and questions
    def __init__(self):
        pass

    def print(self, msg):
        # header
        _, flags, qdcount, ancount, nscount, arcount \
            = struct.Struct('!6H').unpack_from(msg) # no need question ID
        aa = (flags & (1 << 10)) != 0
        rcode = flags & 0b1111

        # offset
        offset = struct.Struct('!6H').size

        # question
        offset = self.getQuestions(msg, offset, qdcount)

        if rcode == 3 or ancount + arcount <= 0:
            print('NOTFOUND')
        elif rcode != 0:
            print('ERROR\tUnexpected response (according to RCODE, see below)')
            if rcode == 1:
                print('1 Format error: the name server was unable to interpret the query')
            elif rcode == 2:
                print('2 Server failure: the name server was unable to process this query due to a problem with the name server')
            elif rcode == 4:
                print('4 Not implemented: the name server does not support the requested kind of query')
            elif rcode == 5:
                print('5 Refused: the name server refuses to perform the requested operation for policy reasons')
        else:
            if ancount > 0: print(f'***Answer Section ({ancount} records)***')
            offset = self.getSection(msg, offset, ancount, aa)

            offset = self.getSection(msg, offset, nscount, aa, isAuthoritySection=True) # ignore

            if arcount > 0: print(f'***Additional Section ({arcount} records)***')
            offset = self.getSection(msg, offset, arcount, aa)

    def getQuestions(self, msg, offset, qdcount):
        for _ in range(qdcount):
            _, offset = self.getLabels(msg, offset)

            # queryType, queryClass = struct.Struct('!2H').unpack_from(msg, offset)
            offset += struct.Struct('!2H').size

        return offset

    def getSection(self, msg, offset, count, aa, isAuthoritySection=False):
        for _ in range(count):
            _, offset = self.getLabels(msg, offset) # no need answer name
            atype, = struct.Struct('!H').unpack_from(msg, offset)
            offset += struct.Struct('!2H').size # no need answer class
            ttl, = struct.Struct('!I').unpack_from(msg, offset)
            offset += struct.Struct('!I').size
            rdlength, = struct.Struct('!H').unpack_from(msg, offset)
            offset += struct.Struct('!H').size

            if isAuthoritySection:
                offset += rdlength
            else:
                authority = 'auth' if aa else 'noauth'
                offset = self.printRecord(atype, msg, offset, ttl, authority)

        return offset

    def getLabels(self, msg, offset):
        labels = []

        while True:
            # length of label
            length, = struct.Struct('!B').unpack_from(msg, offset)

            # pointer
            if length & 0b11000000 == 0b11000000:
                pointer, = struct.Struct('!H').unpack_from(msg, offset)
                offset += 2

                return list(labels) + \
                    list(self.getLabels(msg, pointer & 0x03fff)),\
                    offset # 0x03fff is all 1's except for the 2 most significant bits

            if length & 0b11000000 != 0:
                raise Exception('ERROR\tEncountered a byte that is neither a length, label, nor a pointer')

            offset += 1

            # null terminator
            if length == 0:
                return labels, offset

            # label itself
            labels.append(*struct.unpack_from('!%ds' % length, msg, offset))
            offset += length
    
    def printRecord(self, type, msg, offset, ttl, authority):
        if type == 1: # A
            w, x, y, z = struct.unpack_from('!4B', msg, offset)
            offset += struct.Struct('!4B').size

            print(f'IP\t{w}.{x}.{y}.{z}\t{ttl}\t{authority}')
        elif type == 2 or type == 5: # NS or CNAME
            queryTypeName = 'NS' if type == 2 else 'CNAME'
            alias, offset = self.getLabels(msg, offset)

            print(f'{queryTypeName}\t{self.listToName(alias)}\t{ttl}\t{authority}')
        elif type == 15: # MX
            preference, = struct.Struct('!H').unpack_from(msg, offset)
            offset += struct.Struct('!H').size

            exchange, offset = self.getLabels(msg, offset)

            print(f'MX\t{self.listToName(exchange)}\t{preference}\t{ttl}\t{authority}')
        else:
            raise Exception('ERROR\tEncountered a record that isn\'t A, NS, CNAME, or MX')

        return offset

    def listToName(self, l):
        flatL = self.make1dList(l)
        name = b'.'.join(flatL)
        
        return name.decode()

    def make1dList(self, l):
        if not isinstance(l, list):
            return [l]
        
        flatL = []
        for elem in l:
            if type(elem) == list:
                flatL += self.make1dList(elem)
            elif type(elem) != int:
                flatL.append(elem)
        
        return flatL