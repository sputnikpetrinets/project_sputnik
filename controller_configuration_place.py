#!/usr/bin/python

import model as m
import view_configuration_place as v
import controller_configuration_component as c

import place

class ControllerConfigurationPlace(c.ControllerConfigurationComponent):
    """ The ControllerConfigurationPlace class is a specific controller that inherits from the general ControllerConfigurationComponent class and is used to manage the user interactions of the configuration window for places and the application (ViewConfigurationPlace). """

    _marking = 0
    _capacity = 0

    def __init__(self):
        """ Constructor of ControllerConfigurationPlace. """
        
        # call constructor of parent class
        c.ControllerConfigurationComponent.__init__(self)

        # set default values
        self._marking = 0
        self._capacity = 0

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerConfigurationPlace. """
        
        # call constructor of parent class
        c.ControllerConfigurationComponent.__init__(self, model, view)

        # set default values
        self._marking = 0
        self._capacity = 0

    @property
    def marking(self):
        """ Return marking. """
        return self._marking

    @property
    def capacity(self):
        """ Return capacity. """
        return self._capacity

    @marking.setter
    def marking(self, m):
        """ Set marking. """
        self._marking = m
        if self._marking < 0:
            self._marking *= -1

    @capacity.setter
    def capacity(self, c):
        """ Set capacity. """
        self._capacity = c
        if self._capacity < 0:
            self._capacity *= -1

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """
        
        # call update method of parent class
        c.ControllerConfigurationComponent.update(self)
        
        # check if a new component well be added
        if self.is_new_component():
            # set properties
            self._component.label = self._label
            self._component.key = self._key
            self._component.marking = float(self._marking)
            self._component.capacity = float(self._capacity)
            if self._model != None:
                # add place to core data
                self._model.data.add_place(self._component)
                # remove buffer component
                self._model.data.remove_place_key("new component")
                # notify all observers
                self._model.notify_component(self._key)
        else:
            # set properties
            self._component.label = self._label
            self._component.key = self._key
            self._component.marking = float(self._marking)
            self._component.capacity = float(self._capacity)
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
        self._model.data.remove_place_key("new component")
        # notify all observers
        self._model.notify_component(self._key)
