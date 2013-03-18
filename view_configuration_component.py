#!/usr/bin/python

import pygtk
import gtk

import view

class ViewConfigurationComponent(view.View):
    """ The ViewConfigurationComponent class is a specific view that inherits from the general View class and is used as a parent class to visualise the configuration window and contains a ControllerConfigurationComponent object. """

    I_NONE = 0
    I_ENTRY = 1
    I_SPIN_BUTTON = 2
    I_RADIO_BUTTON = 3
    I_CHECK_BUTTON = 4

    _table = None
    _component = None

    def __init__(self):
        """ Constructor of ViewConfigurationComponent. """
        
        # call constructor of parent class
        view.View.__init__(self)

        # set title of the window
        self._window.set_title("Configuration: Component")

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewConfigurationComponent. """
        
        # call constructor of parent class
        view.View.__init__(self, model, controller)

        # set title of the window
        self._window.set_title("Configuration: Component")

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

    def _add_label_widget_pair(self, list_label, list_initial_value, list_tbl_pos_label, list_tbl_pos_widget, list_widget_type):
        """ General method to add different widgets to a defined location within a table. The first parameter describes a label describing the widged, list_initial_value the initial value, list_tbl_pos_label the position of the label and list_tbl_pos_widget the position of the widget within the table. List_widget_type defines the widget type. A list with all references to the widgets, in the same order, will be returned. """

        # stores references to the widgets
        ent = []
        # needed to connect radio buttons
        radio_btn = None
        # iteration through all 
        for i in range(len(list_label)):
            # create label
            label = gtk.Label()
            if list_widget_type[i] == self.I_CHECK_BUTTON:
                label.set_markup("")
            else:
                label.set_markup(list_label[i])
            # attach label to the table
            self._table.attach(label, list_tbl_pos_label[i][0], list_tbl_pos_label[i][1], list_tbl_pos_label[i][2], list_tbl_pos_label[i][3], gtk.FILL, gtk.FILL)
            
            # create another label
            if list_widget_type[i] == self.I_NONE:
                comp = gtk.Label()
                comp.set_markup(list_initial_value[i])

            # create an entry box
            if list_widget_type[i] == self.I_ENTRY:
                comp = gtk.Entry()
                comp.set_text(str(list_initial_value[i]))

            # create a spin button
            if list_widget_type[i] == self.I_SPIN_BUTTON:
                comp = gtk.SpinButton()
                comp.set_adjustment(gtk.Adjustment(float(list_initial_value[i]), 0, sys.maxint, 1, 10, 0))

            # create a radio button
            if list_widget_type[i] == self.I_RADIO_BUTTON:
                comp = gtk.RadioButton(radio_btn, list_initial_value[i])
                if radio_btn == None:
                    radio_btn = comp
                comp.connect("toggled", self._on_change_radio_button, list_initial_value[i])

            # create a checkbox
            if list_widget_type[i] == self.I_CHECK_BUTTON:
                comp = gtk.CheckButton(list_label[i])
                comp.set_active(list_initial_value[i])
                comp.connect("toggled", self._on_change_check_button, list_label[i])
            # attach reference to the list of references
            ent.append(comp)
            # attach widget to the list
            self._table.attach(comp, list_tbl_pos_widget[i][0], list_tbl_pos_widget[i][1], list_tbl_pos_widget[i][2], list_tbl_pos_widget[i][3])
            
        # return list of references
        return ent

    def _on_change_radio_button(self, widget, data = None):
        """ Is called if a radio button change ocurres. """
        pass

    def _on_change_check_button(self, widget, data = None):
        """ Is called if a check button change ocurres. """
        pass
    
if __name__ == "__main__":
    app = ViewConfigurationComponent()
    app.show()
    gtk.main()
    
