#!/usr/bin/python

import pygtk
import gtk
import cairo
import math

from math import pi
from math import cos
from math import sin

import arrow_head

class StandardArrowHead(arrow_head.ArrowHead):
    """
    Class is used to draw an arrow head onto a surface referenced by a GraphicsContext object. The properties must be defined or default values will be used and it inherits from the ArrowHead class.
    """

    def __init__(self):
        """ Constructor of ArrowHead and default values will be initialised. """
        super(StandardArrowHead, self).__init__()
        self._length = 10
        self._width = 0.4

    @property
    def length(self):
        """ Return the length. """
        return self._length

    @property
    def width(self):
        """ Return the width (in radians). """
        return self._width

    @length.setter
    def length(self, l):
        """ Set the length. """
        if l < 0:
            l *= -1
        self._length = l 

    @width.setter
    def width(self, w):
        """ Set the width (in radians). """
        if w < 0:
            w *= -1
        self._width = w

    def draw(self, ctx):
        """ Draw the arrow head onto the defined Graphics context ctx. """

        # trigonometric calculations of the arrow head for the two bottom corner points
        arrow_x0 = int(self._position[0] + cos(self._angle - pi - self._width / 2) * self._length)
        arrow_y0 = int(self._position[1] + sin(self._angle - pi - self._width / 2) * self._length)
        arrow_x1 = int(self._position[0] + cos(self._angle + pi + self._width / 2) * self._length)
        arrow_y1 = int(self._position[1] + sin(self._angle + pi + self._width / 2) * self._length)

        # define the properties of the arrow head to the GraphicsContext object
        ctx.set_source_rgb(*self._color)
        r = 0
        g = 0
        b = 0
        if self._color[0] != 0:
            r = 1
        if self._color[1] != 0:
            g = 1
        if self._color[2] != 0:
            b = 1
        ctx.set_source_rgba(r, g, b, 0.60)

        # draw arrow head
        ctx.move_to(arrow_x0, arrow_y0)
        ctx.line_to(*self._position)
        ctx.line_to(arrow_x1, arrow_y1)
        ctx.line_to(arrow_x0, arrow_y0)

        # finalize drawing
        ctx.close_path()
        ctx.fill_preserve()
        ctx.stroke()
