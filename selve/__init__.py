#!/usr/bin/python

import time
import serial

from enum import Enum

from .XML2py import deserialize
from .HW_Thread import *


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

class CommandType(Enum):
    STOP = 0
    DRIVEAWAY = 1
    DEPARTURE = 2
    POSITION_1 = 3
    POSITION_2 = 4

class IveoCommand(Enum):
    FACTORY = "Factory"
    TEACH = "Teach"
    LEARN = "Learn"
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"
    RESULT = "Result"



class MethodCall:

    def __init__(self, method_name, parameters):
        self.method_name = method_name
        self.parameters = parameters

    def serializeToXML(self):
        xmlstr = "<methodCall>"
        xmlstr += "<methodName>"+self.method_name+"</methodName>"
        if (self.parameters.count > 0):
            xmlstr += "<array>"
            for typ, val in self.parameters:
                xmlstr+="<{0}>{1}</{0}>".format(typ, val)
            xmlstr += "</array>"
        xmlstr+= "</methodCall>"
        return xmlstr

class MethodResponse:
            
    def __init__(self, xmlstr):
        self.xmlstr = xmlstr
        deserialize(xmlstr)        

class CommandIveo(MethodCall):

    def __init__(self, method_name, parameters)
         super().__init__("selve.GW.iveo.command" + method_name, parameters)


class CommandSingleIveo(CommandIveo):

    def __init__(self, method_name, iveoID):
        super().__init__(method_name, [(ParameterType.INT, iveoID)])

class CommandMaskIveo(CommandIveo):
    def __init__(self, method_name, mask, command):
        super().__init__(method_name, [(ParameterType.BASE64, mask), (ParameterType.INT, command)])

class IveoCommandFactory(CommandSingleIveo):
     def __init__(self, iveoID):
         super().__init__(CommandIveo.FACTORY, iveoID)

class IveoCommandTeach(CommandSingleIveo):
     def __init__(self, iveoID):
         super().__init__(CommandIveo.TEACH, iveoID)

class IveoCommandLearn(CommandSingleIveo):
     def __init__(self, iveoID):
         super().__init__(CommandIveo.LEARN, iveoID)
         
class IveoCommandManual(CommandMaskIveo):
    def  __init__(self, mask, command):
        super().__init__(CommandIveo.MANUAL, mask, command)

class IveoCommandAutomatic(CommandMaskIveo):
    def  __init__(self, mask, command):
        super().__init__(CommandIveo.AUTOMATIC, mask, command)

class IveoCommandResult(MethodCall):
     def __init__(self, command, mask, state):
          super().__init__(CommandIveo.RESULT, [(ParameterType.INT, command), (ParameterType.BASE64, mask), (ParameterType.INT, state)])


class Gateway():

    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(
        port=port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
        self.hw =  HW_Interface(self.ser, 0.1)
            
    def executeCommand(command):
        self.hw.write_HW(command.serializeToXML())    

    def close():
        self.hw.kill()
        self.ser.close()    


class IveoDevice():

    def __init__(self, gateway, iveoID)
        self.iveoID = iveoID
        self.gateway = gateway
    
    def stop():
        command = IveoCommandManual( , CommandType.STOP)
        gateway.executeCommand(command)

    def moveDown():
        command = IveoCommandManual( , CommandType.DEPARTURE)
        gateway.executeCommand(command)

    def moveUp():
        command = IveoCommandManual( , CommandType.DRIVEAWAY)
        gateway.executeCommand(command)
    
    def moveIntermediatePosition1():
        command = IveoCommandManual( , CommandType.POSITION_1)
        gateway.executeCommand(command)

    def moveIntermediatePosition2():
        command = IveoCommandManual( , CommandType.POSITION_2)
        gateway.executeCommand(command)

