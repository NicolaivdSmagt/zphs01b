# -*- coding: utf-8 -*-
# original: https://raw.githubusercontent.com/UedaTakeyuki/slider/master/zphs01b.py
#
# © Takeyuki UEDA 2015 -
import sys
import argparse
import json
import zphs01b.__init__ as zphs01b
#import __init__ as zphs01b

parser = argparse.ArgumentParser(
  description='''return CO2 concentration as object as {'co2': 416}''',
)
parser.add_argument("--serial_device",
                    type=str,
                    help='''Use this serial device file''')

parser.add_argument("--serial_console_untouched",
                    action='store_true',
                    help='''Don't close/reopen serial console before/after sensor reading''')


group = parser.add_mutually_exclusive_group()

group.add_argument("--version",
                    action='store_true',
                    help='''show version''')
group.add_argument("--all",
                    action='store_true',
                    help='''return all as json''')
group.add_argument("--abc_on",
                    action='store_true',
                    help='''Set ABC functionality on model B as ON.''')
group.add_argument("--abc_off",
                    action='store_true',
                    help='''Set ABC functionality on model B as OFF.''')
parser.add_argument("--span_point_calibration",
                    type=int,
                    help='''Call calibration function with SPAN point''')
parser.add_argument("--zero_point_calibration",
                    action='store_true',
                    help='''Call calibration function with ZERO point''')
parser.add_argument("--detection_range_10000",
                    action='store_true',
                    help='''Set detection range as 10000''')
parser.add_argument("--detection_range_5000",
                    action='store_true',
                    help='''Set detection range as 5000''')
parser.add_argument("--detection_range_2000",
                    action='store_true',
                    help='''Set detection range as 2000''')

args = parser.parse_args()

if args.serial_device is not None:
  zphs01b.set_serialdevice(args.serial_device)

#print(args.serial_console_untouched)

if args.abc_on:
  zphs01b.abc_on(args.serial_console_untouched)
  print ("Set ABC logic as on.")
elif args.abc_off:
  zphs01b.abc_off(args.serial_console_untouched)
  print ("Set ABC logic as off.")
elif args.version:
  print (zphs01b.version)
elif args.all:
  value = zphs01b.read_all(args.serial_console_untouched)
  print (json.dumps(value))
else:
  value = zphs01b.read(args.serial_console_untouched)
  print (json.dumps(value))

sys.exit(0)
