#!/usr/bin/python

import sys

import view
import model
import controller
import controller_resize_drawingarea

import pygtk
import gtk

class ViewResizeDrawingArea(view.View):

    def __init__(self):
        view.View.__init__(self)
        self._window.resize(150, 150)
        self._window.set_title("Resize Drawing-Area")

    def __init__(self, model = None, controller = None):
        view.View.__init__(self, model, controller)
        self._window.resize(150, 150)
        self._window.set_title("Resize Drawing-Area")
        if self._model != None:
            self._model.add(self)

    def show(self):
        #o.Observer.show(self)

        self._table = gtk.Table(3, 2, False)

        if self._controller == None:
            return

        self._add_label("Width:", [0, 1, 0, 1])
        self._add_label("Height:", [0, 1, 1, 2])
        self._ent_width = self._add_entry(self._controller.width, [1, 2, 0, 1])
        self._ent_height = self._add_entry(self._controller.height, [1, 2, 1, 2])

        button_ok = gtk.Button("OK")
        button_ok.connect("clicked", self._on_ok_clicked)
        button_cancel = gtk.Button("Cancel")
        button_cancel.connect("clicked", self._on_cancel_clicked)

        self._table.attach(button_ok, 0, 1, 2, 3)
        self._table.attach(button_cancel, 1, 2, 2, 3)
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
        self._controller.width = int(self._ent_width.get_text())
        self._controller.height = int(self._ent_height.get_text())
        self._controller.resize()

    def _on_cancel_clicked(self, button):
        self._window.destroy()

if __name__ == "__main__":
    app = ViewResizeDrawingArea()
    app.show()
    gtk.main()
