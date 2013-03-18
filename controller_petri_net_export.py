#!/usr/bin/python

import model as m
import controller as c

import view_petri_net_export
import drawing_area_export 

class ControllerPetriNetExport(c.Controller):
    """ The ControllerPetriNetExport class is a specific controller that inherits from the general Controller class and is used to manage the user interactions of the file export configuration window and the application (ViewPetriNetExport). """
    E_PDF = 0
    E_PS = 1
    E_SVG = 2
    E_PNG = 3
    E_JPG = 4

    _path = ""
    _format = E_PDF
    _drawing_area = None

    def __init__(self):
        """ Constructor of ControllerPetriNetExport. """

        # call constructor of parent class
        c.Controller.__init__(self)

        # set default values
        self._path = ""
        self._format = self.E_PDF
        self._drawing_area = None

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerPetriNetExport. """

        # call constructor of parent class
        c.Controller.__init__(self, model, view)

        # set default values
        self._path = ""
        self._format = self.E_PDF
        self._drawing_area = None

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """
        pass

    def update_component(self, key):
        """ Interface to notify Observer objects about a data change of a component. """
        pass

    def update_output(self):
        """ Interface to notify Observer objects about a data change of simulation results. """
        pass

    def reset(self):
        """ Interface to notify MVCObserver objects about a reset event. """
        pass

    def undo(self):
        """ Interface to notify Observer objects about an undo. """
        pass

    @property
    def path(self):
        """ Return path. """
        return self._path

    @property
    def format(self):
        """ Return file format. """
        return self._format

    @property
    def drawing_area(self):
        """ Return drawing area object. """
        return self._drawing_area

    @path.setter
    def path(self, p):
        """ Set path. """
        self._path = p

    @format.setter
    def format(self, f):
        """ Set file format. """
        self._format = f

    @drawing_area.setter
    def drawing_area(self, area):
        """ Set drawing area object. """
        self._drawing_area = area

    def export(self):
        """ Export the content of the drawing area object into a file with the defined path and in the defined file format. """

        # check if the drawing area object and the path are set
        if self._drawing_area != None and self._path != None and self._path != "":
            # instantiate an object written to export the content of the drawing area
            exp = drawing_area_export.DrawingAreaExport()
            # assign the properties
            exp.drawing_area = self._drawing_area
            exp.path = self._path
            
            # check the export format and call the exportation method
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

