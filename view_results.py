#!/usr/bin/python

import pygtk
import gtk

import view

class ViewResults(view.View):
    """ The ViewResults class is a specific view that inherits from the general View class and is used to visualise the results window and contains a ControllerResults object. """

    def __init__(self):
        """ Constructor of ViewResults. """
        
        # call constructor of parent class
        view.View.__init__(self)
        
        # set title and size of the window
        self._window.set_title("Simulation: Results")
        self._window.resize(250, 250)
        # initialise the view
        self._initialise()

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewConfigurationPlace. """
        
        # call constructor of parent class
        view.View.__init__(self, model, controller)
        # set title and size of the window
        self._window.set_title("Simulation: Results")
        self._window.resize(250, 250)
        # initialise the view
        self._initialise()

    def _initialise(self):
        """ Initialise the GUI components. """

        # scrolled window
        self._scrolled_window = gtk.ScrolledWindow()
        self._scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        # textview
        self._textview = gtk.TextView()
        self._textview.set_editable(False)
        self._textview.set_left_margin(20)
        self._textview.set_right_margin(20)
        self._textbuffer = self._textview.get_buffer()
        # add textview to the scrolled window
        self._scrolled_window.add(self._textview)

    def show(self):
        """ Interface to create and display the GUI on the screen. """
        
        # call show method from the parent class
        view.View.show(self)
        
        # add scrolled window to the text view
        self._window.add(self._scrolled_window)
        # show components
        self._window.show_all()
        self._window.show()
        self.add("\n")

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

    def add(self, text):
        """ Add text to the textview. """
        self._textbuffer.insert(self._textbuffer.get_end_iter(), text + "\n")
        self._textview.forward_display_line_end(self._textbuffer.get_end_iter())

    def clear(self):
        """ Clear textview. """
        pass

if __name__ == "__main__":
    app = ViewResults()
    app.show()
    gtk.main()
    
