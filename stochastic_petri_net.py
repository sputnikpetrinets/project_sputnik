#!/usr/bin/python

import pygtk
import gtk
import cairo

import petri_net as pn

class StochasticPetriNet(pn.PetriNet):

    def __init__(self):
        super(StochsticPetriNet, self)
        self._petri_net_data = None
        self._sim_data = None
        self._creator = []
    
    def set_petri_net_data(self, petri_net_data):
        pass

    # list of creators
    def set_creator(self, creator, label):
        pass

    def get_petri_net_data(self):
        pass

    def get_simulation_data(self):
        pass

    def show_petri_net(self):
        pass

    def show_simulation(self):
        pass

    def show_simulation_data(self):
        pass

    def save_petri_net(self, path):
        pass

    def calculate_simulation(self):
        pass

    def calculate_components(self):
        pass
