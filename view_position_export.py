#!/usr/bin/python

import sys

import view
import model
import controller
import controller_petri_net_export

import pygtk
import gtk

class ViewPositionExport(view.View):

    def __init__(self):
        view.View.__init__(self)
        self._window.resize(250, 250)
        self._window.set_title("Export: Component Positions")

    def __init__(self, model = None, controller = None):
        view.View.__init__(self, model, controller)
        self._window.resize(250, 250)
        self._window.set_title("Export: Component Positions")
        if self._model != None:
            self._model.add(self)

    def show(self):
        #o.Observer.show(self)

        self._table = gtk.Table(9, 2, False)

        if self._controller == None:
            return

        self._ent_path = self._add_entry("", [0, 1, 0, 1])
        button_path = gtk.Button("...")
        button_path.connect("clicked", self._on_path_clicked)
        self._table.attach(button_path, 1, 2, 0, 1)
        self._add_label("", [0, 1, 1, 2])

        button_ok = gtk.Button("Export")
        button_ok.connect("clicked", self._on_ok_clicked)
        button_cancel = gtk.Button("Cancel")
        button_cancel.connect("clicked", self._on_cancel_clicked)

        self._add_label("", [0, 1, 7, 8])

        self._table.attach(button_ok, 0, 1, 8, 9)
        self._table.attach(button_cancel, 1, 2, 8, 9)
        self._window.add(self._table)
        self._window.show_all()
        self._window.show()

    def _add_label(self, text, position):
        label = gtk.Label()
        label.set_markup(text)
        self._table.attach(label, *position)
        return label

    def _add_entry(self, initial_value, position):
        ent = gtk.Entry()
        ent.set_text(str(initial_value))
        self._table.attach(ent, *position)
        return ent

    def _on_ok_clicked(self, button):
        if self._controller != None:
            self._window.hide()
            self._controller.path = self._ent_path.get_text()
            self._controller.export()
            self._window.show()

    def _on_path_clicked(self, button):
        file_chooser = gtk.FileChooserDialog("Export File", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))        
        if file_chooser.run() == gtk.RESPONSE_OK:
            self._controller.path = file_chooser.get_filename()
            self._ent_path.set_text(self._controller.path)
            if self._controller.path.endswith(".pdf"):
                self._radio_button_pdf.set_active(True)
            if self._controller.path.endswith(".ps"):
                self._radio_button_ps.set_active(True)
            if self._controller.path.endswith(".svg"):
                self._radio_button_svg.set_active(True)
            if self._controller.path.endswith(".png"):
                self._radio_button_png.set_active(True)
            if self._controller.path.endswith(".jpg") or self._controller.path.endswith(".jpeg"):
                self._radio_button_jpg.set_active(True)
        file_chooser.destroy() 

    def _on_cancel_clicked(self, button):
        self._window.destroy()

    def _on_radio_button_changed(self, widget, data = None):
        if self._controller != None:
            if widget.get_active() and data.lower() == "pdf":
                self._controller.format = controller_petri_net_export.ControllerPetriNetExport.E_PDF
            if widget.get_active() and data.lower() == "ps":
                self._controller.format = controller_petri_net_export.ControllerPetriNetExport.E_PS
            if widget.get_active() and data.lower() == "svg":
                self._controller.format = controller_petri_net_export.ControllerPetriNetExport.E_SVG
            if widget.get_active() and data.lower() == "png":
                self._controller.format = controller_petri_net_export.ControllerPetriNetExport.E_PNG
            if widget.get_active() and data.lower() == "jpg":
                self._controller.format = controller_petri_net_export.ControllerPetriNetExport.E_JPG

if __name__ == "__main__":
    app = ViewPetriNetExport()
    app.show()
    gtk.main()
