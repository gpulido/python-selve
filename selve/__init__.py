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

class IveoCommand(Enum):
    FACTORY = "commandFactory"
    TEACH = "commandTeach"
    LEARN = "commandLearn"
    MANUAL = "commandManual"
    AUTOMATIC = "commandAutomatic"
    RESULT = "commandResult"
    GETIDS = "getIDs"



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

class MethodResponse:
            
    def __init__(self, xmlstr):
        self.xmlstr = xmlstr
        #utils.deserialize(xmlstr)        

class CommandIveo(MethodCall):

    def __init__(self, method_name, parameters = []):
         super().__init__("selve.GW.iveo." + method_name.value, parameters)

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

class IveoCommandGetIds(CommandIveo):
    def __init__(self):
        super().__init__(IveoCommand.GETIDS)

class Gateway():

    def __init__(self, port):
        self.port = port
        #self.configserial()
        #self.hw =  HW_Interface(self.ser, 100)
        #self.hw.register_callback(self.serial_data)
    
    def configserial(self):
        self.ser = serial.Serial(
            port=self.port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        self.ser.timeout = 0
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 2

            
    def executeCommand(self, command):
        commandstr = command.serializeToXML()
        print( "Gateway writting: " + str(commandstr))

        
        try:
            self.configserial()

        except Exception as e:
            print ("error open serial port: " + str(e))
            exit()
        
        if self.ser.isOpen():
            try:
                self.ser.flushInput()
                self.ser.flushOutput()
                
                self.ser.write(commandstr)
                time.sleep(0.5)
                numOfLines = 0
                while True:
                    response = self.ser.readall()
                    print("read data: " + str(response.decode()))
                    if (response.decode()== ''):
                        break
                    
                    #numOfLines = numOfLines + 1
                    #if (numOfLines >= 5 ):
                    #    break
                
                self.ser.close()
            except Exception as e1:
                print ("error communicating...: " + str(e1))
        else:
            print ("cannot open serial port")

        
        #self.hw.write_HW(commandstr)    

    #def close(self):
        #self.hw.kill()
        #self.ser.close() 

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
        command = IveoCommandManual(self.mask , CommandType.DRIVEAWAY)
        self.gateway.executeCommand(command)

    def moveUp(self):
        command = IveoCommandManual(self.mask , CommandType.DEPARTURE)
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
    gat = Gateway(portname)
    # device1 = IveoDevice(gat, 1)
    # time.sleep(1)
    # device1.stop()
    gat.executeCommand(IveoCommandGetIds())
    #response = b'<?xml version="1.0"? encoding="UTF-8">\r\n<methodResponse>\r\n\t<array>\r\n\t\t<string>selve.GW.iveo.commandManual</string>\r\n\t\t<int>1</int>\r\n\t</array>\r\n</methodResponse>\r\n\n<?xml version="1.0"? encoding="UTF-8">\r\n<methodCall>\r\n<methodName>selve.GW.iveo.commandResult</methodName>\r\n\t<array>\r\n\t\t<int>0</int>\r\n\t\t<base64>AQAAAAAAAAA=</base64>\r\n\t\t<int>0</int>\r\n\t</array>\r\n</methodCall>\r\n\n'
    #c = response.decode()
    #print(c)
    #deserialize(response)

