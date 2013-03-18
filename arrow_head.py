#!/usr/bin/python

import pygtk
import gtk
import cairo

class ArrowHead(object):
    """
    Class is used to draw an arrow head onto a surface referenced by a GraphicsContext object. The properties must be defined or default values will be used.
    """

    def __init__(self):
        """ Constructor of ArrowHead and default values will be initialised. """
        super(ArrowHead, self).__init__()
        self._angle = 0
        self._color = [0.0, 0.0, 0.0]
        self._position = [0.0, 0.0]

    @property
    def angle(self):
        """ Return the angle between the components (in radians). """
        return self._angle
    
    @property
    def position(self):
        """ Return the position (x- and y-position). """
        return self._position

    @property
    def color(self):
        """ Return the colour (RGB-list). """
        return self._color

    @angle.setter
    def angle(self, a):
        """ Set the angle between the components (in radians). """
        self._angle = a

    @position.setter
    def position(self, pos):
        """ Set the position (x- and y-position). """
        self._position = pos

    @color.setter
    def color(self, c):
        """ Set the colour (RGB-list). """
        self._color = c

    def draw(self, ctx):
        """ Draw the arrow head onto the defined Graphics context ctx. """
        pass
