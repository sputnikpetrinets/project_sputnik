#!/usr/bin/python

import model as m
import view_layout as v
import controller as c

import spectral_a
import force_a

class ControllerLayout(c.Controller):
    """ The ControllerLayout class is a specific controller that inherits from the general Controller class and is used to manage the user interactions of the layouting configuration window and the application (ViewLayout). """

    _width = 900
    _height = 600
    _border = 85
    _displacement_radius = 85
    _iterations = 1
    _selected_components = None

    def __init__(self):
        """ Constructor of ControllerLayout. """

        # call constructor of parent class
        c.Controller.__init__(self)

        # set default values
        self._width = 900
        self._height = 600
        self._border = 85
        self._displacement_radius = 85
        self._iterations = 1
        self._selected_components = None

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerLayout. """

        # call constructor of parent class
        c.Controller.__init__(self, model, view)

        # set default values
        self._width = 900
        self._height = 600
        self._border = 85
        self._displacement_radius = 85
        self._iterations = 1
        self._selected_components = None

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """
        pass

    def update_component(self, key):
        """ Interface to notify Observer objects about a data change of a component. """
        pass

    def update_output(self):
        """ Interface to notify Observer objects about a data change of simulation results. """
        pass

    def reset(self):
        """ Interface to notify MVCObserver objects about a reset event. """
        pass

    def undo(self):
        """ Interface to notify Observer objects about an undo. """
        pass

    @property
    def width(self):
        """ Return width. """
        return self._width

    @property
    def height(self):
        """ Return height. """
        return self._height

    @property
    def border(self):
        """ Return border. """
        return self._border

    @property
    def displacement_radius(self):
        """ Return displacement radius. """
        return self._displacement_radius

    @property
    def iterations(self):
        """ Return iterations. """
        return self._iterations

    @property
    def selected_components(self):
        """ Return selected components. """
        return self._selected_components

    @width.setter
    def width(self, w):
        """ Set width. """
        self._width = w
        if self._width < 0:
            self._width *= -1

    @height.setter
    def height(self, h):
        """ Set height. """
        self._height = h
        if self._height < 0:
            self._height *= -1

    @border.setter
    def border(self, b):
        """ Set border. """
        self._border = b
        if self._border < 0:
            self._border *= -1

    @displacement_radius.setter
    def displacement_radius(self, s):
        """ Set displacement radius. """
        self._displacement_radius = s
        if self._displacement_radius < 0:
            self._displacement_radius *= -1

    @iterations.setter
    def iterations(self, i):
        """ Set iterations. """
        self._iterations = i
        if self._iterations < 0:
            self._iterations *= -1

    @selected_components.setter
    def selected_components(self, comps):
        """ Set selected components. """
        self._selected_components = comps

    def algorithm(self):
        """ Execute spectral algorithm for calculating the positions of the individual components. """

        # check if a model is defined
        if self._model != None:
            # create a snapshot
            self._model.create_snapshot()

        # instantiate an object which is using the spectral algorithm to calculate the positions for the components
        v = force_a.ForceDirected()
        # set data and properties
        v.petri_net = self._model.data.petri_net_data.clone()
        v.get_petri_net()
        v.width = self._width
        v.height = self._height
        v.border = self._border
        v.iterations = self._iterations
        # calculate positions
        v.calculate()
        # assign positions to components
        output = v.node_positions
        for key, value in output.items():
            component = self._model.data.get_component(key)
            # check if a component with the available key could be identified
            if component != None:
                component.position = value
                # update core data
                self._model.data.update(component, key)
        # notify observers
        self._model.notify()
