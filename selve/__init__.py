#!/usr/bin/python

import time
import serial
from HW_Thread import *
from utils import *
from enum import Enum



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
        if (len(self.parameters) > 0):
            xmlstr += "<array>"
            for typ, val in self.parameters:
                xmlstr+="<{0}>{1}</{0}>".format(typ.value, val)
            xmlstr += "</array>"
        xmlstr+= "</methodCall>"
        return xmlstr

class MethodResponse:
            
    def __init__(self, xmlstr):
        self.xmlstr = xmlstr
        #utils.deserialize(xmlstr)        

class CommandIveo(MethodCall):

    def __init__(self, method_name, parameters):
         super().__init__("selve.GW.iveo.command" + method_name.value, parameters)

class CommandSingleIveo(CommandIveo):

    def __init__(self, method_name, iveoID):
        super().__init__(method_name, [(ParameterType.INT, iveoID)])

class CommandMaskIveo(CommandIveo):

    def __init__(self, method_name, mask, command):
        super().__init__(method_name, [(ParameterType.BASE64, mask), (ParameterType.INT, command.value)])

class IveoCommandFactory(CommandSingleIveo):

     def __init__(self, iveoID):
         super().__init__(IveoCommand.FACTORY, iveoID)

class IveoCommandTeach(CommandSingleIveo):
     def __init__(self, iveoID):
         super().__init__(IveoCommand.TEACH, iveoID)

class IveoCommandLearn(CommandSingleIveo):
     def __init__(self, iveoID):
         super().__init__(IveoCommand.LEARN, iveoID)
         
class IveoCommandManual(CommandMaskIveo):
    def  __init__(self, mask, command):
        super().__init__(IveoCommand.MANUAL, mask, command)

class IveoCommandAutomatic(CommandMaskIveo):
    def  __init__(self, mask, command):
        super().__init__(IveoCommand.AUTOMATIC, mask, command)

class IveoCommandResult(MethodCall):
     def __init__(self, command, mask, state):
          super().__init__(IveoCommand.RESULT, [(ParameterType.INT, command), (ParameterType.BASE64, mask), (ParameterType.INT, state)])


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
        self.hw =  HW_Interface(self.ser, 10)
        self.hw.register_callback(self.serial_data)
            
    def executeCommand(self, command):
        commandstr = command.serializeToXML()
        print( "Gateway writting: " + commandstr)
        self.hw.write_HW(commandstr)    

    def close(self):
        self.hw.kill()
        self.ser.close() 

    def serial_data(self, data):
        print (data)


class IveoDevice():

    def __init__(self, gateway, iveoID):
        self.iveoID = iveoID
        self.gateway = gateway
        self.mask = singlemask(iveoID)
    
    def stop(self):
        command = IveoCommandManual(self.mask , CommandType.STOP)
        self.gateway.executeCommand(command)

    def moveDown(self):
        command = IveoCommandManual(self.mask , CommandType.DEPARTURE)
        self.gateway.executeCommand(command)

    def moveUp(self):
        command = IveoCommandManual(self.mask , CommandType.DRIVEAWAY)
        self.gateway.executeCommand(command)
    
    def moveIntermediatePosition1(self):
        command = IveoCommandManual(self.mask , CommandType.POSITION_1)
        self.gateway.executeCommand(command)

    def moveIntermediatePosition2(self):
        command = IveoCommandManual(self.mask , CommandType.POSITION_2)
        self.gateway.executeCommand(command)

if __name__ == '__main__':
    #print (singlemask(2).decode('utf-8'))

    #manual = MethodCall("selve.GW.iveo.getIDs",[])
    portname = '/dev/cu.usbserial-DJ00T875'
    ser = serial.Serial(
        port=portname,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    teststring = '<methodCall><methodName>selve.GW.iveo.commandManual</methodName><array><base64>AQAAAAAAAAA=</base64><int>1</int></array></methodCall>'
    ser.write(teststring.encode())
    #time.sleep(3)
    while(1):
        read_val = ser.read(size=64)
        print(read_val)
    #ser.write(manual.serializeToXML().encode())
    #print (singlemask(2).decode('utf-8'))
    #command = IveoCommandManual(singlemask(1).decode('utf-8'), CommandType.DEPARTURE)
    #a = command.serializeToXML()
    #print (a)
    #ser.write(a.encode())
    #gat = Gateway(portname)
    #device1 = IveoDevice(gat, 1)
    #device1.moveIntermediatePosition1()
    #gat.close()
    ser.close()

