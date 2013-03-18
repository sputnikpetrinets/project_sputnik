#!/usr/bin/python

import sys

import pygtk
import gtk
import cairo

import view
import model as m

import rparser as rpa
import sbml_lex
import pnml_lex
import txt_convert
import txt2_lex

import_libsbml = True

try:
    import sbml_convert
except AttributeError:
    import_libsbml = False

import pnml_convert

import petri_net_data

class ViewFileType(view.View):
    """ The ViewFileType class is a specific view that inherits from the general View class and is used to visualise the file export configuration window and contains a ControllerFileType object. """

    F_TXT = 0
    F_PNML = 1
    F_SBML = 2

    _file_type = F_TXT

    def __init__(self):
        """ Constructor of ViewFileType. """
        
        # call constructor of parent class
        view.View.__init__(self)

        # set title and size
        self._window.set_title("File")
        self._window.resize(200, 200)

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewFileType. """
        
        # call constructor of parent class
        view.View.__init__(self, model, controller)

        # set title and size
        self._window.set_title("File")
        self._window.resize(200, 150)

    def show(self):
        """ Interface to create and display the GUI on the screen. """

        # call show method from the parent class
        view.View.show(self)
        
        # create table
        self._table = gtk.Table(8, 2, False)

        # create description
        label = gtk.Label()
        label.set_markup("Which parser should be used?")
        self._table.attach(label, 0, 1, 0, 1)

        # create radio buttons
        self._radio_button_txt = gtk.RadioButton(None, "TXT-Parser")
        self._radio_button_txt.connect("toggled", self._on_change_radio_button, self.F_TXT)
        self._radio_button_pnml = gtk.RadioButton(self._radio_button_txt, "PNML-Parser")
        self._radio_button_pnml.connect("toggled", self._on_change_radio_button, self.F_PNML)
        self._radio_button_sbml = gtk.RadioButton(self._radio_button_txt, "SBML-Parser")
        self._radio_button_sbml.connect("toggled", self._on_change_radio_button, self.F_SBML)
        self._table.attach(self._radio_button_txt, 1, 2, 0, 1)
        self._table.attach(self._radio_button_pnml, 1, 2, 1, 2)
        self._table.attach(self._radio_button_sbml, 1, 2, 2, 3)

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

    def _on_change_radio_button(self, widget, data = None):
        """ Is called if the status of a radio button changes. """

        # define the correct format
        if widget.get_active() and data == self.F_TXT:
            self._file_type = self.F_TXT
        if widget.get_active() and data == self.F_PNML:
            self._file_type = self.F_PNML
        if widget.get_active() and data == self.F_SBML:
            if import_libsbml:
                self._file_type = self.F_SBML
            else:
                self._file_type = self.F_TXT
                self._radio_button_txt.set_active(True)
                self.show_message_box_warning("LibSBML is not installed and the SBML format is not usable!")

    def _on_ok_clicked(self, button):
        """ Is called if the OK button sends the clicked event. """

        # check if a controller is available
        if self._controller != None:
            try:
                # check the modus and define the right converter and lexer
                if self._controller.modus == self._controller.M_OPEN:
                    if self._file_type == self.F_TXT:
                        self._controller.open(txt2_lex.RLexerTxt())
                    elif self._file_type == self.F_SBML:
                    #self._controller.open(lexer = sbml_lex.RLexerSBML())
                        pass
                    elif self._file_type == self.F_PNML:
                        self._controller.open(lexer = pnml_lex.RLexerPNML())
                    else:
                        self.show_message_box_warning("File extension not recognised!")
                    # close the window
                    self._window.destroy()
    
                if self._controller.modus == self._controller.M_SAVE:
                    if self._file_type == self.F_TXT:
                        self._controller.save(txt_convert.WConverterTxt(self._model.data.petri_net_data))
                    elif self._file_type == self.F_SBML:
                        self._controller.save(sbml_convert.WConverterSbml(self._model.data.petri_net_data))
                    elif self._file_type == self.F_PNML:
                        self._controller.save(pnml_convert.WConverterPnml(self._model.data.petri_net_data))
                    else:
                        self.show_message_box_warning("File extension not recognised!")
                    self._window.destroy()
            except AttributeError:
                self.show_message_box_warning("Invalid File Format!")

    def _on_cancel_clicked(self, button):
        """ Is called if the Cancel button sends the clicked event. """
        self._window.destroy()

if __name__ == "__main__":
    app = ViewFileType()
    app.show()
    gtk.main()
