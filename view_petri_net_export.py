#!/usr/bin/python

import sys

import view
import controller_petri_net_export

import pygtk
import gtk

class ViewPetriNetExport(view.View):
    """ The ViewPetriNetExport class is a specific view that inherits from the general View class and is used to visualise the petri net export configuration window and contains a ControllerPetriNet object. """

    def __init__(self):
        """ Constructor of ViewPetriNetExport. """
        
        # call constructor of parent class
        view.View.__init__(self)

        # set title and size
        self._window.resize(250, 250)
        self._window.set_title("Export: Petri Net")

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewPetriNetExport. """
        
        # call constructor of parent class
        view.View.__init__(self, model, controller)

        # set title and size
        self._window.resize(250, 250)
        self._window.set_title("Export: Petri Net")

    def show(self):
        """ Interface to create and display the GUI on the screen. """

        # call show method from the parent class
        view.View.show(self)

        # create table
        self._table = gtk.Table(9, 2, False)

        # check if a controller is available
        if self._controller == None:
            # abort method
            return

        # create widgets to choose the path
        self._ent_path = self._add_entry("", [0, 1, 0, 1])
        button_path = gtk.Button("Browse")
        button_path.connect("clicked", self._on_path_clicked)
        self._table.attach(button_path, 1, 2, 0, 1)
        self._add_label("", [0, 1, 1, 2])

        # create widgets to choose the file format
        self._add_label("Please choose the file format:", [0, 1, 2, 3])
        self._radio_button_pdf = gtk.RadioButton(None, "PDF-Format")
        self._radio_button_pdf.connect("toggled", self._on_radio_button_changed, "pdf")
        self._table.attach(self._radio_button_pdf, 1, 2, 2, 3)

        self._radio_button_ps = gtk.RadioButton(self._radio_button_pdf, "PS-Format")
        self._radio_button_ps.connect("toggled", self._on_radio_button_changed, "ps")
        self._table.attach(self._radio_button_ps, 1, 2, 3, 4)

        self._radio_button_svg = gtk.RadioButton(self._radio_button_pdf, "SVG-Format")
        self._radio_button_svg.connect("toggled", self._on_radio_button_changed, "svg")
        self._table.attach(self._radio_button_svg, 1, 2, 4, 5)

        #self._radio_button_png = gtk.RadioButton(self._radio_button_pdf, "PNG-Format")
        #self._radio_button_png.connect("toggled", self._on_radio_button_changed, "png")
        #self._table.attach(self._radio_button_png, 1, 2, 5, 6)

        #self._radio_button_jpg = gtk.RadioButton(self._radio_button_pdf, "JPG-Format")
        #self._radio_button_jpg.connect("toggled", self._on_radio_button_changed, "jpg")
        #self._table.attach(self._radio_button_jpg, 1, 2, 6, 7)

        # create OK and Cancel button
        button_ok = gtk.Button("Export")
        button_ok.connect("clicked", self._on_ok_clicked)
        button_cancel = gtk.Button("Cancel")
        button_cancel.connect("clicked", self._on_cancel_clicked)
        self._add_label("", [0, 1, 7, 8])

        # attach buttons to the table
        self._table.attach(button_ok, 0, 1, 8, 9)
        self._table.attach(button_cancel, 1, 2, 8, 9)
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

    def _on_ok_clicked(self, button):
        """ Is called if the OK button sends the clicked event. """

        # check if a controller is available
        if self._controller != None:
            # hide window
            self._window.hide()
            # set property
            self._controller.path = self._ent_path.get_text()
            # export net
            self._controller.export()
            # show window again
            self._window.show()

            self.show_message_box_info("Petri Net exported!")

    def _on_path_clicked(self, button):
        """ Is called if the Path button sends the clicked event. """
        
        # show a file chooser dialog
        file_chooser = gtk.FileChooserDialog("Export File", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))        
        # choose path
        if file_chooser.run() == gtk.RESPONSE_OK:
            self._controller.path = file_chooser.get_filename()
            # set properties
            self._ent_path.set_text(self._controller.path)
            if self._controller.path.endswith(".pdf"):
                self._radio_button_pdf.set_active(True)
            if self._controller.path.endswith(".ps"):
                self._radio_button_ps.set_active(True)
            if self._controller.path.endswith(".svg"):
                self._radio_button_svg.set_active(True)
            #if self._controller.path.endswith(".png"):
            #    self._radio_button_png.set_active(True)
            #if self._controller.path.endswith(".jpg") or self._controller.path.endswith(".jpeg"):
            #    self._radio_button_jpg.set_active(True)
        file_chooser.destroy() 

    def _on_cancel_clicked(self, button):
        """ Is called if the Cancel button sends the clicked event. """
        self._window.destroy()

    def _on_radio_button_changed(self, widget, data = None):
        """ Is called if the status of a radio button changes. """

        # check if a controller is available
        if self._controller != None:
            # according to the selected radio button the file format will be set
            if widget.get_active() and data.lower() == "pdf":
                self._controller.format = controller_petri_net_export.ControllerPetriNetExport.E_PDF
            if widget.get_active() and data.lower() == "ps":
                self._controller.format = controller_petri_net_export.ControllerPetriNetExport.E_PS
            if widget.get_active() and data.lower() == "svg":
                self._controller.format = controller_petri_net_export.ControllerPetriNetExport.E_SVG
            #if widget.get_active() and data.lower() == "png":
            #    self._controller.format = controller_petri_net_export.ControllerPetriNetExport.E_PNG
            #if widget.get_active() and data.lower() == "jpg":
            #    self._controller.format = controller_petri_net_export.ControllerPetriNetExport.E_JPG

if __name__ == "__main__":
    app = ViewPetriNetExport()
    app.show()
    gtk.main()
