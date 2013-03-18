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

import spectral_a as vis

class ConverterMatrixToStochasticPetriNet(object):
    """ The ConverterMatrixToStochasticPetriNet is used to create the single components of a petri net based on the matrices which are specifying a petri net. """

    _data = None
    _pn = None
    _layout = None

    def __init__(self):
        """ Constructor of ConverterMatrixToStochasticPetriNet. """
        
        # set default values
        self._data = None
        self._pn = None
        self._layout = None

    @property
    def data(self):
        """ Return data (PetriNetData-Object). """
        return self._data

    @data.setter
    def data(self, data):
        """ Set data (PetriNetData-Object). """
        self._data = data

    @property
    def converted_data(self):
        """ Return converted data (PetriNet-Object). """
        return self._pn

    @property
    def places(self):
        """ Return dictionary of places (dictionary key is the same as for the component). """
        return self._pn.places

    @property
    def transitions(self):
        """ Return dictionary of transitions (dictionary key is the same as for the component). """
        return self._pn.transitions

    @property
    def arcs(self):
        """ Return dictionary of arcs (dictionary key is the same as for the component). """
        return self._pn.arcs

    @property
    def layout(self):
        """ Return layouting algorithm. """
        return self._layout

    @layout.setter
    def layout(self, l):
        """ Set layouting algorithm. """
        self._layout = l

    def convert(self):
        """ Start converting process from matrices to components. """

        # Information: A lot of exceptions will be thrown because of the NoneType issue we had and it is necessary to prevent the appliation from crashing.

        # create a PetriNet object
        self._pn = petri_net.PetriNet()
        # set PetriNetData object
        self._pn.data = self._data

        try:
            # create the individual places
            for i in range(len(self._data.places)):
                # set default values for the design
                p = place.Place([0.0, 0.0], 15., [0., 0., 0.], [255., 255., 255.])
                # set properties
                p.label = self._data.places[i]
                p.key = self._data.places[i]
                if self._data.initial_marking != None:
                    p.marking = self._data.initial_marking[i]
                try:
                    if self._data.capacities != None:
                        p.capacity = self._data.capacities[i]
                except IndexError:
                    pass
                # add place to the PetriNet object
                self._pn.add_place(p,)
        except TypeError:
            pass

        try:
            # create the individual transitions
            for i in range(len(self._data.transitions)):
                # set default values for the design
                t = transition.Transition([0.0, 0.0], [15, 30], [0., 0., 0.], [0., 0., 0.])
                # set properties
                t.label = self._data.transitions[i]
                t.key = self._data.transitions[i]
                if self._data.rates != None:
                    t.rate = self._data.rates[i]
                # add transition to the PetirNet object
                self._pn.add_transition(t)
        except TypeError:
            pass

        try:
        # create the individual arcs connecting two nodes
            for i in range(len(self._data.transitions)):
                for j in range(len(self._data.places)):
                    a_pre = None
                    a_post = None
                    a_test = None
                    a_inhib = None

                    # iteration through the matrices to figure out which arc needs to be created

                    try:
                        if self._data.stoichiometry.pre_arcs != None:
                            try:
                                if self._data.stoichiometry.pre_arcs[i, j] != None:
                                    if self._data.stoichiometry.pre_arcs[i, j] != 0:
                                        # create a standard pre arc
                                        a_pre = arc.Arc()
                                        a_pre.line_type = arc.Arc.LINE_TYPE_STRAIGHT
                                        a_pre.label = str("Arc" + self._data.places[j] + "to" + self._data.transitions[i])
                                        a_pre.key = str("Arc" + self._data.places[j] + "to" + self._data.transitions[i])
                                        a_pre.origin = self._pn.get_component(self._data.places[j])
                                        a_pre.target = self._pn.get_component(self._data.transitions[i])
                                        if self._data.stoichiometry.pre_arcs != None:
                                            a_pre.weight = self._data.stoichiometry.pre_arcs[i, j]
                                        # add arc to the PetriNet object
                                        self._pn.add_arc(a_pre)
                            except IndexError:
                                pass
                    except TypeError:
                        pass
                    try:
                        if self._data.stoichiometry.post_arcs != None:
                            try:
                                if self._data.stoichiometry.post_arcs[i, j] != None:
                                    if self._data.stoichiometry.post_arcs[i, j] != 0:
                                        # create a standard post arc
                                        a_post = arc.Arc()
                                        a_post.line_type = arc.Arc.LINE_TYPE_STRAIGHT
                                        a_post.label = str(self._data.transitions[i] + "to" + self._data.places[j])
                                        a_post.key = str(self._data.transitions[i] + "to" + self._data.places[j])
                                        a_post.origin = self._pn.get_component(self._data.transitions[i])
                                        a_post.target = self._pn.get_component(self._data.places[j])
                                        if self._data.stoichiometry.post_arcs != None:
                                            a_post.weight = self._data.stoichiometry.post_arcs[i, j]
                                        # add arc to the PetriNet object
                                        self._pn.add_arc(a_post)
                            except IndexError:
                                pass
                    except TypeError:
                        pass
                    try:
                        if self._data.test_arcs != None:
                            try:
                                if self._data.test_arcs[i, j] != None:
                                    if self._data.test_arcs[i, j] != 0:
                                        # create a test arc
                                        a_test = test_arc.TestArc()
                                        a_test.line_type = test_arc.TestArc.LINE_TYPE_ARC_LOWER
                                        a_test.label = str("TestArc" + self._data.transitions[i] + "to" + self._data.places[j])
                                        a_test.key = str("TestArc" + self._data.transitions[i] + "to" + self._data.places[j])
                                        a_test.target = self._pn.get_component(self._data.transitions[i])
                                        a_test.origin = self._pn.get_component(self._data.places[j])
                                        if self._data.test_arcs != None:
                                            a_test.weight = self._data.test_arcs[i, j]
                                        # add arc to the PetriNet object
                                        self._pn.add_arc(a_test)
                            except IndexError:
                                pass
                    except TypeError:
                        pass
                    try:
                        if self._data.inhibitory_arcs != None:
                            try:
                                if self._data.inhibitory_arcs[i, j] != None:
                                    if self._data.inhibitory_arcs[i, j] != 0:
                                        # create an inhibitory arc
                                        a_inhib = inhibitory_arc.InhibitoryArc()
                                        a_inhib.line_type = inhibitory_arc.InhibitoryArc.LINE_TYPE_ARC_UPPER
                                        a_inhib.label = str("InhibitoryArc" + self._data.transitions[i] + "to" + self._data.places[j])
                                        a_inhib.key = str("InhibitoryArc" + self._data.transitions[i] + "to" + self._data.places[j])
                                        a_inhib.target = self._pn.get_component(self._data.transitions[i])
                                        a_inhib.origin = self._pn.get_component(self._data.places[j])
                                        if self._data.inhibitory_arcs != None:
                                            a_inhib.weight = self._data.inhibitory_arcs[i, j]
                                        # add arc to the PetriNet object
                                        self._pn.add_arc(a_inhib)
                            except IndexError:
                                pass
                    except TypeError:
                        pass

                    # determine the style of the line automatically
                    # if two standard arcs are available the curved arcs will be chosen
                    if a_pre != None and a_post != None:
                        a_pre.line_type = arc.Arc.LINE_TYPE_ARC_LOWER
                        self._pn.update(a_pre, a_pre.key)
                        a_post.line_type = arc.Arc.LINE_TYPE_ARC_UPPER
                        self._pn.update(a_post, a_post.key)
        except TypeError:
            pass

#        print len(self._pn.arcs)
        # if an algorithm is defined the positions of the components will be determined
        if self._layout != None:
            self.__layout_components()

    def __layout_components(self):
        """ Calculate the positions of the components. """

        # set data
        self._layout.petri_net = self._data
        self._layout.get_petri_net()
        # set properties
        self._layout.width = 900
        self._layout.height = 600
        self._layout.iterations = 1
        self._grid = 50
        self._border = 75
        # calculate the positions
        self._layout.calculate()
        # set postions for each component
        calc_pos = self._layout.node_positions
        for key, position in calc_pos.items():
            component = self._pn.get_component(key)
            if component != None:
                component.position = position
                self._pn.update(component, key)

if __name__ == "__main__":
    converter = ConverterMatrixToStochasticPetriNet()
    converter.convert()

        
