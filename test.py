#! /usr/bin/python

# Boilerplate
import sys
sys.path.insert(1,"/home/user/bin/rxnlvl/") # Change this to the full path of rxnlvl
from rxnlvl import *

# Plot
p = plot([25.0,10.0],vbuf=10.0,hbuf=5.0,bgcolour=None, qualified=False)

p +  level(energy(   0.0, 'kjmol'),  1,    '1',      0x0) 
p +  level(energy(  -8.5, 'kjmol'),  2,  'EC1',      0x0)
p +  level(energy(  24.4, 'kjmol'),  3, 'TS1a', 0xFF4444)
p +  level(energy(   5.1, 'kjmol'),  3, 'TS1b',      0x0)
p +  level(energy( -10.2, 'kjmol'),  4,  'DC1',      0x0)
p +  level(energy(  -8.2, 'kjmol'),  5,    '2',      0x0)
p +  level(energy( -11.1, 'kjmol'),  6,  'EC2',      0x0)
p +  level(energy(  -8.3, 'kjmol'),  7, 'TS2b',      0x0)
p +  level(energy(   1.8, 'kjmol'),  7, 'TS2a', 0x44FF44)
p +  level(energy( -10.3, 'kjmol'),  8,  'DC2',      0x0)
p +  level(energy(   8.5, 'kjmol'),  9,    '3',      0x0)
p +  level(energy(  18.5, 'kjmol'), 10,    '4',      0x0)
p +  level(energy(   2.5, 'kjmol'), 11,    '5',      0x0)

p +  edge(    '1',  'EC1', 0x0, 0.4, 'normal') 
p +  edge(  'EC1', 'TS1a', 0x0, 0.2, 'normal') 
p +  edge(  'EC1', 'TS1b', 0x0, 0.4, 'normal') 
p +  edge( 'TS1a',  'DC1', 0x0, 0.2, 'normal') 
p +  edge( 'TS1b',  'DC1', 0x0, 0.4, 'normal') 
p +  edge(  'DC1',    '2', 0x0, 0.4, 'normal')
p +  edge(    '2',  'EC2', 0x0, 0.4, 'normal')
p +  edge(  'EC2', 'TS2b', 0x0, 0.4, 'normal')
p +  edge(  'EC2', 'TS2a', 0x0, 0.2, 'normal')
p +  edge( 'TS2a',  'DC2', 0x0, 0.2, 'normal')
p +  edge( 'TS2b',  'DC2', 0x0, 0.4, 'normal')
p +  edge(  'DC2',    '3', 0x0, 0.4, 'normal')
p +  edge(    '3',    '4', 0x0, 0.4, 'normal')
p +  edge(    '4',    '5', 0x0, 0.4, 'normal')


p + baseline(energy( 0.0, 'kjmol'),colour=0x0,mode='dashed',opacity=0.1)

p.write()
