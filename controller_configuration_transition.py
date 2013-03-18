#!/usr/bin/python

import model as m
import view_configuration_transition as v
import controller_configuration_component as c

import transition

class ControllerConfigurationTransition(c.ControllerConfigurationComponent):
    """ The ControllerConfigurationTransition class is a specific controller that inherits from the general ControllerConfigurationComponent class and is used to manage the user interactions of the configuration window for transitions and the application (ViewConfigurationTransition). """

    _rate = 0

    def __init__(self):
        """ Constructor of ControllerConfigurationTransition. """
        
        # call constructor of parent class
        c.ControllerConfigurationComponent.__init__(self)

        # set default values
        self._rate = 0

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerConfigurationTransition. """
        
        # call constructor of parent class
        c.ControllerConfigurationComponent.__init__(self, model, view)

        # set default values
        self._rate = 0

    @property
    def rate(self):
        """ Return rate. """
        return self._rate

    @rate.setter
    def rate(self, m):
        """ Set rate. """
        self._rate = float(m)
        if self._rate < 0:
            self._rate *= -1

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """

        # call update method of parent class
        c.ControllerConfigurationComponent.update(self)
        # check if a new component well be added
        if self.is_new_component():
            # set properties
            self._component.label = self._label
            self._component.key = self._key
            self._component.rate = float(self._rate)
            if self._model != None:
                # add transition to core data
                self._model.data.add_transition(self._component)
                # remove buffer component
                self._model.data.remove_transition_key("new component")
                # notify all observers
                self._model.notify_component(self._key)
        else:
            self._component.label = self._label
            self._component.key = self._key
            self._component.rate = float(self._rate)
            if self._model != None:
                # update core data
                self._model.data.update(self._component, self._key)
                # notify all observers
                self._model.notify_component(self._key)

        # update the matrices
        self.update_data()

    def cancel(self):
        """ Cancel current view. """
        # remove buffer component
        self._model.data.remove_key("new component")
        # notify all observers
        self._model.notify_component(self._key)
