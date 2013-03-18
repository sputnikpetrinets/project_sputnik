#!/usr/bin/python

import pygtk
import gtk
import cairo

class Font(object):
    """ A simple class used to define the fonts within the framwork for the visualisation of the single components. """

    def __init__(self):
        """ Constructor of Font. """

        # set default values
        self._font = "Courier New"
        self._size = 11
        self._weight = cairo.FONT_SLANT_NORMAL
        self._slant = cairo.FONT_WEIGHT_NORMAL

    @property
    def font(self):
        """ Return font type. """
        return self._font

    @property
    def size(self):
        """ Return font size. """
        return self._size

    @property
    def weight(self):
        """ Return font weight. """
        return self._weight

    @property
    def slant(self):
        """ Return font slant. """
        return self._slant

    @font.setter
    def font(self, font):
        """ Set font type. """
        self._font = font

    @size.setter
    def size(self, size):
        """ Set font size. """
        self._size = size

    @weight.setter
    def weight(self, weight = cairo.FONT_WEIGHT_NORMAL):
        """ Set font weight. """
        self._weight = weight

    @slant.setter
    def slant(self, slant = cairo.FONT_SLANT_NORMAL):
        """ Set font slant. """
        self._slant = slant

    def clone(self):
        """ Duplicate the current font and return it. """

        # duplicate
        f = Font()
        # set properties
        f.font = self.font
        f.size = self.size
        f.weight = self.weight
        f.slant = self.slant
        # return duplicate
        return f
