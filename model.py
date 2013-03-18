#!/usr/bin/python

import copy

import pygtk
import gtk

import mvc_observable as o
import memento
import memento_container

import model_state

class Model(o.MVCObservable):
    """
    The Model class is a specific model which is acting as the core of the Model-View-Controller (MVC) Architecture of the Graphical User Interface (GUI) and inherits from the general model class called MVCObservable. It contains the main data and delivers interfaces to register and remove observers.
    """

    _container = None
    _data = None
    _output_data = None

    _output_args = []

    def __init__(self):
        """ Constructor of Model and default values will be initialised. """

        # call constructor of parent class
        super(Model, self).__init__()

        self._data = None
        self._output_data = None

        self._container = memento_container.MementoContainer()
        self._container.storage_limit = 100

    @property
    def output(self):
        """ Return output data. """
        return self._output_data

    @output.setter
    def output(self, data):
        """ Set output data. """
        self._output_data = data

    @property
    def output_args(self):
        """ Return output arguments. """
        return self._output_args

    @output_args.setter
    def output_args(self, args):
        """ Set output arguments. """
        self._output_args = args

    def create_snapshot(self):
        """ Create a snapshot of the current data, that are defining the petri net, to allow the recreation of a previous state. The data will be cloned to avoid a conflict with references. """

        try:
            # instantiate an object that will define the snapshot
            state = model_state.ModelState()
            # check if data are available
            if self._data != None and self._data.petri_net_data != None:
                # clone data
                try:
                    state.data = self.data.petri_net_data.clone()
                except AttributeError:
                    return
                state.position = copy.deepcopy(self.data.get_positions())
                # issue with NoneTypes because of this the AttributeError will be chaught
                if self.output != None:
                    try:
                        # clone output data
                        state.output = self.output.clone()
                    except AttributeError:
                        state.output = None
                else:
                    state.output = None
                # check if output arguments are available
                if self.output_args != None:
                    state.output_args = copy.deepcopy(self.output_args)
                else:
                    state.output_args = None
                # instantiate an empty memento
                m = memento.Memento()
                # assign data to memento
                m.state = state
                # attach memento to container
                self._container.add(m)
        except TypeError:
            pass

    def remove_last_snapshot(self):
        """ Remove the last created snapshot from the container. """
        self._container.remove_last_memento()

    def notify_output(self):
        """ Notification of all registered observers that there was a change of the output data. """
        for observer in self._observers:
            # observer notification
            observer.update_output()

    def notify_component(self, key):
        """ Notification of all registered observers that there was a change of a component with the defined key. """
	for observer in self._observers:
            # observer notification
            observer.update_component(key)

    def notify_reset(self):
        """ Notification of all registered observers that there was a reset event. """
        for observer in self._observers:
            # observer notification
            observer.reset()

    def notify_undo(self):
        """ Notification of all registered observers that there was an undo event. """
        for observer in self._observers:
            # observer notification
            observer.undo()

    def undo(self):
        """ Restore the previous data state. """
        self.restore_state(self._container.undo())

    def restore_state(self, memento):
        """ Restore the data state defined through the input Memento object. """
        # check if the memento is valid
        if memento != None:
            # minimal amount of data will be stored and based on those the petri net will be recreated
            self.data.petri_net_data = memento.state.data
            self.output = memento.state.output
            self.output_args = memento.state.output_args
            self.data.convert_components(memento.state.position)

