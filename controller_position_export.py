#!/usr/bin/python

import model as m
import view_layout as v
import controller as c
import view_petri_net_export
import petri_net_export 

class ControllerPositionExport(c.Controller):
    """ The ControllerPositionExport class is a specific controller that inherits from the general Controller class and is used to manage the user interactions of the position export configuration window and the application (ViewPositionExport). """

    E_PDF = 0
    E_PS = 1
    E_SVG = 2
    E_PNG = 3
    E_JPG = 4

    _path = ""
    _format = E_PDF
    _drawing_area = None

    def __init__(self):
        c.Controller.__init__(self)

    def __init__(self, model = None, view = None):
        c.Controller.__init__(self, model, view)

    def update(self):
        pass

    def update_component(self, key):
        pass

    def update_output(self):
        pass

    def reset(self):
        pass

    def undo(self):
        pass

    @property
    def path(self):
        return self._path

    @property
    def format(self):
        return self._format

    @property
    def drawing_area(self):
        return self._drawing_area

    @path.setter
    def path(self, p):
        self._path = p

    @format.setter
    def format(self, f):
        self._format = f

    @drawing_area.setter
    def drawing_area(self, area):
        self._drawing_area = area

    def export(self):
        if self._drawing_area != None and self._path != None and self._path != "":
            exp = petri_net_export.PetriNetExport()
            exp.drawing_area = self._drawing_area
            exp.path = self._path

            if self._format == self.E_PDF:
                exp.export_as_pdf()
            if self._format == self.E_PS:
                exp.export_as_ps()
            if self._format == self.E_SVG:
                exp.export_as_svg()
            if self._format == self.E_PNG:
                exp.export_as_png()
            if self._format == self.E_JPG:
                exp.export_as_jpg()

            return True
        return False

