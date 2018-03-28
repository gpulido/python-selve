#!/usr/bin/env python

import selve
import sys
import argparse


def list_devices(args):
    print (list_devices)
    gat = selve.Gateway(args.port)
    gat.list_devices()

def action(args):
    gat = selve.Gateway(args.port, args.discover)
    if args.discover: 
        if not gat.is_id_registered(args.iveoId):    
            sys.exit("The device is not registered on the gateway")
        device = gat.devices[args.iveoId]
    else:
        device = selve.IveoDevice(gat, args.iveoId)

    if args.command == 'stop':
        device.stop(args.automation)
    elif args.command == 'up':
        device.moveUp(args.automation)
    elif args.command == 'down':
        device.moveDown(args.automation)
    elif args.command == 'pos1':
        device.moveIntermediatePosition1(args.automation)
    elif args.command == 'pos2':
        device.moveIntermediatePosition2(args.automation)

def teach(args):
    gat = selve.Gateway(args.port, False)
    device = selve.IveoDevice(gat, args.iveoId)
    device.learnChannel(args.channel)


parser = argparse.ArgumentParser(prog='selve-cli')
parser.add_argument("port", type=str, help="serial port")
subparsers = parser.add_subparsers(help='sub-command help')
parser_list = subparsers.add_parser('list', help="print the list of registered  devices")
parser_list.set_defaults(func=list_devices)

parser_action = subparsers.add_parser('action', help="Command to execute over the device")
parser_action.add_argument("command", choices = ['stop', 'up', 'down', 'pos1', 'pos2'], default = 'stop')
parser_action.add_argument("iveoId", type=int, help="IveoId / channel where the device is registered")
parser_action.add_argument("--automation", type=bool, default=False, help="Set to true if the command has to be executed as an automation mecanism to not override manual interaction with the device")
parser_action.add_argument("--discover", type=bool, default= False, help="Force the discover of devices before trying to execute the command")
parser_action.set_defaults(func=action)

parser_teach = subparsers.add_parser('teach', help="Command to teach a channel into an already learned device")
parser_teach.add_argument("channel", type=int, help="channel to be teach")
parser_teach.add_argument("iveoId", type=int, help="device that is going to learn the channel")
parser_teach.set_defaults(func=teach)

args = parser.parse_args()
args.func(args)









