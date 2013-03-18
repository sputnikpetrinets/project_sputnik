#!/usr/bin/python

import copy

import pygtk
import gtk
import cairo

import component
import font

from math import pi

class Place(component.Component):
    """
    The Place class is used to characterise a place and it inherits from the general parent class Component. Via a defined GraphicsObject the place can be drawn directly on the referenced surface.
    """

    def __init__(self):
        """ Constructor of Place and default values will be initialised. """

        # call constructor of parent class
        super(Place, self).__init__()
        
        self._radius = 0.
        self._marking = 0
        self._step_size = 1
        self._capacity = 0
        self._font_marking = font.Font() #self._get_default_font()

    def __init__(self, position = [0., 0.], radius = 0., edge = (0., 0., 0.), fill = (255., 255., 255.)):
        """ Constructor of Place and default values will be initialised for the not defined parameter. """

        # call constructor of parent class
        super(Place, self).__init__()

        self._pos = position
        self._radius = radius
        self._edge = edge
        self._fill = fill
        self._marking = 0
        self._step_size = 1
        self._capacity = 0
        self._font_marking = font.Font() #self._get_default_font()

    @property
    def radius(self):
        """ Return radius. """
        return self._radius

    @property
    def marking(self):
        """ Return marking. """
        return self._marking
    
    @property
    def step(self):
        """ Return step size. """
        return self._step_size

    @property
    def capacity(self):
        """ Return capacity. """
        return self._capacity

    @property
    def font_marking(self):
        """ Return the font of the marking (Font-Object). """
        return self._font_marking

    @radius.setter
    def radius(self, r):
        """ Set radius. """
        self._radius = r
        if self._radius < 0:
            self._radius *= -1

    @marking.setter
    def marking(self, m):
        """ Set marking. """
        self._marking = m
        if self._marking < 0:
            self._marking *= -1
        if self._marking > self._capacity and self._capacity > 0:
            self._marking = self._capacity

    @step.setter
    def step(self, s):
        """ Set step size. """
        self._step = s
        if self._step < 0:
            self._step *= -1

    @capacity.setter
    def capacity(self, c):
        """ Set capacity. """
        self._capacity = c
        if self._capacity < 0:
            self._capacity *= -1

    @font_marking.setter
    def font_marking(self, font):
        """ Set font for marking (Font-Object). """
        self._font_marking = font

    def increase_marking_steps(self, s):
        """ Increase the marking by the defined step size. """
        for i in range(int(s)):
            self._marking += self._step_size
        if self._marking > self._capacity and self._capacity > 0:
            self._marking = self._capacity

    def decrease_marking_steps(self, s):
        """ Decrease the marking by the defined step size. """
        for i in range(int(s)):
            self._marking -= self._step_size
        if self._marking < 0:
            self._marking = 0

    def increase_marking(self, c):
        """ Increase the marking by the defined value c. """
        self._marking += c
        if self._marking > self._capacity and self._capacity > 0:
            self._marking = self._capacity

    def decrease_marking(self, c):
        """ Decrease the marking by the defined value c. """
        self._marking -= c
        if self._marking < 0:
            self._marking = 0

    def zoom(self, factor):
        """ Scale the component by a given factor. The text size will be kept as it is defined. """

        # check if the factor is negative
        if factor < 0:
            # multiply by -1 because the factor is negative
            factor *= -1
        # rescale the radius
        self._radius = int(self._radius * factor)
        # check if the radius reached the lower limit to prevent a size zero
        if self._radius < 2:
            self._radius = 2
        # rescale the positions
        self._pos = [int(self._pos[0] * factor), int(self._pos[1] * factor)]

    def draw(self, ctx):
        """ Draw the place onto the defined GraphicsContext ctx. """

        # check if a colour to fill the place is set
        if self._fill != None:
            # set the properties for filling the place
            ctx.set_source_rgb(*self._fill)
            ctx.fill_preserve()
        # set the general place properties to draw the place
        ctx.set_source_rgb(*self._edge)

        # draw the place
        ctx.arc(self._pos[0] + self.x_offset, self._pos[1] + self.y_offset, self._radius, 0., 2. * pi)
        self._add_text(ctx, [self._pos[0] + self.x_offset, self._pos[1] + self.y_offset], self._font_marking, int(self._marking))
        self._add_text(ctx, [self._pos[0] + self.x_offset, self._pos[1] + self.y_offset - self._radius - 10], 
                       self._font_label, self._label)
        ctx.stroke()
        ctx.save()

    def clone(self):
        """ Duplication of the current place and the duplicate will be returned. """
        # duplicate
        comp = Place()
        # general component properties
        comp.key = self.key
        comp.label = self.label
        comp.description = self.description
        comp.x_offset = self.x_offset
        comp.y_offset = self.y_offset
        comp.font_label = self.font_label.clone()
        comp.font_description = self.font_description.clone()
        comp.position = copy.deepcopy(self.position)
        comp.rgb_edge = copy.deepcopy(self.rgb_edge)
        comp.rgb_fill = copy.deepcopy(self.rgb_fill)
        comp.count_inputs = self.count_inputs
        comp.count_outputs = self.count_outputs   
        # place specific properties
        comp.radius = self.radius
        comp.marking = self.marking
        comp.capacity = self.capacity
        comp.step = self.step
        comp.font_marking = self.font_marking
        # return duplicate
        return comp
