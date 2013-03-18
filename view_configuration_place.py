#!/usr/bin/python

import pygtk
import gtk

import view_configuration_component as view

class ViewConfigurationPlace(view.ViewConfigurationComponent):
    """ The ViewConfigurationPlace class is a specific view that inherits from the general ViewConfigurationComponent class and is used to visualise theconfiguration window for a places and contains a ControllerConfigurationPlace object. """

    __ent = None

    def __init__(self):
        """ Constructor of ViewConfigurationPlace. """
        
        # call constructor of parent class
        view.ViewConfigurationComponent.__init__(self)

        # set size and title of the window
        self._window.resize(150, 150)
        self._window.set_title("Configuration: Place")

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewConfigurationPlace. """
        
        # call constructor of parent class
        view.ViewConfigurationComponent.__init__(self, model, controller)

        # set size and title of the window
        self._window.resize(150, 150)
        self._window.set_title("Configuration: Place")

    def show(self):
        """ Interface to create and display the GUI on the screen. """

        # call show method from the parent class
        view.ViewConfigurationComponent.show(self)

        # create table
        self._table = gtk.Table(5, 2, True)

        # check if a controller is available
        if self._controller.component != None:
            # create widgets
            self.__ent = self._add_label_widget_pair(["Original Label:", "Label:", "Marking:", "Capacity:"], 
                                                    [self._controller.component.key, self._controller.component.label, 
                                                     self._controller.component.marking, 
                                                     str(self._controller.component.capacity)], 
                                                    [[0, 1, 0, 1], [0, 1, 1, 2], [0, 1, 2, 3], [0, 1, 3, 4]], 
                                                    [[1, 2, 0, 1], [1, 2, 1, 2], [1, 2, 2, 3], [1, 2, 3, 4]],
                                                    [self.I_NONE, self.I_ENTRY, self.I_ENTRY, self.I_ENTRY])
        else:
            # create widgets
            self.__ent = self._add_label_widget_pair(["Original Key:", "Label:", "Marking:", "Capacity:"], 
                                                   ["not defined", "", "0"], 
                                                   [[0, 1, 0, 1], [0, 1, 1, 2], [0, 1, 2, 3], [0, 1, 3, 4]], 
                                                   [[1, 2, 0, 1], [1, 2, 1, 2], [1, 2, 2, 3], [1, 2, 3, 4]],
                                                   [self.I_NONE, self.I_ENTRY, self.I_ENTRY, self.I_ENTRY])

        # create OK and Cancel button
        button_ok = gtk.Button("OK")
        button_ok.connect("clicked", self._on_ok_clicked)
        button_cancel = gtk.Button("Cancel")
        button_cancel.connect("clicked", self._on_cancel_clicked)

        # attach buttons to the table
        self._table.attach(button_ok, 0, 1, 4, 5)
        self._table.attach(button_cancel, 1, 2, 4, 5)

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
                if self._model.data.has_key(self.__ent[1].get_text()) or self._model.data.has_label(self.__ent[1].get_text()):
                    self.show_message_box_error("Label is already used! Please choose another label!")
                else:
                    # set properties
                    self._controller.key = str(self.__ent[1].get_text())
                    self._controller.label = str(self.__ent[1].get_text())
                    self._controller.marking = float(self.__ent[2].get_text())
                    self._controller.capacity = float(str(self.__ent[3].get_text()))
                    # update data
                    self._controller.update()
                    # close window
                    self._window.destroy()
            except ValueError:
                self.show_message_box_error("There are invalid entries!")

    def _on_cancel_clicked(self, button):
        """ Is called if the OK button sends the clicked event. """
        if self._controller != None:
            self._controller.cancel()
        self._window.destroy()

if __name__ == "__main__":
    app = ViewConfigurationPlace()
    app.show()
    gtk.main()
