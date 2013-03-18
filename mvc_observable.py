#!/usr/bin/python

import mvc_observer as o

class MVCObservable(object):
    """
    The MVCObservable class is the parent class of the specific models which are acting as the core of the Model-View-Controller (MVC) Architecture and inherit from this class. It contains the main data and delivers interfaces to register and remove observers.
    """

    _observers = []

    def __init__(self):
        """ Constructor of MVCObservable and default values will be initialised. """

        # call constructor of parent class
        self._observers = []

    @property
    def data(self):
        """ Return core data. """
        return self._data

    @data.setter
    def data(self, data = None):
        """ Set core data. """
        self._data = data

    def add(self, observer):
        """ Register an observer (MVCObserver-object). """
        if observer != None:
            self._observers.append(observer)

    def remove(self, observer):
        """ Remove an observer from the list of registered observers (MVCObserver-object). """
        if observer != None:
            self._observers.remove(observer)

    def notify(self):
        """ The general interface to notify observers about a data change. """
	for observer in self._observers:
            observer.update()

    


