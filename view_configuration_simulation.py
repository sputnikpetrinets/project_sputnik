#!/usr/bin/python

import pygtk
import gtk

import view

class ViewConfigurationSimulation(view.View):
    """ The ViewConfigurationSimulation class is a specific view that inherits from the general View class and is used as a parent class to visualise the configuration window for the simulations and contains a ControllerConfigurationSimulation object. """

    A_GILLESPIE = 0
    A_TAULEAP = 1

    _algorithm = None

    def __init__(self):
        """ Constructor of ViewConfigurationSimulation. """
        
        # call constructor of parent class
        view.View.__init__(self)

        # set title
        self._window.set_title("Configuration: Simulation")

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewConfigurationSimulation. """
        
        # call constructor of parent class
        view.View.__init__(self, model, controller)

        # set title
        self._window.set_title("Configuration: Simulation")

    def show(self):
        """ Interface to create and display the GUI on the screen. """
        pass

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """
        pass

    def update_component(self, key):
        """ Interface to notify Observer objects about a data change of a component. """
        pass

    def update_output(self):
        """ Interface to notify Observer objects about a data change of simulation results. """
        pass

    def undo(self):
        """ Interface to notify Observer objects about an undo. """
        pass

if __name__ == "__main__":
    app = ViewConfigurationSimulation()
    app.show()
    gtk.main()
