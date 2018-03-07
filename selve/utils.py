import base64
#from bitarray import bitarray
from lxml import objectify

def deserialize(response_xml_text):
   response = objectify.fromstring(response_xml_text)
   if (response[0].text == 'fault'):
       print ('commanderror')
   else:        
       [element.tag for element in response.array.iterchildren]

# def tobits(s):
#     result = []
#     for c in s:
#         bits = bin(ord(c))[2:]
#         bits = '00000000'[len(bits):] + bits
#         result.extend([int(b) for b in bits])
#     return result

# def frombits(bits):
#     chars = []
#     for b in range(len(bits) // 8):
#         byte = bits[b*8:(b+1)*8]
#         print(byte)
        
#         chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
#     return ''.join(chars)

# def fixed_array():
#     return 64 * bitarray('0', 'little')

def singlemask(id):
    #Obtains a base64 encoded to modify just one index
    mask =  64 * [0]
    #need to transform the position
    newid = int((id // 8) * 8  + 8 - (id % 8))    
    mask[newid] = 1
    bitstring = "".join(str(x) for x in mask)
    return base64.b64encode(bitstring_to_bytes(bitstring)).decode('utf8')

# def access_bit(data, num):
#     base = int(num/8)
#     shift = num % 8
#     return (data[base] & (1<<shift)) >> shift

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

def b64bytes_to_bitlist(b):
    byts = base64.b64decode(b)
    return [bool(int(value)) for value in list(''.join([bin(by).lstrip('0b').zfill(8)[::-1] for by in byts]))]

def true_in_list(l):
    return  [i for i,v in enumerate(l) if v]


if __name__ == '__main__':
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
    a = 'fx4AAAAAAAA='
    print (true_in_list(b64bytes_to_bitlist(a)))

