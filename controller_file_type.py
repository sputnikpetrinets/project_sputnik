#!/usr/bin/python

import model as m
import view_file_type as v
import controller as c

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

import petri_net
import petri_net_data
#import RPndHolder as pndh

import converter_matrixtostochasticpetrinet
import converter_stochasticpetrinettomatrix

import spectral_a

class ControllerFileType(c.Controller):
    """ The ControllerFileType class is a specific controller that inherits from the general Controller class and is used to manage the user interactions of the file export configuration window and the application (ViewFileType). """

    M_OPEN = 0
    M_SAVE = 1

    _path = None
    _modus = 0

    def __init__(self):
        """ Constructor of ControllerConfigurationComponent. """
        
        # call constructor of parent class
        c.Controller.__init__(self)

        # set default values
        self._path = None
        self._modus = 0

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerConfigurationComponent. """
        
        # call constructor of parent class
        c.Controller.__init__(self, model, view)

        # set default values
        self._path = None
        self._modus = 0

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
    def modus(self):
        """ Return modus. """
        return self._modus
    
    @property
    def path(self):
        """ Return path. """
        return self._path

    @modus.setter
    def modus(self, m):
        """ Set modus. """
        self._modus = m

    @path.setter
    def path(self, p):
        """ Set path. """
        self._path = p

    def open(self, lexer):
        """ Input file with the define path will be opened, analysed and a PetriNet object will be created if possible and assigned to the functional core of the MVC architecture. """

        # check if a path is defined
        if self._path == None:
            # abort method
            return False

        # read file
        f = infile = open(self._path, 'r')
        # create token list
        token_list = lexer.lex(f)

        # set parser
        parser = rpa.RParser()
        # set token list 
        parser.data = token_list
        # parse token list to PetriNetData
        parser.parse()

        # set the data
        self._model.data = petri_net.PetriNet()
        self._model.data.petri_net_data = parser.output
        # set converter
        self._model.data.converter_components = converter_matrixtostochasticpetrinet.ConverterMatrixToStochasticPetriNet()
        self._model.data.converter_matrices = converter_stochasticpetrinettomatrix.ConverterStochasticPetriNetToMatrix()

        # instantiate algorithm to calculate the positions of the individual components
        layout = spectral_a.Spectral()
        # initial properties
        layout.width = 900
        layout.height = 600
        layout.border = 85
        layout.d_radius = 85

        # set algorithm
        self._model.data.converter_components.layout = layout
        # set data
        self._model.data.converter_components.layout.data = self._model.data.petri_net_data
        # convert components
        self._model.data.convert_components()
        # notification ot the other observers
        self._model.notify()

        return True

    def save(self, converter):
        """ Output file with the defined path will be created through a defined format. For this the data stored in the model of the MVC architecture is used. """

        # check if a path is defined
        if self._path == None:
            # abort method
            return False

        # create token list from the PetriNetData object
        token = converter.getPetriNetData()
        # create output file
        converter.save(self._path)

        return True
