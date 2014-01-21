#! /usr/bin/python
# -*- coding: utf-8 -*-

#    rxnlvl 0.21
#    Copyright (C) 2014  Richard Terrett
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

def validateColour(colour):
    try:
        assert type(colour) == int and int(colour) < (16**6)
    except AssertionError as e:
        return(False)
    return(True)

def appendTextFile(file):
    buffer = ''
    try:
        lines = [ line for line in open(file,'r').readlines() ]
    except IOError as e:
        sys.stderr.write(e)
        sys.exit()
    for line in lines: buffer = buffer + line
    return(buffer)
