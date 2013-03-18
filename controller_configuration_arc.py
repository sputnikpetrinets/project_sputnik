#!/usr/bin/python

import model as m
import view_configuration_place as v
import controller_configuration_component as c

import place
import transition

import arc
import test_arc
import inhibitory_arc

class ControllerConfigurationArc(c.ControllerConfigurationComponent):
    """ The ControllerConfigurationArc class is a specific controller that inherits from the general ControllerConfigurationComponent class and is used to manage the user interactions of the configuration window for arcs and the application (ViewConfigurationArc). """

    T_ARC = 0
    T_TEST_ARC = 1
    T_INHIBITORY_ARC = 2

    LT_STRAIGHT = 0
    LT_CURVED_LOWER = 1
    LT_CURVED_UPPER = 2

    _weight = 0
    _arcs = None
    _arc_type = T_ARC
    _arc_line_type = LT_STRAIGHT

    __new_component = None
    _selected_components = None
    _auto_line_type = True

    def __init__(self):
        """ Constructor of ControllerConfigurationPlace. """
        
        # call constructor of parent class
        c.ControllerConfigurationComponent.__init__(self)

        # set default values
        self._weight = 0
        self._arcs = None
        self._arc_type = self.T_ARC
        self._arc_line_type = self.LT_STRAIGHT
        self.__new_component = None
        self._selected_components = None
        self._auto_line_type = True

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerConfigurationPlace. """
        
        # call constructor of parent class
        c.ControllerConfigurationComponent.__init__(self, model, view)

        # set default values
        self._weight = 0
        self._arcs = None
        self._arc_type = self.T_ARC
        self._arc_line_type = self.LT_STRAIGHT
        self.__new_component = None
        self._selected_components = None
        self._auto_line_type = True

    @property
    def arcs(self):
        """ Return list of arcs (Arc-Objects). """
        return self._arcs

    @property
    def arc_type(self):
        """ Return arc type. """
        return self._arc_type
    
    @property
    def arc_line_type(self):
        """ Return line type. """
        return self._arc_line_type

    @property
    def weight(self):
        """ Return weight. """
        return self._weight

    @property
    def selected_components(self):
        """ Return list of selected components (Arc-Objects). """
        return self._selected_components

    @property
    def auto_line_type(self):
        """ Return flag that determines if the line type will be determined automatically. """
        return self._auto_line_type

    @arcs.setter
    def arcs(self, a):
        """ Set list of arcs (Arc-Objects). """
        self._arcs = a

    @arc_type.setter
    def arc_type(self, t):
        """ Set arc type. """
        self._arc_type = t

    @arc_line_type.setter
    def arc_line_type(self, l):
        """ Set line type. """
        self._arc_line_type = l

    @weight.setter
    def weight(self, m):
        """ Set weight. """
        self._weight = int(m)
        if self._weight < 0:
            self._weight *= -1

    @selected_components.setter
    def selected_components(self, comps):
        """ Set selected components (Arc-Objects). """
        self._selected_components = comps

    @auto_line_type.setter
    def auto_line_type(self, state):
        """ Set flag that determines if the line type will be determined automatically. """
        self._auto_line_type = state

    def delete(self):
        """ Delete the selected component from the data core. """
        if self._model != None and self._component != None:
            self._model.create_snapshot()
            val = self._model.data.remove_key(self._component.key)
            self.update_data()
            return val
            #self._model.notify()
        return False

    def get_line_type(self):
        """ Determine automatically which line type should be used to connect two components. """

        # check if a component has been selected
        if self._component != None:
            # check if the selected component is a standard arc
            if type(self._component) == arc.Arc:
                if self._model != None:
                    # check if an opposite arc exists and determine the best choice of the arc type of if 
                    # the same connection already exists the already chosen type will be used
                    for key, item in self._model.data.arcs.items():
                        # check arc type
                        if type(item) == arc.Arc:
                            # check if an arc already exists with the same key
                            if key == self._component.key and key != "new_component" and key != "new_comp" and key != "new component":
                                if item.line_type == arc.Arc.LINE_TYPE_ARC_LOWER:
                                    return self.LT_CURVED_LOWER
                                if item.line_type == arc.Arc.LINE_TYPE_ARC_UPPER:
                                    return self.LT_CURVED_UPPER
                                if item.line_type == arc.Arc.LINE_TYPE_STRAIGHT:
                                    return self.LT_STRAIGHT
                            else:
                            # check if an arc already exists with the same origin and target (if key was changed)
                                if item.target.is_equal(self._component.origin) and item.origin.is_equal(self._component.target):
                                    if item.line_type == arc.Arc.LINE_TYPE_ARC_LOWER:
                                        return self.LT_CURVED_UPPER
                                    if item.line_type == arc.Arc.LINE_TYPE_ARC_UPPER:
                                        return self.LT_CURVED_LOWER
                                    if item.line_type == arc.Arc.LINE_TYPE_STRAIGHT:
                                        if type(self._component.origin) == place.Place:
                                            return self.LT_CURVED_LOWER
                                        else:
                                            return self.LT_CURVED_UPPER
                    return self.LT_STRAIGHT
            # if it is a test arc a fixed line type will be returned
            if type(self._component) == test_arc.TestArc:
                return self.LT_CURVED_LOWER
            # if it is an inhibitory arc a fixed line type will be returned
            if type(self._component) == inhibitory_arc.InhibitoryArc:
                return self.LT_CURVED_UPPER
        return self.LT_STRAIGHT

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """

        # call update method of parent class
        c.ControllerConfigurationComponent.update(self)

        # check arc type and update the correct type of arcs
        if type(self._component) == arc.Arc:
            self._update_arc()
        if type(self._component) == test_arc.TestArc:
            self._update_test_arc()
        if type(self._component) == inhibitory_arc.InhibitoryArc:
            self._update_inhibitory_arc()

        # update the matrices
        self.update_data()

    def cancel(self):
        """ Cancel current view. """
        # remove buffer component
        self._model.data.remove_key("new component")
        # notify all observers
        self._model.notify_component(self._key)

    def _update_arc(self):
        """ Update the current arc and update the functional core. """

        # new component
        self.__new_component = arc.Arc()
        self.__new_component.line_type = arc.Arc.LINE_TYPE_STRAIGHT

        # check if the line type needs to be determined automatically
        if not self._auto_line_type:
            if self._arc_line_type == self.LT_STRAIGHT:
                self.__new_component.line_type = arc.Arc.LINE_TYPE_STRAIGHT
            if self._arc_line_type == self.LT_CURVED_LOWER:
                self.__new_component.line_type = arc.Arc.LINE_TYPE_ARC_LOWER
            if self._arc_line_type == self.LT_CURVED_UPPER:
                self.__new_component.line_type = arc.Arc.LINE_TYPE_ARC_UPPER
        else:
            # determine the line type and assign the correct one to the buffer component
            if self._model != None:
                # check if a similar arc already exists
                for key, item in self._model.data.arcs.items():
                    if type(item) == arc.Arc:
                        if key == self._component.key and key != "new_component" and key != "new_comp" and key != "new component":
                            if item.line_type == arc.Arc.LINE_TYPE_ARC_LOWER:
                                self.__new_component.line_type = arc.Arc.LINE_TYPE_ARC_LOWER
                            if item.line_type == arc.Arc.LINE_TYPE_ARC_UPPER:
                                self.__new_component.line_type = arc.Arc.LINE_TYPE_ARC_UPPER
                            if item.line_type == arc.Arc.LINE_TYPE_STRAIGHT:
                                self.__new_component.line_type = arc.Arc.LINE_TYPE_STRAIGHT
                            break
                        else:
                            if item.target.is_equal(self._component.origin) and item.origin.is_equal(self._component.target):
                                if item.line_type == arc.Arc.LINE_TYPE_ARC_LOWER:
                                    self.__new_component.line_type = arc.Arc.LINE_TYPE_ARC_UPPER
                                if item.line_type == arc.Arc.LINE_TYPE_ARC_UPPER:
                                    self.__new_component.line_type = arc.Arc.LINE_TYPE_ARC_LOWER
                                if item.line_type == arc.Arc.LINE_TYPE_STRAIGHT:
                                    if type(self._component.origin) == place.Place:
                                        self.__new_component.line_type = arc.Arc.LINE_TYPE_ARC_LOWER
                                    else:
                                        self.__new_component.line_type = arc.Arc.LINE_TYPE_ARC_UPPER
                                break

        # remove buffer component
        self._model.data.remove_key("new component")
        # update
        self.__update_component()

    def _update_test_arc(self):
        """ Update test arc and set correct parameters. """

        # instantite TestArc object
        self.__new_component = test_arc.TestArc()
        # set line type
        self.__new_component.line_type = test_arc.TestArc.LINE_TYPE_ARC_LOWER
        if not self._auto_line_type:
            if self._arc_line_type == self.LT_STRAIGHT:
                self.__new_component.line_type = inhibitory_arc.InhibitoryArc.LINE_TYPE_STRAIGHT
            if self._arc_line_type == self.LT_CURVED_LOWER:
                self.__new_component.line_type = inhibitory_arc.InhibitoryArc.LINE_TYPE_ARC_LOWER
            if self._arc_line_type == self.LT_CURVED_UPPER:
                self.__new_component.line_type = inhibitory_arc.InhibitoryArc.LINE_TYPE_ARC_UPPER
        # remove buffer component
        self._model.data.remove_key("new component")
        # update component
        self.__update_component()

    def _update_inhibitory_arc(self):
        """ Update inhibitory arc and set correct parameters. """
        
        # instantiate InhibitoryArc object
        self.__new_component = inhibitory_arc.InhibitoryArc()
        # set line type
        self.__new_component.line_type = inhibitory_arc.InhibitoryArc.LINE_TYPE_ARC_UPPER
        if not self._auto_line_type:
            if self._arc_line_type == self.LT_STRAIGHT:
                self.__new_component.line_type = inhibitory_arc.InhibitoryArc.LINE_TYPE_STRAIGHT
            if self._arc_line_type == self.LT_CURVED_LOWER:
                self.__new_component.line_type = inhibitory_arc.InhibitoryArc.LINE_TYPE_ARC_LOWER
            if self._arc_line_type == self.LT_CURVED_UPPER:
                self.__new_component.line_type = inhibitory_arc.InhibitoryArc.LINE_TYPE_ARC_UPPER
        # remove buffer component
        self._model.data.remove_key("new component")
        # update component
        self.__update_component()

    def __update_component(self):
        """ Update final component. """

        if self._model != None:
            # set properties of the arc
            self.__new_component.key = self._key
            self.__new_component.label = self.label
            self.__new_component.weight = self._weight
            if self._component.origin != None:
                self.__new_component.origin = self._model.data.get_component(self._component.origin.key)
            if self._component.target != None:
                self.__new_component.target = self._model.data.get_component(self._component.target.key)

            if self._component.key == "new component":
                self._model.data.add_arc(self.__new_component)
            else:
                self._model.data.update(self.__new_component, self._component.key)

            # notify all observers
            self._model.notify_component(self.__new_component.key)
