#!/usr/bin/python

import gtk
import pygtk
import cairo

class MVCObserver(object):
    """
    The MVCObserver class is the parent class of the specific observers (views and controllers) which are part of the Model-View-Controller (MVC) Architecture and inherit from this class. View are implementing the Graphical User Interface (GUI) and controller the interaction between the user and the data. Those observers can register with the model to receive notification events.
    """

    _model = None

    def __init__(self):
        """ Constructor of MVCObserver and default values will be initialised. """

        self._model = None
        self._controller = None

    def __init__(self, model = None):
        """ Constructor of MVCObserver and default values will be initialised. """
        
        self._model = model
        if self._model != None:
            self._model.add(self)

    @property
    def model(self):
        """ Return model (MVCObservable-Object). """
        return self._model

    @model.setter
    def model(self, model):
        """ Set model (MVCObservable-Object). """
        self._model = model
        # check if observer object can be registered
        if self._model != None:
            # register observer
            self._model.add(self)

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """
        pass

    def reset(self):
        """ Interface to notify MVCObserver objects about a reset event. """
        pass
