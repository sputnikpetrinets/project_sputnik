#!/usr/bin/python

import pygtk
import gtk
import cairo

import numpy as np

import place
import arc
import test_arc
import inhibitory_arc
import transition

import petri_net
import petri_net_data

import stoichiometry

class ConverterStochasticPetriNetToMatrix(object):
    """ The ConverterStochasticPetriNetToMatrix is used to create the petri net specifying matrices based on the available components. """

    _data = None
    _converted_data = None
    _layout = None

    def __init__(self):
        """ Constructor of ConverterStochasticPetriNetToMatrix. """

        # set default values
        self._data = None
        self._pn = None
        self._layout = None

    @property
    def data(self):
        """ Return data (PetriNet-Object). """
        return self._data

    @data.setter
    def data(self, data):
        """ Set data (PetriNet-Object). """
        self._data = data

    @property
    def converted_data(self):
        """ Return converted data (PetriNetData-Object). """
        return self._converted_data

    def convert(self):
        """ Start converting process form components to matrices. """

        # create a new PetriNetData object
        self._converted_data = petri_net_data.PetriNetData()
        # set arrays for places and transitions
        self._converted_data.places = self._create_array(self._data.places)
        self._converted_data.transitions = self._create_array(self._data.transitions)
        
        l_pre = []
        l_post = []
        l_test = []
        l_inhib = []
        # determine the type of the arcs connecting the nodes (pre, post, test or inhibitory arc)
        for key, item in self._data.arcs.items():
            if type(item) == arc.Arc:
                if type(item.origin) == place.Place and type(item.target) == transition.Transition:
                    l_pre.append(item)
                if type(item.target) == place.Place and type(item.origin) == transition.Transition:
                    l_post.append(item)
            if type(item) == test_arc.TestArc:
                l_test.append(item)
            if type(item) == inhibitory_arc.InhibitoryArc:
                l_inhib.append(item)

        # create the stoichiometry object
        s = stoichiometry.Stoich()
        # set matrices for pre and post arcs
        s.pre_arcs = self._create_matrix(self._data.places, self._data.transitions, l_pre)
        #print "POST:", self._create_matrix(self._data.places, self._data.transitions, l_post)
        s.post_arcs = self._create_matrix(self._data.places, self._data.transitions, l_post)
        try:
            # calculate stoichiometry and dependency matrix if possible
            s.calculate_stoichiometry_matrix()
            s.calculate_dependency_matrix()
        except TypeError:
            pass # NoneType problem
        #print "SET POST:", s.post_arcs
        
        # set data
        self._converted_data.stoichiometry = s
        self._converted_data.test_arcs = self._create_matrix(self._data.places, self._data.transitions, l_test)
        self._converted_data.inhibitory_arcs = self._create_matrix(self._data.places, self._data.transitions, l_inhib)

        l_rates = []
        l_capacities = []
        l_markings = []

        # performance improvement
        check_zeros_capacities = True

        # only if capacities are available they will be set and otherwise the object will be set to None
        # performance reasons during the simulation
        for key, item in self._data.places.items():
            if key != "new_comp":
                l_markings.append(item.marking)
                if item.capacity != 0:
                    check_zeros_capacities = False
                l_capacities.append(item.capacity)
        if check_zeros_capacities:
            self._converted_data.capacities = None
        else:
            self._converted_data.capacities = np.array(l_capacities)

        # determine the rates
        for key, item in self._data.transitions.items():
            if key != "new_comp":
                l_rates.append(item.rate)

        # set rates and markings
        self._converted_data.rates = np.array(l_rates)
        self._converted_data.initial_marking = np.array(l_markings)

#        print self._converted_data.places
#        print self._converted_data.transitions
#        print self._converted_data.stoichiometry.pre_arcs
#        print self._converted_data.stoichiometry.post_arcs
#        print self._converted_data.test_arcs
#        print self._converted_data.inhibitory_arcs
#        print self._converted_data.rates
#        print self._converted_data.initial_marking
#        print self._converted_data.capacities

    def _create_array(self, comp_list):
        """ Create a numpy array for the given list of components and returns it. """

        l = []
        # create list of components
        for key, item in comp_list.items():
            if key != "new_comp":
                l.append(item.label)
        # return numpy array
        return np.array(l)

    def _create_matrix(self, places, transitions, arcs):
        """ Create a numpy matrix for the given list of places, transitions and arcs and returns it. This method is used for creating the matrices specifying the connections between the nodes. """

        l = []
        check_zeros = True

        # iteration through all transitions
        for t_key, t_item in transitions.items():
            l_sub = []
            add_item = False
            if t_key == "new_comp":
                next
            # iteration through all places
            for p_key, p_item in places.items():
                add_item = False
                if p_key == "new_comp":
                    next
                for a_item in arcs:
                    if a_item.key != "new_comp":
                        if a_item.origin != None:
                            # check if a weight needs to be attached to the sublist
                            if a_item.origin.is_equal(p_item) and a_item.target.is_equal(t_item) or a_item.origin.is_equal(t_item) and a_item.target.is_equal(p_item):
                                l_sub.append(a_item.weight)
                                add_item = True
                                check_zeros = False
                                break
                if not add_item and p_key != "new_comp":
                    # no weight available that means no arc is available and value is set to 0
                    l_sub.append(0)
            # attach sublist to the list
            l.append(l_sub)
        # check if any connections are available
        if check_zeros:
            # return None if no connections are available - performance reasons during the simulation
            return None
    # create and return numpy matrix
        return np.matrix(l, dtype = int)

        
