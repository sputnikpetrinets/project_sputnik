#!/usr/bin/python

import mvc_observer

class Controller(mvc_observer.MVCObserver):
    """
    The Controller class is the parent class of the specific controller observers which are part of the Model-View-Controller (MVC) Architecture and inherit from this class. This class inherits from the more general MVCObserver class and extend its functionalities. Controllers are implementing the interaction between the user and the application. Those observers can register with the model to receive notification events.
    """

    _view = None

    def __init__(self):
        """ Constructor of Controller and default values will be initialised. """

        # call constructor of parent class
        mvc_observer.MVCObserver.__init__(self)
        self._model = None
        self._view = None

    def __init__(self, model = None, view = None):
        """ Constructor of Controller and values will be set. """

        # call constructor of parent class
        mvc_observer.MVCObserver.__init__(self)
        self._model = model
        self._view = view
        # register view
        if self._view != None and self._model != None:
            self._model.add(self._view)

    @property
    def view(self):
        """ Return view (MVCObserver-Object). """
        return self._view

    @view.setter
    def view(self, v):
        """ Set view (MVCObserver-Object). """
        self._view = v
        # register view
        if self._view != None and self._model != None:
            self._model.add(self._view)
