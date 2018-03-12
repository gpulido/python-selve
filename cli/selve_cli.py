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
        gat.devices[args.iveoId].stop()
    elif args.command == 'up':
        gat.devices[args.iveoId].moveUp()
    elif args.command == 'down':
        gat.devices[args.iveoId].moveDown()
    elif args.command == 'pos1':
        gat.devices[args.iveoId].moveIntermediatePosition1()
    elif args.command == 'pos2':
        gat.devices[args.iveoId].moveIntermediatePosition2()


parser = argparse.ArgumentParser(prog='selve-cli')
parser.add_argument("port", type=str, help="serial port")
subparsers = parser.add_subparsers(help='sub-command help')
parser_list = subparsers.add_parser('list', help="print the list of registered  devices")
parser_list.set_defaults(func=list_devices)

parser_action = subparsers.add_parser('action', help="Command to execute over the device")
parser_action.add_argument("command", choices = ['stop', 'up', 'down', 'pos1', 'pos2'], default = 'stop')
parser_action.add_argument("iveoId", type=int, help="IveoId / channel where the device is registered'")
parser_action.set_defaults(func=action)

args = parser.parse_args()
args.func(args)










