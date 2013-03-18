#!/usr/bin/python

import pygtk
import gtk

import view_main
import controller_main
import petri_net
import model as m

if __name__ == "__main__":
    model = m.Model()
    model.data = petri_net.PetriNet()
    controller = controller_main.ControllerMain()
    app = view_main.ViewMain()
    controller.view = app
    controller.model = model
    app.model = model
    app.controller = controller
    app.show()
    gtk.main()

