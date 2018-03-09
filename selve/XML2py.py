'''
XML2Py - XML to Python de-serialization

This code transforms an XML document into a Python data structure

Usage:
    deserializer = XML2Py()
    python_object = deserializer.parse( xml_string )
    print xml_string
    print python_object
'''

from lxml import objectify
import untangle

def deserialize(response_xml_text):
    response = objectify.fromstring(response_xml_text.encode('utf8'))
    if (response[0].text == 'fault'):
        print ('commanderror')
    else:        
        [element.tag for element in response.array.iterchildren]

def main():

    selve_string = '''<?xml version="1.0"?>
    <methodResponse>
        <array>
            <string>Methodenname</string>
            <string>Parameter 1</string>
            <int>Parameter 2</int>
            <base64>Parameter 3</base64>
        </array>
    </methodResponse>
    '''

    error_string = '''<?xml version="1.0" encoding="UTF-8"?>
    <methodResponse>
        <fault>
            <array>
                <string>Method not supported!</string>                
                <int>2</int>                
            </array>
        </fault>
    </methodResponse>
    '''

    test = objectify.fromstring(error_string.encode('utf8'))
    print (test)
    if test[0].text == 'fault':
        print ('commanderror' )       
    else:        
        [element.tag for element in test.array.iterchildren]


if __name__ == '__main__':
    main()