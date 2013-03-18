#!/usr/bin/python
	
class Trajectory(object):
    """ The Trajectory class is used to define a single trajectory within a diagram. Different properties for this trajectory as well as the data for the x- and y-dimension can be set and all of these base on the matplotlib library. """

    _color = "#000000"
    _legend_text = ""
    _x_data = None
    _y_data = None
    _auto_color = False

    def __init__(self):
        """ Constructor of Trajectory and default values will be initialised. """
        self._color = "#000000"
        self._legend_text = ""
        self._x_data = None
        self._y_data = None
        self._auto_color = False

    @property
    def color(self):
        """ Return color. """
        return self._color

    @property
    def x_data(self):
        """ Return data in x-dimension. """
        return self._x_data

    @property
    def y_data(self):
        """ Return data in y-dimension. """
        return self._y_data

    @property
    def legend_text(self):
        """ Return legend text. """
        return self._legend_text

    @property
    def auto_color_allocation(self):
        """ Return flag for an automatic colour allocation. """
        return self._auto_color

    @color.setter
    def color(self, color):
        """ Set color. """
        self._color = color

    @x_data.setter
    def x_data(self, data):
        """ Set data in x-dimension. """
        self._x_data = data

    @y_data.setter
    def y_data(self, data):
        """ Set data in y-dimension. """
        self._y_data = data

    @legend_text.setter
    def legend_text(self, text):
        """ Set legend text. """
        self._legend_text = text

    @auto_color_allocation.setter
    def auto_color_allocation(self, status):
        """ Set flag for an automatic colour allocation. """
        self._auto_color = status
