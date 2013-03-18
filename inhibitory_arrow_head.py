#!/usr/bin/python

import pygtk
import gtk
import cairo
import math

from math import pi
from math import cos
from math import sin

import arrow_head

class InhibitoryArrowHead(arrow_head.ArrowHead):
    """
    Class is used to draw an inhibitory arrow head onto a surface referenced by a GraphicsContext object. The properties must be defined or default values will be used and it inherits from the ArrowHead class.
    """

    def __init__(self):
        """ Constructor of InhibitoryArrowHead and default values will be initialised. """
        super(InhibitoryArrowHead, self).__init__()
        self._radius = 3

    @property
    def radius(self):
        """ Return the radius. """
        return self._radius

    @radius.setter
    def radius(self, r):
        """ Set the radius. """
        self._radius = r
        if self._radius < 0:
            self._radius *= -1

    def draw(self, ctx):
        """ Draw the arrow head onto the defined Graphics context ctx. """

        # trigonometric calculations to find the position at the circle
        dx = self._radius * cos(self._angle)
        dy = self._radius * sin(self._angle)

        circle_position = [self._position[0], self._position[1]]

        # set properties for the GraphicsObject
        ctx.move_to(*circle_position)
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
        ctx.stroke()
        
        # draw arrow head
        ctx.arc(circle_position[0], circle_position[1], self._radius, 0., 2. * pi)
        ctx.stroke()
