#!/usr/bin/python

import gtk
import pygtk
import cairo

import mvc_observer

class View(mvc_observer.MVCObserver):
    """
    The View class is the parent class of the specific view observers which are part of the Model-View-Controller (MVC) Architecture and inherit from this class. This class inherits from the more general MVCObserver class and extend its functionalities. Views are implementing the Graphical User Interface (GUI) . Those observers can register with the model to receive notification events.
    """

    _controller = None
    _window = None

    def __init__(self):
        """ Constructor of View and default values will be initialised. """

        # call constructor of parent class
        super(View, self).__init__()

        # set general window properties
        self._window = gtk.Window()
        self._window.set_title("Stochastic Petri Net Simulation")
        self._window.resize(600, 600)
	self._window.set_position(gtk.WIN_POS_CENTER)
	self._window.connect("destroy", self.close)

    def __init__(self, model = None, controller = None):
        """ Constructor of View and values will be set. """

        # call constructor of parent class
        super(View, self).__init__(model)

        self._controller = controller
        # register controller
        if self._controller != None and self._model != None:
            self._model.add(self._controller)

        # set general window properties
        self._window = gtk.Window()
        self._window.set_title("Stochastic Petri Net Simulation")
        self._window.resize(600, 600)
	self._window.set_position(gtk.WIN_POS_CENTER)
	self._window.connect("destroy", self.close)

    @property
    def controller(self):
        """ Return controller (MVCObserver-Object). """
        return self._controller

    @controller.setter
    def controller(self, controller):
        """ Set controller (MVCObserver-Object). """
        self._controller = controller
        # register controller
        if self._controller != None and self._model != None:
            self._model.add(self._controller)

    def close(self, widget):
        """ Close the current view. """
        widget.destroy()

    def show(self):
        """ Interface to create and display the GUI on the screen. """
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

    def show_message_box_info(self, msg):
        """ Display an information message with the defined message msg on the screen. """
        msg_box = gtk.MessageDialog(self._window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                               gtk.BUTTONS_CLOSE, msg)
        msg_box.run()
        msg_box.destroy()
    
    def show_message_box_error(self, msg):
        """ Display an error message with the defined message msg on the screen. """
        msg_box = gtk.MessageDialog(self._window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
                               gtk.BUTTONS_CLOSE, msg)
        msg_box.run()
        msg_box.destroy()
    
    def show_message_box_question(self, msg):
        """ Display a question message with the defined message msg on the screen. """
        msg_box = gtk.MessageDialog(self._window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION, 
                               gtk.BUTTONS_CLOSE, msg)
        msg_box.run()
        msg_box.destroy()
    
    def show_message_box_warning(self, msg):
        """ Display a warning message with the defined message msg on the screen. """
        msg_box = gtk.MessageDialog(self._window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
                               gtk.BUTTONS_CLOSE, msg)
        msg_box.run()
        msg_box.destroy()
