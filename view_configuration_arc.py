#!/usr/bin/python

import pygtk
import gtk

import view_configuration_component as view

class ViewConfigurationArc(view.ViewConfigurationComponent):
    """ The ViewConfigurationArc class is a specific view that inherits from the general ViewConfigurationComponent class and is used to visualise the configuration window for a arcs and contains a ControllerConfigurationArc object. """

    _ent = None
    _arc_type = None

    def __init__(self):
        """ Constructor of ViewConfigurationArc. """
        
        # call constructor of parent class
        view.ViewConfigurationComponent.__init__(self)

        # set size and title of the window
        self._window.resize(150, 150)
        self._window.set_title("Configuration: Arc")

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewConfigurationArc. """
        
        # call constructor of parent class
        view.ViewConfigurationComponent.__init__(self, model, controller)

        # set size and title of the window
        self._window.resize(150, 150)
        self._window.set_title("Configuration: Arc")

    def show(self):
        """ Interface to create and display the GUI on the screen. """

        # call show method from the parent class
        view.ViewConfigurationComponent.show(self)

        # create table
        self._table = gtk.Table(8, 2, True)

        # add a label to the table
        label = gtk.Label()
        label.set_markup("Available Arcs:")
        self._table.attach(label, 0, 1, 0, 1)

        # check if a model is defined
        if self._model != None:
            # create the gtk.ListStore that contains the available arcs connecting two components
            a_store_list = gtk.ListStore(str, str)
            # check if a controller is available
            if self._controller != None:
                # check if any arcs are available which need to be added to the list
                if self._controller.selected_components == None:
                    # add all arcs to the list
                    for key, item in self._model.data.arcs.items():
                        if item != None and key != "new_comp":
                            a_store_list.append([key, item.label])
                else:
                    # add delete button to the table
                    button_delete = gtk.Button("Delete")
                    button_delete.connect("clicked", self._on_delete_clicked)
                    self._table = gtk.Table(8, 2, True)
                    self._table.attach(button_delete, 2, 3, 0, 1)
                    # add selected arcs to the list
                    for i in range(len(self._controller.selected_components)):
                        if self._controller.selected_components[i] != None and self._controller.selected_components[i].key != "new_comp":
                            a_store_list.append([self._controller.selected_components[i].key, self._controller.selected_components[i].label])

            # create a combobox containing the selected or all arcs
            a_combo_box = gtk.ComboBox(a_store_list)
            a_combo_box.connect("changed", self._on_combo_box_changed)
            renderer = gtk.CellRendererText()
            a_combo_box.pack_start(renderer, True)
            a_combo_box.add_attribute(renderer, "text", 0)
            # version conflict - only in 2.24+ available!!!
            #a_combo_box.set_entry_text_column(1)
            # attach combobox to the table
            self._table.attach(a_combo_box, 1, 2, 0, 1)
        else:
            # label that no selection
            label = gtk.Label()
            label.set_markup("No Selection Available")
            self._table.attach(label, 1, 2, 0, 1)

        # add general widgets to the table
        self._ent = self._add_label_widget_pair(["Original Label", "Label:", "Weight:"], 
                                               ["not defined", "", "0"], 
                                               [[0, 1, 1, 2], [0, 1, 2, 3], [0, 1, 3, 4]], 
                                               [[1, 2, 1, 2], [1, 2, 2, 3], [1, 2, 3, 4]],
                                               [self.I_NONE, self.I_ENTRY, self.I_ENTRY])

        # create line-type label
        label_line = gtk.Label()
        label_line.set_markup("Line Type:")

        # create the selection for the line type
        self._radio_button_straight = gtk.RadioButton(None, "Straight Line")
        self._radio_button_straight.connect("toggled", self._on_change_radio_button_line, "straight")

        self._radio_button_curved_lower = gtk.RadioButton(self._radio_button_straight, "Curved Line - Lower")
        self._radio_button_curved_lower.connect("toggled", self._on_change_radio_button_line, "curved_lower")

        self._radio_button_curved_upper = gtk.RadioButton(self._radio_button_straight, "Curved Line - Upper")
        self._radio_button_curved_upper.connect("toggled", self._on_change_radio_button_line, "curved_upper")

        # create a checkbox which can be checked if the line type needs to be determined automatically
        self._auto_line_type = gtk.CheckButton("Automatic Line-Type Allocation")
        self._auto_line_type.set_active(True)
        self._auto_line_type.connect("toggled", self._on_change_checkbutton, "auto_line_type")
        self._table.attach(self._auto_line_type, 1, 2, 5, 6)

        # create OK and Cancel button
        button_ok = gtk.Button("OK")
        button_ok.connect("clicked", self._on_ok_clicked)
        button_cancel = gtk.Button("Cancel")
        button_cancel.connect("clicked", self._on_cancel_clicked)

        # attach widgets to the table
        self._table.attach(label_line, 0, 1, 5, 6)
        self._table.attach(self._radio_button_straight, 1, 2, 6, 7)
        self._table.attach(self._radio_button_curved_lower, 1, 2, 7, 8)
        self._table.attach(self._radio_button_curved_upper, 1, 2, 8, 9)
        self._table.attach(button_ok, 0, 1, 9, 10)
        self._table.attach(button_cancel, 1, 2, 9, 10)

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
                if self._model.data.has_key(self._ent[1].get_text()) or self._model.data.has_label(self._ent[1].get_text()):
                    self.show_message_box_error("Label is already used! Please choose another label!")
                else:
                    # set properties
                    self._controller.key = self._ent[1].get_text()
                    self._controller.label = self._ent[1].get_text()
                    self._controller.weight = float(self._ent[2].get_text())
                    # update data
                    self._controller.update()
                    # close window
                    self._window.destroy()
            except ValueError:
                self.show_message_box_error("There are invalid entries!")

    def _on_cancel_clicked(self, button):
        """ Is called if the Cancel button sends the clicked event. """
        if self._controller != None:
            self._controller.cancel()
        self._window.destroy()

    def _on_delete_clicked(self, button):
        """ Is called if the delete button sends the clicked event. """

        # check if a controller is available
        if self._controller != None:
            # delete selected arc
            if self._controller.delete():
                self.show_message_box_info("Arc could be removed!")
            else:
                self.show_message_box_error("Arc could not be removed!")

    def _on_change_radio_button_line(self, widget, data = None):
        """ Is called if the status of a radio button changes. """

        # check if a controller is available
        if self._controller != None:
            # set the correct line type
            if widget.get_active() and data.lower() == "straight":
                self._controller.arc_line_type = self._controller.LT_STRAIGHT
            if widget.get_active() and data.lower() == "curved_lower":
                self._controller.arc_line_type = self._controller.LT_CURVED_LOWER
            if widget.get_active() and data.lower() == "curved_upper":
                self._controller.arc_line_type = self._controller.LT_CURVED_UPPER
                    
    def _on_combo_box_changed(self, widget, data = None):
        """ Is called if the selection of the combobox changes. """

        # check if a model and controller is available
        if self._model != None and self._controller != None:
            # check if no selection of arcs is available
            if self._controller.selected_components == None:
                # iteration through all arcs
                for key, item in self._model.data.arcs.items():
                    if item != None:
                        # check if the current arc is the same as the selected one
                        if key == widget.get_active_text():
                            # load data
                            self._controller.component = item
                            self.load_initial_values()
                            # stop iteration
                            break
            else:
                # iteration through the selected arcs
                for i in range(len(self._controller.selected_components)):
                    # check if the current arc is the same as the selected one
                    if self._controller.selected_components[i] != None:
                        if self._controller.selected_components[i].key == widget.get_active_text():
                            # load data
                            self._controller.component = self._controller.selected_components[i]
                            self._load_initial_values()
                            # stop iteration
                            break

    def _on_change_checkbutton(self, widget, data = None):
        """ Is called if the status of the checkbox changes. """

        # check the type of checkbox
        if data.lower() == "auto_line_type":
            # check if a controller is available
            if self._controller != None:
                # set property
                self._controller.auto_line_type = widget.get_active()

    def _load_initial_values(self):
        """ Load the data into the different available widgets form the selected component. """

        # check if a controller is available
        if self._controller != None:
            # check if a component is selected
            if self._controller.component != None:
                # load data
                self._ent[0].set_text(self._controller.component.key)
                self._ent[1].set_text(self._controller.component.label)
                self._ent[2].set_text(str(self._controller.component.weight))
                lt = self._controller.get_line_type()
                if lt == self._controller.LT_STRAIGHT:
                    self._radio_button_straight.set_active(True)
                if lt == self._controller.LT_CURVED_LOWER:
                    self._radio_button_curved_lower.set_active(True)
                if lt == self._controller.LT_CURVED_UPPER:
                    self._radio_button_curved_upper.set_active(True)

if __name__ == "__main__":
    app = ViewConfigurationArc()
    app.show()
    gtk.main()
