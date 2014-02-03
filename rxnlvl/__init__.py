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

from energy import energy
from level  import level
from edge   import edge
from baseline import baseline
from rxnlvl_util import validateColour, appendTextFile
import sys, os

class plot():
   # dimensions = [0,0]
   # bgcolour   = None
   # vbuf       = 10.0
   # hbuf       = 10.0
   # nodes      = []
   # edges      = []
   # qualified  = True

    def __init__(self, dimensions, bgcolour=None, vbuf=10.0, hbuf=10.0,
                 qualified=True):
        self.nodes = []
        self.edges = []
        self.bgcolour = None
        self.baseline = None
        try:
            assert len(dimensions) == 2, 'plot dimensions not equal to 2\n'
        except AssertionError as e:
            sys.stderr.write(str(e))
            sys.exit(1)
        try:
            for elem in dimensions:
                assert type(elem) in [int,float] and elem > 1,\
                'Malformed dimension element: {0}\n'.format(
                str(elem)
                )
        except AssertionError as e:
            sys.stderr.write(str(e))
            sys.exit(1)
        self.dimensions = dimensions
        if validateColour(bgcolour):
            self.bgcolour = bgcolour
        else:
            sys.stderr.write('INFO: Plot background colour is not set ' +
                             'or invalid - plot background will be ' +
                             'transparent\n'
                            )
        try:
            assert type(qualified) in [bool, str],\
            ('Could not interpret qualification ({0}) as '.format(qualified) +
             'boolean or string.\n'
            )
        except AssertionError as e:
            sys.stderr.write(str(e))
            sys.exit(1)
        self.qualified = qualified
        try:
            assert vbuf > 0 and hbuf > 0,\
            ('vertical and horizontal buffers must be ' +
             'positive rational numbers\n'
            )
        except AssertionError:
            sys.stderr.write(str(e))
            sys.exit(1)
        self.vbuf = float(vbuf)
        self.hbuf = float(hbuf)

    def __add__(self, object):
        choice = { 'edge':self.__add_edge, 'level':self.__add_node, 'baseline':self.__add_baseline}
        choice[object.__class__.__name__](object)

    def __add_node(self, node):
        self.nodes.append(node)

    def __add_edge(self, edge):
        self.edges.append(edge)

    def __add_baseline(self, baseline):
        self.baseline = baseline

    def getNamedNode(self, name):
        for node in self.nodes:
            if node.getName() == name:
                return(node)
        sys.stderr.write('a referenced node {0} could not be found\n'.format(
                        name
                        ))
        sys.exit()

    def deriveBufferedEnergyRange(self, bufsize):
        energyRange = [
                       min([ node.getEnergy() for node in self.nodes ]),
                       max([ node.getEnergy() for node in self.nodes ])
                      ]
        diff = energyRange[1]-energyRange[0]
        return([ energyRange[0]-(bufsize/100.0)*diff,
                 energyRange[1]+(bufsize/100.0)*diff ])

    def write(self):
        # Determine absolute path
        path = os.path.dirname(unicode(__file__,sys.getfilesystemencoding()))
        svgstring = ''
        # Write the preamble for the svg format
        svgstring += appendTextFile('{}/dat/svgprefix.frag'.format(str(path)))
        # Write dimensions of plot
        svgstring += ('<svg width="{0}cm" height="{1}cm" version="1.1" xmlns="http://www.w3.org/2000/svg">\n'.format(
                      self.dimensions[0], self.dimensions[1]
                     ))
        # If background is defined, draw it
        if self.bgcolour != None:
            svgstring += ('    <rect x="0%" y="0%" width="100%" height="100%" fill="#{0}"/>\n'.format(
                          str(hex(self.bgcolour))[2:]
                         ))
        # Calculate some geometry
        energyRange = self.deriveBufferedEnergyRange(self.vbuf)
        slices      = ((max([ node.getLocation() for \
                              node in self.nodes ]) -
                        min([ node.getLocation() for \
                              node in self.nodes ]))+1)*2-1
        sliceWidth  = (100.0-self.hbuf)/slices
        # Draw baseline if it has been defined
        if self.baseline != None:
            self.baseline.setVisualHeight(energyRange)
        svgstring += ('    <line x1="{0}%" x2="{1}%" y1="{2}%" y2="{2}%" stroke-linecap="round" stroke="#{3}" {4} stroke-opacity="{5}" stroke-width="1"/>\n'.format(
                          self.baseline.getVisualLeft(),
                          self.baseline.getVisualRight(),
                          self.baseline.getVisualHeight(),
                          # Courtesy of Tim Pietzcker
                          "{0:#0{1}x}".format(self.baseline.getColour(),8)[2:],
                          self.baseline.getMode(),
                          self.baseline.getOpacity()
                         ))
         # Iterate over nodes, setting visual sizes
        for node in self.nodes:
            node.setVisualLeft(sliceWidth, self.hbuf)
            node.setVisualRight(sliceWidth, self.hbuf)
            node.setVisualHeight(energyRange)
        # Iterate over edges, find the nodes that each edge
        # connects and draw edges between them
        for edge in self.edges:
            entry_node = self.getNamedNode(edge.getStart())
            exit_node  = self.getNamedNode(edge.getEnd())
            svgstring += ('    <line x1="{0}%" x2="{1}%" y1="{2}%" y2="{3}%" stroke="#{4}" {5} stroke-width="1" stroke-opacity="{6}" />\n'.format(
                          entry_node.getVisualRight(),
                          exit_node.getVisualLeft(),
                          entry_node.getVisualHeight(),
                          exit_node.getVisualHeight(),
                          "{0:#0{1}x}".format(edge.getColour(),8)[2:],
                          edge.getMode(),
                          edge.getOpacity()
                         ))
        # Draw energy levels as well as their annotations
        def qualify(node, qualified):
            qual_lut = {True:node.getQualifiedEnergy(), False:node.getUnqualifiedEnergy()}
            if qualified in qual_lut.keys():
                return(qual_lut[qualified])
            else:
                if node == self.nodes[0]:
                    return(node.getQualifiedEnergy())
                else:
                    return(node.getUnqualifiedEnergy())

        for node in self.nodes:
            svgstring += ('    <line x1="{0}%" x2="{1}%" y1="{2}%" y2="{2}%" stroke-linecap="round" stroke="#{3}" stroke-width="3"/>\n'.format(
                          node.getVisualLeft(),
                          node.getVisualRight(),
                          node.getVisualHeight(),
                          # Courtesy of Tim Pietzcker
                          "{0:#0{1}x}".format(node.getColour(),8)[2:]
                         ))
            svgstring += ('    <text x="{0}%" y="{1}%" dy="-1ex" font-family="sans-serif" text-anchor="middle" fill="#000000">{2}</text>\n'.format(
                          node.getVisualLeft()+sliceWidth/2,
                          node.getVisualHeight(),
                          node.getName()
                         ))
            svgstring += ('    <text x="{0}%" y="{1}%" dy="1ex" font-family="sans-serif" text-anchor="middle" font-size="8pt" fill="#000000">{2}</text>\n'.format(
                          node.getVisualLeft()+sliceWidth/2,
                          node.getVisualHeight()+4,
                          qualify(node,self.qualified)
                         ))
        svgstring += appendTextFile('{0}/dat/svgpostfix.frag'.format(str(path)))
        sys.stderr.write('Normal termination\n')
        sys.stdout.write(svgstring)
