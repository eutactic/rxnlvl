rxnlvl
======

A simple python package for drawing attractive chemical reaction energy level diagrams.

![An energy level diagram](http://i.imgur.com/VMpnduy.png)

What do I need?
------
`rxnlvl` requires Python 2.x or later.

How do I work it?
------
You can import the `rxnlvl` module to draw plots. A parser for those not versed in Python is planned, but even if you don't know python you should still be able to easily create plots. Here's the script that generates part of the image you see above (I truncated it for brevity but you can make plots as long as you want):

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
    
    p +  edge(    '1',  'EC1', 0x0, 0.4, 'normal') 
    p +  edge(  'EC1', 'TS1a', 0x0, 0.2, 'normal') 
    p +  edge(  'EC1', 'TS1b', 0x0, 0.4, 'normal') 
    p +  edge( 'TS1a',  'DC1', 0x0, 0.2, 'normal') 
    p +  edge( 'TS1b',  'DC1', 0x0, 0.4, 'normal') 
    p +  edge(  'DC1',    '2', 0x0, 0.4, 'normal')
    
    
    p + baseline(energy( 0.0, 'kjmol'),colour=0x0,mode='dashed',opacity=0.1)
    
    p.write()


The boilerplate just tells Python where to find rxnlvl. Let's step through the rest:

###Plot creation:

    p = plot([25.0,10.0],vbuf=10.0,hbuf=5.0,bgcolour=None, qualified=False)
    
The plot takes the following arguments:
- `dimensions` - the width and height of the plot in cm.
- `vbuf` - the vertical margin as a percentage of the total height.
- `hbuf` - the horizontal margin as a percentage of the total height.
- `bgcolour` - the background colour of the image, as a 24-bit hexadecimal integer, or `None`. If `None`, the background will be transparent!
- `qualified` - if True, the units in which each energy are specified will be pretty-printed in the image. If False, will only print the numeric values. If set to *any* string value, will only print units on the leftmost energy level, which is useful if you want to give units in your plot but don't want to clutter it up.

Now we can start adding elements to the plot.

###Time to add some levels:

    p +  level(energy(   0.0, 'kjmol'),  1,    '1',      0x0)

Each level object takes the following arguments:
- `energy` - an `energy` object which represents the relative energy of the level. Each energy has 2 arguments - the energy as a floating point number, and the units, which can be `'kjmol'`, `'eh'` (Hartrees), `'ev'` (electronvolts), `'kcal'` (thermochemical kilocalories per mole) or `'wavenumber'`.
- `location` - the ordinal location of the level in the scheme. This must be a positive nonzero integer. Different levels can share the same location.
- `name` - the name of the level in the scheme. Levels should not share the same name.
- `colour` - A 24-bit hexadecimal integer representing the colour of the level.

###Time to join the levels with edges:

    p +  edge(    '1',  'EC1', 0x0, 0.4, 'normal')

Each edge object takes the folliwing arguments:
- `start` - The `name` of the level that the edge originates from.
- `end` - The `name` of the level that the edge terminates at. This must be different to `start`.
- `colour` - A 24-bit hexadecimal integer representing the colour of the edge.
- `opacity` - A float between 0.0 and 1.0 representing the opacity of the edge.
- `mode` - Choose either `'normal'` or `'dashed'`. Controls the appearance of the edge in terms of its dashed-linedness.

###Can we have a baseline ruled at 0.0 kJ/mol? Yes.

    p + baseline(energy( 0.0, 'kjmol'),colour=0x0,mode='dashed',opacity=0.1)

You can only have one baseline. The syntax should be fairly familiar:
- `energy` - an `energy` object which represents the relative energy of the baseline. Each energy has 2 arguments - the energy as a floating point number, and the units, which can be `'kjmol'`, `'eh'` (Hartrees), `'ev'` (electronvolts), `'kcal'` (thermochemical kilocalories per mole) or `'wavenumber'`.
- `colour` - A 24-bit hexadecimal integer representing the colour of the edge.
- `mode` - Choose either `'normal'` or `'dashed'`. Controls the appearance of the edge in terms of its dashed-linedness.
- `opacity` - A float between 0.0 and 1.0 representing the opacity of the edge.

###Okay let's plot this.

    p.write()

Will dump a `*.svg` file of your plot to `stdout`. Have fun!
