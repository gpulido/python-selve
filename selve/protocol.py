import untangle


class ParameterType(Enum):
    INT = "int"
    STRING = "string"
    BASE64 = "base64"

class MethodCall:

    def __init__(self, method_name, parameters = []):
        self.method_name = method_name
        self.parameters = parameters

    def serializeToXML(self):
        xmlstr = "<methodCall>"
        xmlstr += "<methodName>"+self.method_name+"</methodName>"
        if (len(self.parameters) > 0):
            xmlstr += "<array>"
            for typ, val in self.parameters:
                xmlstr+="<{0}>{1}</{0}>".format(typ.value, val)
            xmlstr += "</array>"
        xmlstr+= "</methodCall>"
        return xmlstr.encode('utf-8')

class ErrorResponse:

    def __init__(self, message, code):
        self.message = message
        self.code = code


def create_error(obj):
    return ErrorResponse(obj.methodResponse.fault.string.cdata, obj.methodResponse.fault.int.cdata ) 

def processResponse(obj):
    array = obj.methodResponse.array
    methodName = list(array.string)[0].cdata
    str_params_tmp = list(array.string)[1:]
    str_params = [(ParameterType.STRING, v) for v in str_params_tmp]
    int_params = []
    if hasattr(array, ParameterType.INT):
        int_params = [(ParameterType.INT, v) for v in list(array.int)]
    b64_params = []
    if hasattr(array, ParameterType.BASE64):
        b64_params = [(ParameterType.BASE64, v) for v in list(array.base64)]
    paramslist = str_params.extend(int_params).extend(b64_params)
    return MethodResponse(methodName, paramslist)


def process_response(xmlstr):
    obj = untangle.parse(xmlstr)
    if hasattr(obj.methodResponse, 'fault'):
        return create_error(obj)
    else:
        return create_response(obj)



class MethodResponse:

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

class ErrorResponse:

    def __init__(self, message, code):
        self.message = message
        self.code = code

ef main():

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
