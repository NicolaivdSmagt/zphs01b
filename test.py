#!/usr/bin/python3

import zphs01b

readout = zphs01b.read_all()

print(readout['temperature'])
