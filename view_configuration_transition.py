#!/usr/bin/python

import pygtk
import gtk

import view_configuration_component as view

class ViewConfigurationTransition(view.ViewConfigurationComponent):
    """ The ViewConfigurationTransition class is a specific view that inherits from the general ViewConfigurationComponent class and is used to visualise the configuration window for a transitions and contains a ControllerConfigurationTransition object. """

    __ent = None

    def __init__(self):
        """ Constructor of ViewConfigurationTransition. """
        
        # call constructor of parent class
        view.ViewConfigurationComponent.__init__(self)
        
        # set size and title of the window
        self._window.resize(150, 150)
        self._window.set_title("Configuration: Transition")

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewConfigurationTransition. """
        
        # call constructor of parent class
        view.ViewConfigurationComponent.__init__(self, model, controller)
        
        # set size and title of the window
        self._window.resize(150, 150)
        self._window.set_title("Configuration: Transition")

    def show(self):
        """ Interface to create and display the GUI on the screen. """
        
        # call show method from the parent class
        view.ViewConfigurationComponent.show(self)

        # create table
        self._table = gtk.Table(4, 2, True)

        # check if a controller is available
        if self._controller.component != None:
            # create widgets
            self.__ent = self._add_label_widget_pair(["Original Label:", "Label:", "Rate:"], 
                                                    [self._controller.component.key, 
                                                     self._controller.component.label, 
                                                     str(self._controller.component.rate)], 
                                                    [[0, 1, 0, 1], [0, 1, 1, 2], [0, 1, 2, 3]], 
                                                    [[1, 2, 0, 1], [1, 2, 1, 2], [1, 2, 2, 3]],
                                                    [self.I_NONE, self.I_ENTRY, self.I_ENTRY])
        else:
            # create widgets
            self.__ent = self._add_label_widget_pair(["Original Key:", "Label:", "Rate:"], 
                                                   ["not defined", "", "0.0"], 
                                                   [[0, 1, 0, 1], [0, 1, 1, 2], [0, 1, 2, 3], [0, 1, 3, 4]], 
                                                   [[1, 2, 0, 1], [1, 2, 1, 2], [1, 2, 2, 3], [1, 2, 3, 4]],
                                                   [self.I_NONE, self.I_ENTRY, self.I_ENTRY])

        # create OK and Cancel button
        button_ok = gtk.Button("OK")
        button_ok.connect("clicked", self._on_ok_clicked)
        button_cancel = gtk.Button("Cancel")
        button_cancel.connect("clicked", self._on_cancel_clicked)

        # attach buttons to the table
        self._table.attach(button_ok, 0, 1, 3, 4)
        self._table.attach(button_cancel, 1, 2, 3, 4)

        # attach table to the window
        self._window.add(self._table)
        # show all components
        self._window.show_all()
        self._window.show()

    def _on_ok_clicked(self, button):
        """ Is called if the OK button sends the clicked event. """
        
        # check if a controller is available
        if self._controller != None:
            try:
                if self._model.data.has_key(self.__ent[1].get_text()) or self._model.data.has_label(self.__ent[1].get_text()):
                    self.show_message_box_error("Label is already used! Please choose another label!")
                else:
                    # set properties
                    self._controller.key = self.__ent[1].get_text()
                    self._controller.label = self.__ent[1].get_text()
                    self._controller.rate = float(self.__ent[2].get_text())
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
    app = ViewConfigurationTransition()
    app.show()
    gtk.main()
