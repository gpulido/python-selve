#!/usr/bin/python

import time
import serial
from enum import Enum

from utils import * 
from iveo import *
from protocol import *


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


class Gateway():

    def __init__(self, port):
        self.port = port
        self.discover()
    
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
                response_str = "" 
                while True:
                    response = self.ser.readall()
                    response_str += str(response.decode())
                    print("read data: " + response_str)
                    if (response.decode()== ''):
                        break
                    
                self.ser.close()
                return process_response(response_str)
            except Exception as e1:
                print ("error communicating...: " + str(e1))
        else:
            print ("cannot open serial port")
        
        return None

    def serial_data(self, data):
        print (data)

    def discover(self):
        command = IveoCommandGetIds()
        command.execute(self)
        self.devices = [IveoDevice(self, id) for id in command.ids]
        for device in self.devices:
            device.discover_properties()
            print(str(device))
            
    

if __name__ == '__main__':
    #print (singlemask(2).decode('utf-8'))

    #manual = MethodCall("selve.GW.iveo.getIDs",[])
    portname = '/dev/cu.usbserial-DJ00T875'
    gat = Gateway(portname)

    # device1 = IveoDevice(gat, 1)
    # device2 = IveoDevice(gat, 2)
    # device1.moveDown()
    # time.sleep(5)
    # device1.moveUp()
    # device2.moveDown()
    # time.sleep(3)
    # device1.stop()
    # device2.stop
    # time.sleep(1)
    # device1.stop()
    #command = IveoCommandGetIds()
    #command.execute(gat)
    #print (command.ids)
    #response = b'<?xml version="1.0"? encoding="UTF-8">\r\n<methodResponse>\r\n\t<array>\r\n\t\t<string>selve.GW.iveo.commandManual</string>\r\n\t\t<int>1</int>\r\n\t</array>\r\n</methodResponse>\r\n\n<?xml version="1.0"? encoding="UTF-8">\r\n<methodCall>\r\n<methodName>selve.GW.iveo.commandResult</methodName>\r\n\t<array>\r\n\t\t<int>0</int>\r\n\t\t<base64>AQAAAAAAAAA=</base64>\r\n\t\t<int>0</int>\r\n\t</array>\r\n</methodCall>\r\n\n'
    #c = response.decode()
    #print(c)
    #deserialize(response)

