#!/usr/bin/python

import time
import serial

from enum import Enum

ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)




class ParameterType(Enum):
    INT = "int"
    STRING = "string"
    BASE64 = "base64"

class DeviceType(Enum):
    NOTYPE = 0
    BLIND = 1
    AWNING = 2
    AWNING2 = 3
    DIMMER = 4
    DIMMER2 = 5
    DIMMER3 = 6
    DIM = 7
    HEAT = 8
    HEAT2 = 9
    COOLING = 10
    GATEWAY = 11


class MethodCall:

    def __init__(self, method_name, parameters):
        self.method_name = method_name
        self.parameters = parameters

    def serializeToXML(self):
        xmlstr = "<methodCall>"
        xmlstr += "<methodName>"+self.method_name+"</methodName>"
        for typ, val in self.parameters:
            xmlstr+="<{0}>{1}</{0}>".format(typ, val)
        xmlstr+= "</methodCall>"
        return smlstr

class MethodResponse:
        
    def __init__(self, str):
        self.str = str
        //TODO: deserialize str
        

    
