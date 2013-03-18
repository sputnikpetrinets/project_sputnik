#!/usr/bin/python

import model as m
import view_results
import controller as c

class ControllerResults(c.Controller):
    """ The ControllerResults class is a specific controller that inherits from the general Controller class and is used to manage the user interactions of the results window and the application (ViewResults). """

    def __init__(self):
        """ Constructor of ControllerResults. """

        # call constructor of parent class
        c.Controller.__init__(self)

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerResults. """

        # call constructor of parent class
        c.Controller.__init__(self, model, view)

    def add_text(self, text):
        """ Add a defined text to the locked entry box of the corresponding view. """
        if self._view != None:
            self._view.add(text)

    def clear(self):
        """ Clear the entry box of the corresponding view. """
        if self._view != None:
            self._view.clear()

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
