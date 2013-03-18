#!/usr/bin/python

import pygtk
import gtk

import view_configuration_simulation as view

class ViewConfigurationTokenGameAnimation(view.ViewConfigurationSimulation):
    """ The ViewConfigurationTokenGameAnimation class is a specific view that inherits from the general ViewConfigurationSimulation class and is used to visualise the configuration window for the token game animation and contains a ControllerConfigurationTokenGameAnimation object. """

    def __init__(self):
        """ Constructor of ViewConfigurationTokenGameAnimation. """
        
        # call constructor of parent class
        view.ViewConfigurationSimulation.__init__(self)

        # set algorithm an window size
        self._algorithm = self.A_GILLESPIE
        self._window.resize(150, 100)

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewConfigurationTokenGameAnimation. """
        
        # call constructor of parent class
        view.ViewConfigurationSimulation.__init__(self, model, controller)
        
        # set algorithm and window size
        self._algorithm = self.A_GILLESPIE
        self._window.resize(150, 100)

    def show(self):
        """ Interface to create and display the GUI on the screen. """

        # call show method from the parent class
        view.ViewConfigurationSimulation.show(self)

        # create table
        self._table = gtk.Table(3, 2, False)

        # create labels
        self._add_label("Number of Events:", [0, 1, 0, 1])
        self._add_label("Sleep Time:", [0, 1, 1, 2])

        # create entries
        self._ent_num_events = self._add_entry("50", [1, 2, 0, 1])
        self._ent_sleep_time = self._add_entry("1", [1, 2, 1, 2])

        # create OK and Cancel button
        button_ok = gtk.Button("OK")
        button_ok.connect("clicked", self._on_ok_clicked)
        button_cancel = gtk.Button("Cancel")
        button_cancel.connect("clicked", self._on_cancel_clicked)

        # attach buttons to the table
        self._table.attach(button_ok, 0, 1, 2, 3)
        self._table.attach(button_cancel, 1, 2, 2, 3)
        # attach table to the window
        self._window.add(self._table)
        # show all components
        self._window.show_all()
        self._window.show()

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

    def _on_ok_clicked(self, button):
        """ Is called if the OK button sends the clicked event. """

        # check if a controller is available
        if self._controller != None:
            try:
                # set properties
                self._controller.number_events = int(self._ent_num_events.get_text())
                self._controller.sleep_time = int(self._ent_sleep_time.get_text())
                # simulate petri net
                self._controller.simulate()
                # close window
                self._window.destroy()
            except ValueError:
                self.show_message_box_error("There are invalid entries!")

    def _on_cancel_clicked(self, button):
        """ Is called if the OK button sends the clicked event. """
        self._window.destroy()

    def _add_label(self, text, position):
        """ Add a label with a text to the table at the defined position and returns a reference. """
        # create label
        label = gtk.Label()
        label.set_markup(text)
        # attach label to the table
        self._table.attach(label, *position)
        # return reference
        return label

    def _add_entry(self, initial_value, position):
        """ Add an entry box with an initial value to the table at the defined position and returns a reference. """
        # create an entry box
        ent = gtk.Entry()
        ent.set_text(initial_value) 
        # attach entry box to the table
        self._table.attach(ent, *position)
        # return reference
        return ent

if __name__ == "__main__":
    app = ViewConfigurationSimulationMovie()
    app.show()
    gtk.main()
