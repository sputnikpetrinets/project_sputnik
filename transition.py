#!/usr/bin/python

import copy

import pygtk
import gtk
import cairo

import component
import font

class Transition(component.Component):
    """
    The Transition class is used to characterise a transition and it inherits from the general parent class Component. Via a defined GraphicsObject the transition can be drawn directly on the referenced surface.
    """

    def __init__(self):
        """ Constructor of Transition and default values will be initialised. """

        # call constructor of parent class
        super(Transition, self).__init__()
        
        self._dim = [0., 0.]
        self._rate = 1.
        self._font_rate = font.Font() #self._get_default_font()

    def __init__(self, position = [0., 0.], dimension = [0., 0.], edge = (0., 0., 0.), fill = (0., 0., 0.)):
        """ Constructor of Transition and default values will be initialised for the not defined parameter. """

        # call constructor of parent class
        super(Transition, self).__init__()

        self._pos = position
        self._dim = dimension
        self._edge = edge
        self._fill = fill
        self._label_pos = [self._pos[0] - self._dim[0], self._pos[1] - 3]
        self._rate = 1.
        self._font_rate = font.Font() #self._get_default_font()

    @property
    def rate(self):
        """ Return rate. """
        return self._rate

    @property
    def dimension(self):
        """ Return dimension (x- and y-dimension of the rectangle as list). """
        return self._dim

    @property
    def font_rate(self):
        """ Return the font of the rate (Font-Object). """
        self._font_rate

    @rate.setter
    def rate(self, r):
        """ Set rate. """
        self._rate = r
        if self._rate < 0:
            self._rate *= -1

    @dimension.setter
    def dimension(self, dim):
        """ Set dimension (x- and y-dimension of the rectangle as list). """
        for i in range(len(dim)):
            if dim[i] < 0:
                dim[i] = dim[i] * -1
        self._dim = dim

    @font_rate.setter
    def font_rate(self, font):
        """ Set the font of the rate (Font-Object). """
        self._font_rate = font

    def zoom(self, factor):
        """ Scale the component by a given factor. The text size will be kept as it is defined. """

        # check if the factor is negative and mu
        if factor < 0:
            # multiply by -1 because the factor is negative
            factor *= -1
        # rescale dimensions
        x_dim = int(self._dim[0] * factor)
        y_dim = int(self._dim[1] * factor)
        # check if the dimension in x-direction reached the lower limit to prevent a size zero
        if x_dim < 2:
            x_dim = 2
        # check if the dimension in y-direction reached the lower limit to prevent a size zero
        if y_dim < 4:
            y_dim = 4
        self._dim = [x_dim, y_dim]
        # rescale the positions
        self._pos = [int(self._pos[0] * factor), int(self._pos[1] * factor)]

    def draw(self, ctx):
        """ Draw the place onto the defined GraphicsContext ctx. """
        # set the general transition properties to draw the transition
        ctx.set_source_rgb(*self._edge)

        # draw the transition
        ctx.rectangle(self._pos[0] - int(self._dim[0] / 2), self._pos[1] - int(self._dim[1] / 2), self._dim[0], self._dim[1])

        # check if a colour to fill the rectangel is set
        if self._fill != None:
            # set the properties for filling the rectangle
            ctx.set_source_rgb(*self._fill)
            ctx.fill_preserve()

        # set text
        self._add_text(ctx, [self._pos[0], self._pos[1] + self._dim[1]], self._font_label, self._rate)
        self._add_text(ctx, [self._pos[0], self._pos[1] - self._dim[1]], self._font_label, self._label)
        ctx.stroke()
        ctx.save()

    def clone(self):
        """ Duplication of the current transition and the duplicate will be returned. """
        # duplicate
        comp = Transition()
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
        # transition specific properties
        comp.dimension = copy.deepcopy(self.dimension)
        comp.dimension = self.dimension
        comp.font_rate = self.font_rate
        # return duplicate
        return comp
