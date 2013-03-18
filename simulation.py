#!/usr/bin/python

import threading
import time

import numpy as np
import pygtk
import gtk
import cairo
import os
#pygtk.require("2.0")

import observer as o
import model as m
import petri_net as pn
import event

import place
import transition
import arc
import inputarc
import outputarc
import model as m
import petri_net

#import numpy as np
import petri_net_data
import stoichiometry as stoich_1
import algorithm as al
import matplotlib.pyplot as plt
import invariants

class Simulation(o.Observer, threading.Thread):

    _simulation_data = None
    _pn_data = None
    _stop = False
    _model = None
    _path_collection = None
    _frame = None

    def __init__(self, model):
        #super(ViewMain, self).__init__()
        o.Observer.__init__(self)
        threading.Thread.__init__(self) 
        self._model = model

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, f):
        self._frame = f

    @property
    def petri_net_data(self):
        return self._pn_data

    @petri_net_data.setter
    def petri_net_data(self, data):
        self._pn_data = data

    @property
    def simulation_data(self):
        return self._simulation_data

    @simulation_data.setter
    def simulation_data(self, data):
        self._simulation_data = data

    def go_to_iteration(self, itr):
        pass

    def stop(self):
        pass

    def next(self):
        #itr = self._scale.get_value()
        for i in range(self._iteration_pos, int(len(self._simulation_data.markings))):
            #itr += 1
            #self._scale.set_value(int(itr))
            for j in range(len(self._pn_data.places)):
                if self._simulation_data.markings[i, j] != self._simulation_data.markings[i - 1, j]:
                    # path vum vorheriga place zum aktuella place
                    place = self._model.get_data().get_place(self._pn_data.places[j])
                    place.set_marking(int(self._simulation_data.markings[i, j]))
                    # update auch labels!!!
                    if place != None:
                        if self._path_collection != None:
                            for path in self._path_collection:
                                for item in path:
                                    item.set_rgb_edge(0, 0, 0)
                                    self._model.get_data().update(item, item.get_key())

                        self._path_collection = self._model.get_data().get_path(place)
                        print self._path_collection
                        self._add_console_text(str(self._path_collection))
                        
                        if self._path_collection != None:
                            for path in self._path_collection:
                                for item in path:
                                    item.set_rgb_edge(255, 0, 0)
                                    self._model.get_data().update(item, item.get_key())
                        #self._frame.add_text("Test", str(self._iteration_pos))
                        self._frame.refresh()
                        self._iteration_pos = i + 1
                        return

    def previous(self):
        pass

    def run(self):
        #itr = self._scale.get_value()
        #while not self.finished.isSet():
        # iterator counter + daten speichern und bei jedem klick auf weiter - next
        #for i in range(self._iteration_pos, int(len(self._simulation_data.markings))):
        for i in range(0, int(len(self._simulation_data.markings))):
            #itr += 1
            #self._scale.set_value(int(itr))
            for j in range(len(self._pn_data.places)):
                #time.sleep(1)
                print self._simulation_data.markings[i]
                if self._simulation_data.markings[i, j] != self._simulation_data.markings[i - 1, j]:
                    #print p.places[j]
                    # path vum vorheriga place zum aktuella place
                    place = self._model.get_data().get_place(self._pn_data.places[j])
                    place.set_marking(int(self._simulation_data.markings[i, j]))
                    # update auch labels!!!
                    if place != None:
                        if self._path_collection != None:
                            for path in self._path_collection:
                                for item in path:
                                    item.set_rgb_edge(0, 0, 0)
                                    self._model.get_data().update(item, item.get_key())

                        self._path_collection = self._model.get_data().get_path(place)
                        
                        if self._path_collection != None:
                            for path in self._path_collection:
                                for item in path:
                                    item.set_rgb_edge(255, 0, 0)
                                    self._model.get_data().update(item, item.get_key())
                    
                print "update"
                #self._model.notify()
                self._frame.refresh()
                time.sleep(1)

if __name__ == "__main__":
    sim = Simulation(None)
    sim.start()
    sim.join()

    
