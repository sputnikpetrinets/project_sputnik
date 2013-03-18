#!/usr/bin/python

class Memento(object):
    """
    This class defines the Memento objects and contains all necessary data to recreate a previous condition.
    """

    _object = None

    def __init__(self):
        """ Constructor of Memento and default values will be initialised. """

        # call constructor of parent class
        super(Memento, self).__init__()
        self._object = None

    def __init__(self, state = None):
        """ Constructor of Memento and the defined status will be stored. """

        # call constructor of parent class
        super(Memento, self).__init__()

        # set the state of the memento
        if state != None:
            self._object = state
        else:
            self._object = None

    @property
    def state(self):
        """ Return state of the memento. """
        return self._object

    @state.setter
    def state(self, state):
        """ Set state of the memento. """
        self._object = state
