#!/usr/bin/python

import model as m
import view_configuration_token_game_animation as v
import controller_configuration_simulation
import controller as c

import gillespie

class ControllerConfigurationTokenGameAnimation(controller_configuration_simulation.ControllerConfigurationSimulation):
    """ The ControllerConfigurationTokenGameAnimation class is a specific controller that inherits from the general ControllerConfigurationSimulation class and is used to manage the user interactions of the simulation configuration window and the application (ViewConfigurationConfigurationTokenGameAnimation). """

    _num = 0
    _sleep = 1

    def __init__(self):
        """ Constructor of ControllerConfigurationTokenGameAnimation. """
        
        # call constructor of parent class
        controller_configuration_simulation.ControllerConfigurationSimulation.__init__(self)

        # set default values
        self._num = 0
        self._sleep = 1

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerConfigurationTokenGameAnimation. """
        
        # call constructor of parent class
        controller_configuration_simulation.ControllerConfigurationSimulation.__init__(self, model, view)

    @property
    def number_events(self):
        """ Return number of events. """
        return self._num

    @property
    def sleep_time(self):
        """ Return sleep time between the events. """
        return self._sleep

    @number_events.setter
    def number_events(self, num):
        """ Set number of events. """
        self._num = num
        if self._num < 0:
            self._num *= -1

    @sleep_time.setter
    def sleep_time(self, t):
        """ Set sleep time between the events. """
        self._sleep = int(t)
        if self._sleep < 0:
            self._sleep *= -1

    def simulate(self):
        """ Execute the simulation that generates the firing events. """

        # instantiate an object used to simulate the petri net via a gillespie algorithm
        g = gillespie.Gillespie()
        # set properties
        g.petri_net = self._model.data.petri_net_data
        g.num_iterations = self._num
        # run simulation
        g.run_simulation()

        # set data
        self._model.output = g.simulation_data
        self._model.output_args = [self._sleep, self._num]
        # notify observers
        self._model.notify_output()
