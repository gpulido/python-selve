import base64

def singlemask(id):
    
    #Obtains a base64 encoded to modify just one index
    mask =  64 * [0]
    #need to transform the position
    newid = int((id // 8) * 8  + 7 - (id % 8))    
    mask[newid] = 1
    bitstring = "".join(str(x) for x in mask)
    return base64.b64encode(bitstring_to_bytes(bitstring)).decode('utf8')


def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

def b64bytes_to_bitlist(b):
    byts = base64.b64decode(b)
    return [bool(int(value)) for value in list(''.join([bin(by).lstrip('0b').zfill(8)[::-1] for by in byts]))]

def true_in_list(l):
    return [i for i,v in enumerate(l) if v]


if __name__ == '__main__':
    for i in range (0,64):
        mask = singlemask(i)
        #print(mask)
        b = b64bytes_to_bitlist(mask)
        #print (b)
        c =true_in_list(b)
        #print (c)
        if c[0] != i:
            print("error in: " +str(i))
        else:
            print(str(i) + " OK")

    # a = 8*  bitarray('0', 'little')
    # a[7] = 1
    # print (a)
    # bitdecoded = base64.b64encode(a.tobytes())
    # print(bitdecoded)l
    # mask = singlemask(1)
    # print(mask.decode('utf-8'))


    # a = 64 * [0]
    # a[1] = 1    
    # print(a)   
    # d = "".join(str(x) for x in a)
    # print (d)
    # b = bitstring_to_bytes(d)
    # print(b)
    # c = base64.b64encode(b)  
    # print(c)

    # d = 'AQAAAAAAAAA='
    # b = base64.b64decode(d)
    # d = b'\x01\x00\x00\x00\x00\x00\x00\x00'
    # int(d)
    # test = '10000000'
    # print ("test " + base64.b64encode(test))

    # converted = [access_bit(d,i) for i in range(len(d)*8)]
    # print (converted)
    # bitarray('0',)
    # print(b)
    # c = base64.b64encode(d)
    # print(c)

    #fx4AAAAAAAA=
    #a = 'fx4AAAAAAAA='
    #print (true_in_list(b64bytes_to_bitlist(a)))

