#!/usr/bin/python

import model as m
import view_configuration_component as v
import controller as c

class ControllerConfigurationComponent(c.Controller):
    """ The ControllerConfigurationComponent class is a specific controller that inherits from the general Controller class and is used as a parent class to manage the user interactions of the configuration window and the application (ViewConfigurationComponent). """

    _component = None
    _label = ""
    _key = ""
    _add_component = False

    def __init__(self):
        """ Constructor of ControllerConfigurationComponent. """
        
        # call constructor of parent class
        c.Controller.__init__(self)
        
        # set default values
        self._component = None
        self._label = ""
        self._key = ""
        self._add_component = False

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerConfigurationComponent. """
        
        # call constructor of parent class
        c.Controller.__init__(self, model, view)
        
        # set default values
        self._component = None
        self._label = ""
        self._key = ""
        self._add_component = False

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """
        self._model.create_snapshot()

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
    def component(self):
        """ Return component (Component-Object). """
        return self._component

    @property
    def label(self):
        """ Return label. """
        return self._label

    @property
    def key(self):
        """ Return key. """
        return self._key

    @component.setter
    def component(self, comp):
        """ Set component (Component-Object). """
        if comp.key == "new_component" or comp.key == "new component" or comp.key == "new_comp":
            self._add_component = True
        self._component = comp

    @label.setter
    def label(self, label):
        """ Set label. """
        self._label = label

    @key.setter
    def key(self, key):
        """ Set key. """
        self._key = key

    def is_new_component(self):
        """ Check if the setted component is a new one. If so, TRUE will be returned. """
        return self._add_component

    def update_data(self):
        """ Automatically creates the new matrices describing the current petri net. """
        self._model.data.convert_matrices()
