#!/usr/bin/python

import copy

import pygtk
import gtk
import cairo

import place
import transition
import arc
import inhibitory_arc
import test_arc

import petri_net_data

import converter_matrixtostochasticpetrinet
import converter_stochasticpetrinettomatrix

import force_a
import spectral_a

class PetriNet(object):
    """
    The PetriNet class is the central point of this framework and is used for the encapsulation of the framework subparts. Included is a PetriNetData object which holds the petri net specifications in matrix form and the sincle components as individual object which can be drawn onto a surface referenced by a GraphicsContext object.
    """

    def __init__(self):
        """ Constructor of Place and default values will be initialised. """

        # call constructor of parent class
        self._places = dict()
        self._transitions = dict()
        self._arcs = dict()

        self._converter_components = converter_matrixtostochasticpetrinet.ConverterMatrixToStochasticPetriNet()
        self._converter_matrices = converter_stochasticpetrinettomatrix.ConverterStochasticPetriNetToMatrix()

        self._pn_data = petri_net_data.PetriNetData()
        self._prev_pn_data = None

    @property
    def petri_net_data(self):
        """ Return PetriNetData object that contains the petri net specifications in matrix form. """
        return self._pn_data

    @petri_net_data.setter
    def petri_net_data(self, data):
        """ Set PetriNetData object that contains the petri net specifications in matrix form. """
        self._pn_data = data

    @property
    def converter_components(self):
        """ Return the converter for creating the components out of the petri net specifications in matrix form from the PetriNetData object. """
        return self._converter_components

    @converter_components.setter
    def converter_components(self, converter):
        """ Set the converter for creating the components out of the petri net specifications in matrix form from the PetriNetData object. """
        self._converter_components = converter

    @property
    def converter_matrices(self):
        """ Return the converter for creating the PetriNetData object out of the component dictionaries containing the individual component types (places, transitions and arcs). """
        return self._converter_matrices

    @converter_matrices.setter
    def converter_matrices(self, converter):
        """ Set the converter for creating the PetriNetData object out of the component dictionaries containing the individual component types (places, transitions and arcs). """
        self._converter_matrices = converter

    @property
    def places(self):
        """ Return dictionary of places (dictionary key is the key of the component). """
        return self._places

    @places.setter
    def places(self, data):
        """ Set dictionary of places (dictionary key is the key of the component). """
        self._places = data

    @property
    def transitions(self):
        """ Return dictionary of transitions (dictionary key is the key of the component). """
        return self._transitions

    @transitions.setter
    def transitions(self, data):
        """ Set dictionary of transitions (dictionary key is the key of the component). """
        self._transitions = data

    @property
    def arcs(self):
        """ Return dictionary of arcs (dictionary key is the key of the component). """
        return self._arcs

    @arcs.setter
    def arcs(self, data):
        """ Set dictionary of arcs (dictionary key is the key of the component). """
        self._arcs = data

    def add(self, component):
        """ Add a new component to the petri net. It is not necessary to define the component type because it will be determined automatically. TRUE will be returned if the component could be added and otherwise FALSE. """
        # check if component is valid
        if component == None:
            return False
        # according to the object type the component will be added
        if type(component) == place.Place:
            return self.add_place(component)
        if type(component) == transition.Transition:
            return self.add_transition(component)
        if type(component) == arc.Arc or type(component) == inhibitory_arc.InhibitoryArc or type(component) == test_arc.TestArc:
            return self.add_arc(component)
        return False

    def add_place(self, component):
        """ Add a new place to the petri net. TRUE will be returned if the component could be added and otherwise FALSE. """
        # check if component is valid
        if component == None:
            return False
        # check if key is valid
        if component.key != "" and not self._places.has_key(component.key):
            # check object type
            if type(component) == place.Place:
                # add place
                self._places[component.key] = component
                return True
        return False

    def add_transition(self, component):
        """ Add a new transition to the petri net. TRUE will be returned if the component could be added and otherwise FALSE. """
        # check if component is valid
        if component == None:
            return False
        # check if key is valid
        if component.key != "" and not self._transitions.has_key(component.key):
            # check object type
            if type(component) == transition.Transition:
                # add transition
                self._transitions[component.key] = component
                return True
        return False

    def add_arc(self, component):
        """ Add a new arc to the petri net. TRUE will be returned if the component could be added and otherwise FALSE. """
        # check if component is valid
        if component == None:
            return False
        # check if key is valid
        if component.key != "" and not self._arcs.has_key(component.key):
            # check object type
            if type(component) == arc.Arc or type(component) == inhibitory_arc.InhibitoryArc or type(component) == test_arc.TestArc:
                # add arc
                self._arcs[component.key] = component
                return True
        return False

    def update(self, component, key):
        """ Update an existing component or the petri net. It is not necessary to define the component type because it will be determined automatically. TRUE will be returned if the component could be updated and otherwise FALSE. """
        # check if component is valid
        if component == None:
            return False
        # update component according to its object type
        if type(component) == place.Place:
            return self.update_place(component, key)
        if type(component) == transition.Transition:
            return self.update_transition(component, key)
        if type(component) == arc.Arc or type(component) == inhibitory_arc.InhibitoryArc or type(component) == test_arc.TestArc:
            return self.update_arc(component, key)
        return False

    def update_place(self, component, key):
        """ Add an existing place of the petri net. TRUE will be returned if the component could be updated and otherwise FALSE. """
        # check if component is valid
        if component == None:
            return False
        # check if key is valid
        if key != "" and self._places.has_key(key):
            # check object type
            if type(component) == place.Place:
                # update
                self._places[key] = component
                return True
        return False

    def update_transition(self, component, key):
        """ Add an existing transition of the petri net. TRUE will be returned if the component could be updated and otherwise FALSE. """
        # check if component is valid
        if component == None:
            return False
        # check if key is valid
        if key != "" and self._transitions.has_key(key):
            # check object type
            if type(component) == transition.Transition:
                # update
                self._transitions[key] = component
                return True
        return False

    def update_arc(self, component, key):
        """ Add an existing arc of the petri net. TRUE will be returned if the component could be updated and otherwise FALSE. """
        # check if component is valid
        if component == None:
            return False
        # check if key is valid
        if key != "" and self._arcs.has_key(key):
            # check object type
            if type(component) == arc.Arc  or type(component) == inhibitory_arc.InhibitoryArc or type(component) == test_arc.TestArc:
                # update
                self._arcs[key].key = component.key
                self._arcs[key].label = component.label
                self._arcs[key].weight = component.weight
                self._arcs[key].line_type = component.line_type
                self._arcs[key].description = component.description
                self._arcs[key].font_label = component.font_label
                self._arcs[key].font_weight = component.font_weight
                return True
        return False

    def remove_place(self, component):
        """ Remove an existing place of the petri net. TRUE will be returned if the component could be removed and otherwise FALSE. """
        # check if component is valid
        if component != None:
            # check object type
            if type(component) == place.Place:
                # remove place
                del self._places[component.key]
                return True
        return False

    def remove_transition(self, component):
        """ Remove an existing transition of the petri net. TRUE will be returned if the component could be removed and otherwise FALSE. """
        # check if component is valid
        if component != None:
            # check object type
            if type(component) == transition.Transition:
                # remove transition
                del self._transitions[component.key]
                return True
        return False

    def remove_arc(self, component):
        """ Remove an existing arc of the petri net. TRUE will be returned if the component could be removed and otherwise FALSE. """
        # check if component is valid
        if component != None:
            # check object type
            if type(component) == arc.Arc or type(component) == inhibitory_arc.InhibitoryArc or type(component) == test_arc.TestArc:
                # remove arc
                del self._arcs[component.key]
                return True
        return False
    
    def remove(self, components):
        """ Remove a list of existing components of the petri net. It will be determined automatically from which dictionary the component needs to be removed. TRUE will be returned if the component could be removed and otherwise FALSE. """
        del_comp = True
        # remove all arcs from the list if one of its components will be removed (origin or target)
        for comp in components:
            # go through the available arcs
            for key, item in self._arcs.items():
                try:
                    # check if the arc should be removed because its origin will be removed
                    if item.origin.key == comp.key:
                        # remove arc
                        self.remove_arc(item)
                except TypeError:
                    del_comp = False
                try:
                    # check if the arc should be removed because its target will be removed
                    if item.target.key == comp.key:
                        # remove arc
                        self.remove_arc(item)
                except TypeError:
                    del_comp = False
            
        # remove all places and transitions
        for comp in components:
            # check the object type
            if type(comp) == place.Place:
                # remove place
                self.remove_place(comp)
            else:
                # check object type
                if type(comp) == transition.Transition:
                    # remov transition
                    self.remove_transition(comp)
                else:
                    # check object type
                    if type(component) != arc.Arc and type(component) != inhibitory_arc.InhibitoryArc and type(component) != test_arc.TestArc:
                        del_comp = False
        
        return del_comp

    def remove_place_key(self, key):
        """ Remove an existing place of the petri net according to its key. TRUE will be returned if the component could be removed and otherwise FALSE. """
        # check if key is valid
        if key != "" and self._places.has_key(key):
            # remove place
            del self._places[key]
            return True
        return False

    def remove_transition_key(self, key):
        """ Remove an existing transition of the petri net according to its key. TRUE will be returned if the component could be removed and otherwise FALSE. """
        # check if key is valid
        if key != "" and self._transitions.has_key(key):
            # remove transition
            del self._transitions[key]
            return True
        return False

    def remove_arc_key(self, key):
        """ Remove an existing arc of the petri net according to its key. TRUE will be returned if the component could be removed and otherwise FALSE. """
        # check if key is valid
        if key != "" and self._arcs.has_key(key):
            # remove arc
            del self._arcs[key]
            return True
        return False

    def remove_key(self, key):
        """ Remove an existing component of the petri net according to its key. It will be determined automatically from which dictionary the component needs to be removed. TRUE will be returned if the component could be removed and otherwise FALSE. """
        # check if key is valid
        if key != "":
            # according to the key it will be determined which list contains this key and the component will be removed
            if self._places.has_key(key):
                return self.remove_place_key(key)
            if self._transitions.has_key(key):
                return self.remove_transition_key(key)
            if self._arcs.has_key(key):
                return self.remove_arc_key(key)
        return False

    def has_key(self, key):
        """ Check if the key defines already a component. TRUE will be returned if the key is already reserved. """
        if self._places.has_key(key):
            return True
        if self._transitions.has_key(key):
            return True
        if self._arcs.has_key(key):
            return True
        return False

    def has_label(self, label):
        """ Check if the label defines already a component. TRUE will be returned if the key is already reserved. """
        for key, value in self._places.items():
            if value.label == label:
                return True
        for key, value in self._transitions.items():
            if value.label == label:
                return True
        for key, value in self._transitions.items():
            if value.label == label:
                return True
        return False

    def get_place(self, key):
        """ Return a place according to the defined key and if it cannot be found None will be returned. """
        # check if key is valid
        if key != "" and self._places.has_key(key):
            # return place
            return self._places[key]
        return None

    def get_transition(self, key):
        """ Return a transition according to the defined key and if it cannot be found None will be returned. """
        # check if key is valid
        if key != "" and self._transitions.has_key(key):
            # return transition
            return self._transitions[key]
        return None

    def get_arc(self, key):
        """ Return an arc according to the defined key and if it cannot be found None will be returned. """
        # check if arc is valid
        if key != "" and self._arcs.has_key(key):
            # return arc
            return self._arcs[key]
        return None

    def get_component(self, key):
        """ Return a component (place, transition or arc) according to the defined key and if it cannot be found None will be returned. """
        component = self.get_place(key)
        if component == None:
            component = self.get_transition(key)
        if component == None:
            component = self.get_arc(key)
        return component

    # abstaende muessand ou no beruecksichtigt wera!
    def get_nearest_component(self, position):
        """ Determine which component is the nearest to the define position (x- and y-dimension) under regarding of a virtual buffer/tolerance zone around the components that the user does not have to define exactly a position within the component. If no component can be identified None will be returned. """

        # the minimal distance to a component
        comp_dist = -1
        # the nearest component
        comp = None

        # the buffer zone around a place is 10
        # check if the nearest component is a place
        for key, value in self._places.items():
            # calculate distance - Manhattan Distance is used
            dist = abs(value.position[0] - position[0]) + abs(value.position[1] - position[1])
            # check if the current component is nearer than the previous one
            if dist < comp_dist or comp_dist == -1:
                # check if the position is within the buffer zone
                if position[0] < value.position[0] + value.radius + 10 and position[0] > value.position[0] - value.radius - 10 and position[1] < value.position[1] + value.radius + 10 and position[1] > value.position[1] - value.radius - 10:
                    # select current component
                    comp_dist = dist
                    comp = self._places[key]

        # the buffer zone around a transition is 10
        # check if the nearest component is a transition
        for key, value in self._transitions.items():
            # calculate distance - Manhattan Distance is used
            dist = abs(value.position[0] - position[0]) + abs(value.position[1] - position[1])
            # check if the current component is nearer than the previous one
            if dist < comp_dist or comp_dist == -1:
                # check if the position is within the buffer zone
                if position[0] < value.position[0] + value.dimension[0] + 10 and position[0] > value.position[0] - value.dimension[0] - 10 and position[1] < value.position[1] + value.dimension[1] + 10 and position[1] > value.position[1] - value.dimension[1]- 10:
                    # select current component
                    comp_dist = dist
                    comp = self._transitions[key]

        # return last selected component
        return comp

    def get_selected_arcs(self, position):
        """ Based on a simple linear equation it will be determined if the defined position (x- and y-dimension) is on a virtual connection between two components and all of the arcs connecting these two components will be returned. A buffer/tolerance zone will be regarded too and the postion does not need to be exactly on the virtual connection. If no arcs can be identified an empty list will be returned. """

        # list that contains the selected arcs
        l_arcs = []
        
        # iteration through all available arcs
        for key, value in self._arcs.items():

            # corners of the rectangle
            left_upper = [0, 0]
            right_lower = [0, 0]

            try:
                # get start- and end-position of the components which are connected through the current arc
                comp_1 = value.origin.position
                comp_2 = value.target.position

                # determine the corners of the virtual rectangle created throught the two components
                if comp_1[0] > comp_2[0]:
                    right_lower[0] = comp_1[0]
                    left_upper[0] = comp_2[0]
                else:
                    right_lower[0] = comp_2[0]
                    left_upper[0] = comp_1[0]
                if comp_1[1] > comp_2[1]:
                    right_lower[1] = comp_1[1]
                    left_upper[1] = comp_2[1]
                else:
                    right_lower[1] = comp_2[1]
                    left_upper[1] = comp_1[1]

                # check if position is within the rectangle - saves exact calculations if it is not
                if position[0] < right_lower[0] and position[0] > left_upper[0] and position[1] < right_lower[1] and position[1] > left_upper[1]:
                    # determine if the position is on the virtual line (a bufferzone will be regarded)
                    if self.__is_on_virtual_line(position, value.origin.position, value.target.position):
                        # the arc is selected through the defined position
                        l_arcs.append(self._arcs[key])
            except AttributeError:
                # next iteration
                next
        
        # return list of arcs
        return l_arcs

    # dahoam muass i des no fertig macha
    # verwenda vu da normala kx plus gleichung
    def __is_on_virtual_line(self, position, start_position, end_position):
        """ Check if a position is on a virtual line between the start- and end-position under regarding a buffer/tolerance zone around the line. If the position is on the line TRUE will be returned and otherwise FALSE. """

        # difference between end- and start-position in x-dimension
        dx = float(int(end_position[0] - start_position[0]))
        # difference between end- and start-position in y-dimension
        dy = float(int(end_position[1] - start_position[1]))
        # calculate elements for a linear equation
        k = float(dy/dx)
        d = start_position[1] - k * int(start_position[0])
        # define start- and end-position in x-dimension to determine the y values of the linear equation (virtual connection)
        start = start_position[0]
        end = end_position[0]
        if end_position[0] < start_position[0]:
            start = end_position[0]
            end = start_position[0]
        # iteration through all possible x-values between the start- and end-position
        for i in range(int(start), int(end)):
            # y value of the linear equation
            y = k * i + d
            # check if the position is within the defined buffer zone
            if position[0] >= i - 25 and position[0] <= i + 25 and position[1] >= y - 25 and position[1] <= y + 25:
                return True
        return False

    def get_selected_components_without_arcs(self, start_position, end_position):
        """ Determine all components except arc within a rectangular area defined through a start- and end-position. If components are included a list with those will be returned and otherwise an empty list. """

        # list of selected components 
        components = []

        # change start- and end-position if necessary
        for i in range(len(start_position)):
            if start_position[i] > end_position[i]:
                h = end_position[i]
                end_position[i] = start_position[i]
                start_position[i] = h

        # determine the places which are lying within the rectangle
        for key, value in self._places.items():
            # check if the place lies within the defined rectangle
            if value.position[0] >= start_position[0] and value.position[0] <= end_position[0] and value.position[1] >= start_position[1] and value.position[1] <= end_position[1]:
                # select component
                components.append(value)

        # determine the transitions which are lying within the rectangle
        for key, value in self._transitions.items():
            # check if the transition lies within the defined rectangle
            if value.position[0] >= start_position[0] and value.position[0] <= end_position[0] and value.position[1] >= start_position[1] and value.position[1] <= end_position[1]:
                # select component
                components.append(value)

        # return selected components
        return components

    def get_selected_components_with_arcs(self, start_position, end_position):
        """ Determine all components within a rectangular area defined through a start- and end-position. An arc will only be added if its origin and target are also within the defined area. If components are included a list with those will be returned and otherwise an empty list. """

        components = []
        tolerance = 20
        tolerance_place = 10

        for i in range(len(start_position)):
            if start_position[i] > end_position[i]:
                h = end_position[i]
                end_position[i] = start_position[i]
                start_position[i] = h

        # radius plus 10
        for key, value in self._places.items():
            if value.position[0] >= start_position[0] - value.radius - tolerance_place and value.position[0] <= end_position[0] + value.radius + tolerance_place and value.position[1] >= start_position[1] - value.radius - tolerance_place and value.position[1] <= end_position[1] + value.radius + tolerance_place:
                components.append(value)

        # surrounding plus 10
        for key, value in self._transitions.items():
            if value.position[0] >= start_position[0] and value.position[0] <= end_position[0] and value.position[1] >= start_position[1] and value.position[1] <= end_position[1]:
                components.append(value)

        for key, value in self._arcs.items():
            # origin and target has to be within the defined area
            origin = False
            target = False
            for i in range(len(components)):
                if value.origin.is_equal(components[i]):
                    origin = True
                if value.target.is_equal(components[i]):
                    target = True
            if origin and target:
                components.append(value)

        return components

    def get_positions(self):
        """ Create a dictionary which also will be returned containing all positions of each component. The key of the dictionary is the key of the component. """
        
        # dictionary that stores positions of the components
        pos = dict()
        # read the positions of the places
        for key, value in self._places.items():
            pos[value.key] = value.position
        # read the positions of the transitions
        for key, value in self._transitions.items():
            pos[value.key] = value.position
        
        return pos

    def set_positions(self, positions):
        """ Set the positions of the single components. The key of the dictionary positions is the key of the components. """

        # iteration through all positions
        for key, value in positions.items():
            # read component
            component = self.get_component(key)
            # check if component could be read
            if component != None:
                # assign position
                component.position = value
                # update component
                self.update(component, key)

    def draw(self, ctx):
        """ Draw the components onto the defined GraphicsContext ctx. """

        ctx.set_source_rgb(1., 1., 1.)
        ctx.paint()

        # draw the places onto the referenced surface
        for key, item in self._places.items():
            item.draw(ctx)

        # draw the transitions onto the referenced surface
        for key, item in self._transitions.items():
            item.draw(ctx)

        # draw the arcs onto the referenced surface
        for key, item in self._arcs.items():
            item.draw(ctx)

        ctx.stroke()
        ctx.clip()

    def zoom(self, factor):
        """ Scale the components by a given factor. """

        # scale all places
        for key, value in self._places.items():
            self._places[key].zoom(factor)
        # scale all transitions
        for key, value in self._transitions.items():
            self._transitions[key].zoom(factor)

    def get_detailed_paths(self, transition_component = None):
        """ Determine the paths which are used for a transition to fire and only standard arcs will be regarded. """

        # multi-dimensional list that contains all possible paths from the origin to the target component via the defined tarnsition
        path_collection = []
        # check if an origin and target are defined

        # read input arcs of the target
        inputs = self.get_input_arcs(transition_component)

        # list that stores the current path
        path = []        

        # iteration through the input arcs
        for input_arc in inputs:
            # check the arc type (only standard arcs are allowed)
            if type(input_arc) == arc.Arc:
                # attach target
                path.append(transition_component)
                # check if origin of the component is the defined transition
                if input_arc.origin != None: #and input_arc.origin.key == transition_component.key:
                    # attach arc and origin
                    path.append(input_arc)
                    path.append(input_arc.origin)
                    path.append(input_arc.target)

                # attach path to the list of possible paths
                #path_collection.append(path)


        outputs = self.get_output_arcs(transition_component)

        # iteration through the input arcs
        for output_arc in outputs:
            # check the arc type (only standard arcs are allowed)
            if type(output_arc) == arc.Arc:
                # attach target
                path.append(transition_component)
                # check if origin of the component is the defined transition
                if output_arc.origin != None:# and output_arc.origin.key == transition_component.key:
                    # attach arc and origin
                    path.append(output_arc)
                    path.append(output_arc.origin)
                    path.append(output_arc.target)

        # attach path to the list of possible paths
        path_collection.append(path)

        # return determined paths
        return path_collection

    def get_detailed_path(self, target_component = None, transition_component = None, origin_component = None):
        """ Determine the path from an origin place to a target place via a transition. Only standard arcs will be regarded and at least a target or origin place with a transition need to be defined otherwise the input is invalid and no path can be determined. A multidimensional array with valid paths will be returned. Dimension one describes the different paths and the second dimension the components of each path. """

        # multi-dimensional list that contains all possible paths from the origin to the target component via the defined tarnsition
        path_collection = []
        # check if an origin and target are defined
        if target_component != None and origin_component != None:
            # read input arcs of the target
            inputs = self.get_input_arcs(target_component)
            # iteration through the input arcs
            for input_arc in inputs:
                # list that stores the current path
                path = []
                # check the arc type (only standard arcs are allowed)
                if type(input_arc) == arc.Arc:
                    # attach target
                    path.append(target_component)
                    # check if origin of the component is the defined transition
                    if input_arc.origin != None and input_arc.origin.key == transition_component.key:
                        # attach arc and origin
                        path.append(input_arc)
                        path.append(input_arc.origin)
                        # read input arcs of the origin
                        inputs_origin = self.get_input_arcs(input_arc.origin)
                        # iteration through the input arcs of the origin which is the defined transition
                        for input_arc_origin in inputs_origin:
                            # check the arc type (only standard arcs are allowed)
                            if type(input_arc_origin) == arc.Arc:
                                # check if the origin (place) is equal the defined one
                                if input_arc_origin.origin.is_equal(origin_component):
                                    # attach arc and origin to the path
                                    path.append(input_arc_origin)
                                    path.append(input_arc_origin.origin)
                    # attach path to the list of possible paths
                    path_collection.append(path)
        # check if a target is defined but not an origin component
        if target_component != None and origin_component == None:
            # read input arcs of the target
            inputs = self.get_input_arcs(target_component)
            # iteration through the input arcs
            for input_arc in inputs:
                # list that stores the current path
                path = []
                # check the arc type (only standard arcs are allowed)
                if type(input_arc) == arc.Arc:
                    # attach target
                    path.append(target_component)
                    # check if origin of the component is the defined transition
                    if input_arc.origin != None and input_arc.origin.key == transition_component.key:
                        #attach arc and origin
                        path.append(input_arc)
                        path.append(input_arc.origin)
                        # read input arcs of the origin
                        inputs_origin = self.get_input_arcs(input_arc.origin)
                        # iteration through the input arcs of the origin which is the defined transition
                        for input_arc_origin in inputs_origin:
                            # check the arc type (only standard arcs are allowed)
                            if type(input_arc_origin) == arc.Arc:
                                # check if the origin of the arc is the target again (loop over transition to the same place again)
                                if input_arc_origin.origin.is_equal(target_component):
                                    # attach arc and origin to the path
                                    path.append(input_arc_origin)
                                    path.append(input_arc_origin.origin)
                    # attach path to the list of possible paths
                    path_collection.append(path)
        
        # check if an origin but no target component are defined
        if target_component == None and origin_component != None:
            # read output arcs of the target
            outputs = self.get_output_arcs(origin_component)
            # iteration through the output arcs
            for output_arc in outputs:
                # list that stores the current path
                path = []
                # check the arc type (only standard arcs are allowed)
                if type(output_arc) == arc.Arc:
                    # attach origin
                    path.append(origin_component)
                    # check if origin of the arc is defined
                    if output_arc.origin != None:
                        # read output arcs of the target of the arc
                        outputs_target = self.get_output_arcs(output_arc.target)
                        # check if the target component does not have any output arcs (connection from place to transition and not further)
                        if outputs_target == None or len(outputs_target) == 0:
                            # attach arc and origin to the path
                            path.append(output_arc)
                            path.append(output_arc.origin)
                    # attach path to the list of possible paths
                    path_collection.append(path)

        # return determined paths
        return path_collection

    def get_input_arcs(self, component, weight = None):
        """ Determine the input arcs of a component and a list containing those will be returned. The weight parameter is optional and if it is defined only input arcs with the defined weight will be regarded. If the defined component does not have any an empty list will be returned. """

        # list of input arcs
        inputs = []
        # iteration through all arcs
        for key, value in self._arcs.items():
            # check if the target component is equal to the defined one
            if component.is_equal(value.target):
                # check if a weight is defined
                if weight != None:
                    # check if the weights are equal
                    if value.weight == weight:
                        # attach arc to the list of input arcs
                        inputs.append(value)
                else:
                    # attach arcs to the list of input arcs
                    inputs.append(value)
                
        # return list of input arcs
        return inputs

    def get_output_arcs(self, component, weight = None):
        """ Determine the output arcs of a component and a list containing those will be returned. The weight parameter is optional and if it is defined only output arcs with the defined weight will be regarded. If the defined component does not have any an empty list will be returned. """

        # list of output arcs
        outputs = []
        # iteration through all arcs
        for key, value in self._arcs.items():
            # check if the origin component is equal to the defined one
            if component.is_equal(value.origin):
                # check if a weight is defined
                if weight != None:
                    # check if the weights are equal
                    if value.weight == weight:
                        # attach arc to the list of output arcs
                        outputs.append(value)
                else:
                    # attach arc to the list of output arcs
                    outputs.append(value)

        # return list of output arcs
        return outputs

#    def valid_connection_old(self, component): 
#        """ Return TRUE if a connection defined through an arc component is valid. """
#        if type(component) == arc.Arc or type(component) == test_arc.TestArc or type(component) == inhibitory_arc.InhibitoryArc:
#            if (type(component.origin) == place.Place and type(component.target) == transition.Transition) or (type(component.origin) == transition.Transition and type(component.target) == place.Place):
#                for key, value in self._arcs.items():
#                    if type(component) == type(value) and not value.key == "new_comp":
#                        if component.origin.is_equal(value.origin) and component.target.is_equal(value.target):
#                            return False
#                return True
#        return False

    def valid_connection(self, component): 
        """ Return TRUE if a connection defined through an arc component is valid. """

        # check the object type
        if type(component) == arc.Arc:
            # check if the origin and target are correct defined
            if (type(component.origin) == place.Place and type(component.target) == transition.Transition) or (type(component.origin) == transition.Transition and type(component.target) == place.Place):
                # iteration through all arcs to check if an arc with the same key already exists
                for key, value in self._arcs.items():
                    if type(component) == type(value) and not value.key == "new_comp":
                        if component.origin.is_equal(value.origin) and component.target.is_equal(value.target):
                            return False
                return True
        else:
            # check the object type
             if type(component) == test_arc.TestArc or type(component) == inhibitory_arc.InhibitoryArc:
                 # test and inhibitory arcs can only be connected from a place to a transition
                 if (type(component.origin) == place.Place and type(component.target) == transition.Transition):
                     # iteration through all arcs to check if an arc with the same key already exists
                     for key, value in self._arcs.items():
                         if type(component) == type(value) and not value.key == "new_comp":
                             if component.origin.is_equal(value.origin) and component.target.is_equal(value.target):
                                 return False
                     return True
        return False

    def convert_components(self, position = None):
        """ Based on the defined PetriNetData object, which contains the petri net specifications in matrix form, the single components will be created and automatically assigned to the dictionaries. """

        # reset the dictionaries
        self._places = dict()
        self._transitions = dict()
        self._arcs = dict()
        # set data for the converter
        self._converter_components.data = self._pn_data
        # convert
        self._converter_components.convert()
        # assign new components
        self._places = self._converter_components.places
        self._transitions = self._converter_components.transitions
        # arcs cannot be assigned directly
        self._arcs = dict()
        arcs = self._converter_components.arcs

        # need to be recreated otherwise a problem with references occurres
        for key, item in arcs.items():
            # arc component
            a = None
            # check object type an instantiate an object of the correct class
            if type(item) == arc.Arc:
                a = arc.Arc()
            if type(item) == test_arc.TestArc:
                a = test_arc.TestArc()
            if type(item) == inhibitory_arc.InhibitoryArc:
                a = inhibitory_arc.InhibitoryArc()
            # check if an object could be created
            if a != None:
                # set properties
                a.key = item.key
                a.label = item.label
                a.weight = item.weight
                a.line_type = item.line_type
                a.font_weight = item.font_weight
                a.font_label = item.font_label
                if item.target != None:
                    a.target = self.get_component(item.target.key)
                if item.origin != None:
                    a.origin = self.get_component(item.origin.key)
                # add arc
                self.add_arc(a)

        # check if positions are defined
        if position != None:
            # iteration through all positions
            self.set_positions(position)
        else:
            # instantiate layout object
            v = force_a.ForceDirected()
            # set data
            v.petri_net = self.petri_net_data.clone()
            v.get_petri_net()
            # set default parameter
            v.width = 900
            v.height = 600
            v.border = 100
            v.grid_size = 50
            v.iterations = 1
            # calculate positions
            v.calculate()
            # read positions
            self.set_positions(v.node_positions)
            

    def convert_matrices(self):
        """ Based on the defined components a PetriNetData object will be created and overwrites the existing one. """
        # set data
        self._converter_matrices.data = self
        # convert
        self._converter_matrices.convert()
        # set output data
        self._pn_data = self._converter_matrices.converted_data

    def create_petri_net_data_backup(self):
        """ Creates a backup of the current PetriNetData object. Only one backup can be stored. """
        self._prev_pn_data = self._pn_data.clone()

    def reset(self):
        """ Restore the previous markings. """
        for i in range(len(self._prev_pn_data.places)):
            for key, item in self._places.items():
                if item.label == self._prev_pn_data.places[i]:
                    self._places[key].marking = self._prev_pn_data.initial_marking[i]
