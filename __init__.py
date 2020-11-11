# -*- coding: utf-8 -*-
# original: https://raw.githubusercontent.com/UedaTakeyuki/slider/master/zphs01b.py
#
# © Takeyuki UEDA 2015 -

import serial
import time
import subprocess
import traceback
import getrpimodel
import struct
import platform
import os.path

# setting
version = "0.6.3"
pimodel        = getrpimodel.model
pimodel_strict = getrpimodel.model_strict()

if os.path.exists('/dev/serial0'):
  partial_serial_dev = 'serial0'
elif pimodel == "3 Model B" or pimodel_strict == "Zero W":
  partial_serial_dev = 'ttyS0'
else:
  partial_serial_dev = 'ttyAMA0'
  
serial_dev = '/dev/%s' % partial_serial_dev
#stop_getty = 'sudo systemctl stop serial-getty@%s.service' % partial_serial_dev
#start_getty = 'sudo systemctl start serial-getty@%s.service' % partial_serial_dev
#start_getty = ['sudo', 'systemctl', 'start', 'serial-getty@%s.service' % partial_serial_dev]
#stop_getty = ['sudo', 'systemctl', 'stop', 'serial-getty@%s.service' % partial_serial_dev]

# major version of running python
p_ver = platform.python_version_tuple()[0]

def start_getty():
#  p = subprocess.call(start_getty, stdout=subprocess.PIPE, shell=True)
  start_getty = ['sudo', 'systemctl', 'start', 'serial-getty@%s.service' % partial_serial_dev]
  p = subprocess.call(start_getty)

def stop_getty():
#  p = subprocess.call(stop_getty, stdout=subprocess.PIPE, shell=True)
  stop_getty = ['sudo', 'systemctl', 'stop', 'serial-getty@%s.service' % partial_serial_dev]
  p = subprocess.call(stop_getty)

def set_serialdevice(serialdevicename):
  global serial_dev
  serial_dev = serialdevicename

def connect_serial():
  return serial.Serial(serial_dev,
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1.0)

def zphs01b():
  try:
    ser = connect_serial()
    while 1:
      result=ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
      s=ser.read(26)

      if p_ver == '2':
        if len(s) >= 4 and s[0] == "\xff" and s[1] == "\x86":
          return {'pm1.0': ord(s[2])*256 + ord(s[3]),
                  'pm2.5': ord(s[4])*256 + ord(s[5]),
                  'pm10': ord(s[6])*256 + ord(s[7]),
                  'co2': ord(s[8])*256 + ord(s[9]),
                  'voc': ord(s[10]),
                  'temperature': ((ord(s[11])*256 + ord(s[12]))-435)*0.1,
                  'rh': ord(s[13])*256 + ord(s[14]),
                  'ch2o': (ord(s[15])*256 + ord(s[16]))*0.001,
                  'co': (ord(s[17])*256 + ord(s[18]))*0.1,
                  'o3': (ord(s[19])*256 + ord(s[20]))*0.01,
                  'no2': (ord(s[21])*256 + ord(s[22]))*0.01
                  }
        break
      else:
        if len(s) >= 4 and s[0] == 0xff and s[1] == 0x86:
          return {'pm1.0': s[2]*256 + s[3],
                  'pm2.5': s[4]*256 + s[5],
                  'pm10': s[6]*256 + s[7],
                  'co2': s[8]*256 + s[9],
                  'voc': s[10],
                  'temperature': ((s[11]*256 + s[12])-435)*0.1,
                  'rh': s[13]*256 + s[14],
                  'ch2o': (s[15]*256 + s[16])*0.001,
                  'co': (s[17]*256 + s[18])*0.1,
                  'o3': (s[19]*256 + s[20])*0.01,
                  'no2': (s[21]*256 + s[22])*0.01
                  }
        break
  except:
     traceback.print_exc()

def read(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()

  result = zphs01b()

  if not serial_console_untouched:
    start_getty()
  if result is not None:
    return result

def read_all(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  try:
    ser = connect_serial()
    while 1:
      result=ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
      s=ser.read(26)

      if p_ver == '2':
        if len(s) >= 9 and s[0] == "\xff" and s[1] == "\x86":
          return {'pm1.0': ord(s[2])*256 + ord(s[3]),
                  'pm2.5': ord(s[4])*256 + ord(s[5]),
                  'pm10': ord(s[6])*256 + ord(s[7]),
                  'co2': ord(s[8])*256 + ord(s[9]),
                  'voc': ord(s[10]),
                  'temperature': ((ord(s[11])*256 + ord(s[12]))-435)*0.1,
                  'rh': ord(s[13])*256 + ord(s[14]),
                  'ch2o': (ord(s[15])*256 + ord(s[16]))*0.001,
                  'co': (ord(s[17])*256 + ord(s[18]))*0.1,
                  'o3': (ord(s[19])*256 + ord(s[20]))*0.01,
                  'no2': (ord(s[21])*256 + ord(s[22]))*0.01
                  }
        break
      else:
        if len(s) >= 9 and s[0] == 0xff and s[1] == 0x86:
          return {'pm1.0': s[2]*256 + s[3],
                  'pm2.5': s[4]*256 + s[5],
                  'pm10': s[6]*256 + s[7],
                  'co2': s[8]*256 + s[9],
                  'voc': s[10],
                  'temperature': ((s[11]*256 + s[12])-435)*0.1,
                  'rh': s[13]*256 + s[14],
                  'ch2o': (s[15]*256 + s[16])*0.001,
                  'co': (s[17]*256 + s[18])*0.1,
                  'o3': (s[19]*256 + s[20])*0.01,
                  'no2': (s[21]*256 + s[22])*0.01
                  }
        break
  except:
     traceback.print_exc()

  if not serial_console_untouched:
    start_getty()
  if result is not None:
    return result

def abc_on(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  ser = connect_serial()
  result=ser.write(b"\xff\x01\x79\xa0\x00\x00\x00\x00\xe6")
  ser.close()
  if not serial_console_untouched:
    start_getty()

def abc_off(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  ser = connect_serial()
  result=ser.write(b"\xff\x01\x79\x00\x00\x00\x00\x00\x86")
  ser.close()
  if not serial_console_untouched:
    start_getty()

def checksum(array):
  return struct.pack('B', 0xff - (sum(array) % 0x100) + 1)
