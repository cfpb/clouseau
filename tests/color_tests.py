#! /usr/bin/env python
# -*- coding: utf-8 -*-

from clouseau.clients import colors




print dir( colors )

for c in colors.codes:
    print colors.color( c, c )


print colors.ok()
print colors.fail()

print colors.ok( 'OK with text' )
print colors.fail( 'Fail with text' )


print ('-------------------')

print colors.gray('Gray Text')






