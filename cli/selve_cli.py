#!/usr/bin/env python

import selve
import sys
import argparse

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--list", help="print the list of registered  devices")
group.add_argument("--action", choices = ['stop', 'up', 'down', 'pos1', 'pos2'], default = 'stop', help="Command to execute over the device")
parser.add_argument("--port", help="serial port")
parser.add_argument("--iveoId", type=int, help="IveoId / channel where the device is registered'")
args = parser.parse_args()

gat = selve.Gateway(args.port)

if  args.list:
    gat.list_devices()
    sys.exit()
elif not gat.is_id_registered(args.iveoId):    
    sys.exit("The device is not registered on the gateway")

if args.action == 'stop':
    gat.devices[args.iveoId].stop()
elif args.action == 'up':
    gat.devices[args.iveoId].moveUp()
elif args.action == 'down':
    gat.devices[args.iveoId].moveDown()
elif args.action == 'pos1':
    gat.devices[args.iveoId].moveIntermediatePosition1()
elif args.action == 'pos2':
    gat.devices[args.iveoId].moveIntermediatePosition2()







