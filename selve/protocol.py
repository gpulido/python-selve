
from enum import Enum
from itertools import chain
import untangle
import logging

class DeviceType(Enum):
    UNKNOWN = 0
    SHUTTER = 1
    BLIND = 2
    AWNING = 3
    SWITCH = 4
    DIMMER = 5
    NIGHT_LIGHT = 6
    DRAWN_LIGHT = 7
    HEATING = 8
    COOLING = 9
    COOLING2 = 10
    GATEWAY = 11

class CommandType(Enum):
    STOP = 0
    DRIVEAWAY = 1
    DEPARTURE = 2
    POSITION_1 = 3
    POSITION_2 = 4

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
    
    def execute(self, gateway):
        response = gateway.executeCommand(self)
        if response != None and isinstance(response, MethodResponse):
            self.process_response(response)
    
    def process_response(self, methodResponse):
        print (methodResponse)


class MethodResponse:

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

class ErrorResponse:

    def __init__(self, message, code):
        self.message = message
        self.code = code


def create_error(obj):
    return ErrorResponse(obj.methodResponse.fault.array.string.cdata, obj.methodResponse.fault.array.int.cdata ) 

def create_response(obj):
    array = obj.methodResponse.array
    methodName = list(array.string)[0].cdata
    str_params_tmp = list(array.string)[1:]
    str_params = [(ParameterType.STRING, v.cdata) for v in str_params_tmp]
    int_params = []
    if hasattr(array, ParameterType.INT.value):
        int_params = [(ParameterType.INT, v.cdata) for v in list(array.int)]
    b64_params = []
    if hasattr(array, ParameterType.BASE64.value):
        b64_params = [(ParameterType.BASE64, v.cdata) for v in list(array.base64)]
    paramslist = [str_params, int_params, b64_params]
    flat_params_list = list(chain.from_iterable(paramslist))
    return MethodResponse(methodName, flat_params_list)


def process_response(xmlstr):
    msgs = xmlstr.split('<?xml version="1.0"? encoding="UTF-8">')
    msgs = [untangle.parse(res) for res in msgs if res!='']
    list_res = [res for res in msgs if hasattr(res, 'methodResponse')]
    if not list_res:
        logging.error("Bad response format")
        return None
    obj = list_res[0]
    if hasattr(obj.methodResponse, 'fault'):
        return create_error(obj)
    return create_response(obj)

def main():

    selve_string = '''<?xml version="1.0" encoding="UTF-8"?>
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

    a ='<?xml version="1.0"? encoding="UTF-8">\r\n<methodResponse>\r\n\t<array>\r\n\t\t<string>selve.GW.iveo.getIDs</string>\r\n\t\t<base64>fx4AAAAAAAA=</base64>\r\n\t</array>\r\n</methodResponse>\r\n\n'

    process_response(selve_string)


if __name__ == '__main__':
    main()
