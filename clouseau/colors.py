#! /usr/bin/ENV python
# -*- coding: utf-8 -*-

from output import *


symbols = {
  'ok': '✓',
  'er': '✖',
  'dot': '.'
}

print symbols

print green( symbols['ok'] )
print darkred( symbols['er'] )

print turquoise('Some turquoise text')
print red('Red')
print teal('Teal')
print blue('Blue')





