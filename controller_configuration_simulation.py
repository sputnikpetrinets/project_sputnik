#!/usr/bin/python

import model as m
import controller as c

class ControllerConfigurationSimulation(c.Controller):
    """ The ControllerConfigurationSimulation class is a specific controller that inherits from the general Controller class and is used as a parent class to manage the user interactions of the simulation configuration window and the application (ViewConfigurationSimulation). """

    def __init__(self):
        """ Constructor of ControllerConfigurationSimulation. """
        
        # call constructor of parent class
        c.Controller.__init__(self)

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerConfigurationSimulation. """
        
        # call constructor of parent class
        c.Controller.__init__(self, model, view)

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
    def algorithm(self):
        """ Return algorithm. """
        return self._algorithm

    @algorithm.setter
    def algorithm(self, alg):
        """ Set algorithm. """
        self._algorithm = alg

    def gillespie_algorithm(self):
        """ Execute Gillespie algorithm. """
        pass

    def tauleap_algorithm(self):
        """ Execute Tau Leap algorithm. """
        pass
