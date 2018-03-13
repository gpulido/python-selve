#!/usr/bin/env python

import selve
import sys
import argparse


def list_devices(args):
    print (list_devices)
    gat = selve.Gateway(args.port)
    gat.list_devices()

def action(args):
    gat = selve.Gateway(args.port)
    if not gat.is_id_registered(args.iveoId):    
        sys.exit("The device is not registered on the gateway")

    if args.command == 'stop':
        gat.devices[args.iveoId].stop(args.automation)
    elif args.command == 'up':
        gat.devices[args.iveoId].moveUp(args.automation)
    elif args.command == 'down':
        gat.devices[args.iveoId].moveDown(args.automation)
    elif args.command == 'pos1':
        gat.devices[args.iveoId].moveIntermediatePosition1(args.automation)
    elif args.command == 'pos2':
        gat.devices[args.iveoId].moveIntermediatePosition2(args.automation)


parser = argparse.ArgumentParser(prog='selve-cli')
parser.add_argument("port", type=str, help="serial port")
subparsers = parser.add_subparsers(help='sub-command help')
parser_list = subparsers.add_parser('list', help="print the list of registered  devices")
parser_list.set_defaults(func=list_devices)

parser_action = subparsers.add_parser('action', help="Command to execute over the device")
parser_action.add_argument("command", choices = ['stop', 'up', 'down', 'pos1', 'pos2'], default = 'stop')
parser_action.add_argument("iveoId", type=int, help="IveoId / channel where the device is registered")
parser_action.add_argument("--automation", type=bool, default=False, help="Set to true if the command has to be executed as an automation mecanism to not override manual interaction with the device")
parser_action.set_defaults(func=action)

args = parser.parse_args()
args.func(args)










