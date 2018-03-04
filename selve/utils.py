import base64
from bitarray import bitarray
from lxml import objectify

#def deserialize(response_xml_text):
#    response = objectify.fromstring(response_xml_text.encode('utf8'))
#    if (response[0].text == 'fault'):
#        print ('commanderror')
#    else:        
#        [element.tag for element in response.array.iterchildren]

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def fixed_array():
    return 64 * bitarray('0', 'little')

def singlemask(id):
    mask = fixed_array()
    mask[id] = 1
    return base64.b64encode(mask.tobytes())

def access_bit(data, num):
    base = int(num/8)
    shift = num % 8
    return (data[base] & (1<<shift)) >> shift

if __name__ == '__main__':
    a = 8*  bitarray('0', 'little')
    a[7] = 1
    print (a)
    bitdecoded = base64.b64encode(a.tobytes())
    print(bitdecoded)

    d = 'AQAAAAAAAAA='
    b = base64.b64decode(d)
    d = b'\x01\x00\x00\x00\x00\x00\x00\x00'
    test = '10000000'
    print ("test " + base64.b64encode(test))

    converted = [access_bit(d,i) for i in range(len(d)*8)]
    print (converted)
    bitarray('0',)
    print(b)
    c = base64.b64encode(d)
    print(c)