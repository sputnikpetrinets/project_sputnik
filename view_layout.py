#!/usr/bin/python

import view

import pygtk
import gtk

class ViewLayout(view.View):
    """ The ViewLayout class is a specific view that inherits from the general View class and is used to visualise the configuration window for the layouting algorithms and contains a ControllerLayout object. """

    I_NONE = 0
    I_ENTRY = 1
    I_SPIN_BUTTON = 2
    I_RADIO_BUTTON = 3
    I_CHECK_BUTTON = 4

    __ent = None

    def __init__(self):
        """ Constructor of ViewLayout. """
        
        # call constructor of parent class
        view.View.__init__(self)
        
        # set default values
        self._window.resize(150, 150)
        self._window.set_title("Layout")

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewLayout. """
        
        # call constructor of parent class
        view.View.__init__(self, model, controller)

        # set default values
        self._window.resize(150, 150)
        self._window.set_title("Layout")

    def show(self):
        """ Interface to create and display the GUI on the screen. """

        # call show method from the parent class
        view.View.show(self)

        # check if a controller is available
        if self._controller == None:
            # abort method
            return

        # create table
        self._table = gtk.Table(7, 2, False)
        
        # create widgets
        self.__ent = self._add_label_widget_pair(["Algorithm:", "", "Width:", "Height:", "Border:", "Post-Processing Iterations:"], 
                                               ["Spectral with Post-Processing", "", self._controller.width, self._controller.height, self._controller.border, self._controller.iterations], 
                                               [[0, 1, 0, 1], [0, 1, 1, 2], [0, 1, 2, 3], [0, 1, 3, 4], [0, 1, 4, 5], [0, 1, 5, 6]], 
                                               [[1, 2, 0, 1], [1, 2, 1, 2], [1, 2, 2, 3], [1, 2, 3, 4], [1, 2, 4, 5], [1, 2, 5, 6]], 
                                               [self.I_NONE, self.I_NONE, self.I_ENTRY, self.I_ENTRY, self.I_ENTRY, self.I_ENTRY])

        # create OK and Cancel button
        button_ok = gtk.Button("OK")
        button_ok.connect("clicked", self._on_ok_clicked)
        button_cancel = gtk.Button("Cancel")
        button_cancel.connect("clicked", self._on_cancel_clicked)

        # attach buttons to the table
        self._table.attach(button_ok, 0, 1, 6, 7)
        self._table.attach(button_cancel, 1, 2, 6, 7)
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
                self._controller.width = int(self.__ent[2].get_text())
                self._controller.height = int(self.__ent[3].get_text())
                self._controller.border = int(self.__ent[4].get_text())
                self._controller.iterations = int(self.__ent[5].get_text())
                # run algorithm
                self._controller.algorithm()
                # close window
                self._window.destroy()
            except ValueError:
                self.show_message_box_error("There are invalid entries!")

    def _on_cancel_clicked(self, button):
        """ Is called if the Cancel button sends the clicked event. """
        self._window.destroy()

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

if __name__ == "__main__":
    app = ViewLayout()
    app.show()
    gtk.main()
