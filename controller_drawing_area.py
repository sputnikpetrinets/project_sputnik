#!/usr/bin/python

import math

import pygtk
import gtk
import cairo

import model as m
import view_main as v
import controller as c

import petri_net

import place
import transition
import arc
import test_arc
import inhibitory_arc

import view_configuration_place
import view_configuration_transition
import view_configuration_arc
import view_layout
import view_petri_net_export
import view_configuration_simulation_diagram
import view_configuration_token_game_animation
import controller_configuration_place
import controller_configuration_transition
import controller_configuration_arc
import controller_layout
import controller_petri_net_export
import controller_configuration_token_game_animation
import controller_configuration_simulation_diagram

#import converter_matrixtostochasticpetrinet
#import calculatevisualisation as vis

class ControllerDrawingArea(c.Controller):
    """ The ControllerDrawingArea class is a specific controller that inherits from the general Controller class and is used to manage the user interactions of the drawing area of the application (ViewDrawingArea). """

    _config_mouse = False
    _ctrl_status = False
    _start_pos = None
    _end_pos = None
    _orig_pos = None
    _centered_pos = None
    _pressed = False
    _started = False
    _select = True
    _paste = False
    _selected = False
    _multi_select = False
    _move_items = False
    _arc_selection = False
    _zoom = False
    _lock_components = False
    _add_component = False
    _iteration_pos = 1
    _ctrl = False
#    _c = False
#    _v = False
#    _d = False
#    _z = False
#    _plus = False
#    _minus = False

    _play = False
    _pause = False
    _add_component = False
    _lock = False
    _component = None
    _selected_components = None
    _copied_components = None
    _drawing_area = None
    _paste_dict = dict()
    _width = 900
    _height = 600

    def __init__(self):
        """ Constructor of ControllerDrawingArea. """
        
        # call constructor of parent class
        c.Controller.__init__(self)
        #self._frame = None

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerDrawingArea. """
        
        # call constructor of parent class
        c.Controller.__init__(self, model, view)
        #self._frame = None

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """
        self.refresh()

    def update_component(self, key):
        """ Interface to notify Observer objects about a data change of a component. """
        self.refresh()

    def update_output(self):
        """ Interface to notify Observer objects about a data change of simulation results. """
        self.refresh()

    def reset(self):
        """ Interface to notify MVCObserver objects about a reset event. """
        self.reset()

    def undo(self):
        """ Interface to notify Observer objects about an undo. """
        self.refresh()

    @property
    def ctrl_key(self):
        """ Return flag for a pressed Ctrl key. """
        return self._ctrl

    @property
    def lock(self):
        """ Return flag for locking the screen. """
        return self._lock

    @property
    def drawing_area(self):
        """ Return DrawingArea-Object. """
        return self._drawing_area

    @drawing_area.setter
    def drawing_area(self, d):
        """ Set DrawingArea-Object. """
        self._drawing_area = d

    @ctrl_key.setter
    def ctrl_key(self, status):
        """ Set flag for pressing the Ctrl key. """
        self._ctrl = status

    @lock.setter
    def lock(self, status):
        """ Set flag for locking the screen. """
        self._lock = status
        self._select = not self._lock

    def copy(self):
        """ Selected components will be copied and placed at the same positions as the original ones. """

        # matching dictionary to connect to new created components with each other
        self._paste_dict = dict()

        # copy the selected components
        self._copied_components = None
        # check if a single component needs to be copied
        if self._component != None:
            self._copied_components = []
            self._copied_components.append(self.copy_component(self._component))
        # check if multiple components need to be copied
        if self._selected_components != None:
            self._copied_components = []
            # iteration through all selected components
            for i in range(len(self._selected_components)):
                if type(self._selected_components[i]) == place.Place or type(self._selected_components[i]) == transition.Transition:
                    self._copied_components.append(self.copy_component(self._selected_components[i]))
                    self._paste_dict[self._copied_components[len(self._copied_components) - 1].key] = self._selected_components[i].key

        # calculate centre which is used as the mouse position for pasting the components
        if self._copied_components != None:
            # determine minimal and maximal coordinates in each dimension
            min_pos = [0, 0]
            max_pos = [0, 0]
            if len(self._copied_components) > 0:
                min_pos = [self._copied_components[0].position[0], self._copied_components[0].position[1]]
                max_pos = [self._copied_components[0].position[0], self._copied_components[0].position[1]]
            for i in range(len(self._copied_components)):
                if type(self._copied_components[i]) == place.Place or type(self._copied_components[i]) == transition.Transition:
                    if min_pos[0] > self._copied_components[i].position[0]:
                        min_pos[0] = self._copied_components[i].position[0]
                    if min_pos[1] > self._copied_components[i].position[1]:
                        min_pos[1] = self._copied_components[i].position[1]
                    if max_pos[0] < self._copied_components[i].position[0]:
                        max_pos[0] = self._copied_components[i].position[0]
                    if max_pos[0] < self._copied_components[i].position[1]:
                        max_pos[0] = self._copied_components[i].position[1]
            # determine centre
            self._centered_pos = [int((max_pos[0] + min_pos[0]) / 2), int((max_pos[1] + min_pos[1]) / 2)]

    def copy_component(self, component):
        """ Copy the defined component and a not yet existing name will be assigned to the copied component. """

        # clone component
        clone = component.clone()
        key = component.key
        # check if key is already used
        if self._model.data.has_key(key + " (copy)"):
            # use a counter to define a not existing key for the copied component
            ctr = 1
            loop = True
            # iteration until a not existing key can be found
            while loop:
                if self._model.data.has_key(key + " (copy " + str(ctr) + ")"):
                    ctr += 1
                else:
                    # abort loop
                    loop = False
                    # assign label and key
                    clone.key = key + " (copy " + str(ctr) + ")"
                    clone.label = clone.label + " (copy " + str(ctr) + ")"
        else:
            # assign label and key
            clone.key = key + " (copy)"
            clone.label = clone.label + "(copy)"
        return clone

    def paste(self):
        """ Paste the copied components onto the drawing area. """

        # create a snapshot
        self._model.create_snapshot()
        
        # set flags and object values
        self._selected_components = None
        self._component = None
        self._multi_select = False
        self._move_items = False
        self._paste = True

        # iteration through all copied components and add them to the core data except arcs
        for i in range(len(self._copied_components)):
            if type(self._copied_components[i]) == place.Place or type(self._copied_components[i]) == transition.Transition:
                # add component to the core data
                self._model.data.add(self._copied_components[i])

        # dictionary of arcs
        arcs = self._model.data.arcs
        # iteration through all available arcs
        for key, item in arcs.items():
            # check if both parties of the current arc are part of the copied components
            origin = False
            target = False
            key_origin = ""
            key_target = ""
            # iteration through all copied components
            for clone_key, orig_key in self._paste_dict.items():
                if item.origin.key == orig_key:
                    origin = True
                    key_origin = clone_key
                if item.target.key == orig_key:
                    target = True
                    key_target = clone_key
            # check if both parties of an arc could be identified
            if origin and target:
                # add arc
                # reference issue - recreation of the arc component is necessary
                new_item_properties = self.copy_component(item)
                new_arc = None
                if type(item) == arc.Arc:
                    new_arc = arc.Arc()
                if type(item) == inhibitory_arc.InhibitoryArc:
                    new_arc = inhibitory_arc.InhibitoryArc()
                if type(item) == test_arc.TestArc:
                    new_arc = inhibitory_arc.InhibitoryArc()
                if new_arc != None:
                    new_arc.line_type = new_item_properties.line_type
                    new_arc.label = new_item_properties.label
                    new_arc.key = new_item_properties.key
                    new_arc.origin = self._model.data.get_component(key_origin)
                    new_arc.target = self._model.data.get_component(key_target)
                    new_arc.weight = new_item_properties.weight
                    # add arc to the core data
                    self._model.data.add(new_arc)

        # remove labelling from the components
        for key, item in self._model.data.places.items():
            try:
                self._model.data.places[key].rgb_edge = [0, 0, 0]
            except AttributeError:
                pass
        for key, item in self._model.data.transitions.items():
            try:
                self._model.data.transitions[key].rgb_edge = [0, 0, 0]
                self._model.data.transitions[key].rgb_fill = [0, 0, 0]
            except AttributeError:
                pass
        for key, item in self._model.data.arcs.items():
            try:
                self._model.data.arcs[key].rgb_edge = [0, 0, 0]
                self._model.data.arcs[key].origin.rgb_edge = [0, 0, 0]
                self._model.data.arcs[key].target.rgb_edge = [0, 0, 0]
            except AttributeError:
                pass

        # refresh the drawing area
        self.refresh()

    def zoom(self, factor):
        """ Forward zoom command including the defined scaling factor to each of the single components. """
        self._model.data.zoom(factor)
        # refresh drawing area
        self.refresh()

    def add_component(self, status, component):
        """ Add the defined component if the flag status is TRUE. Otherwise the new component will be removed from the list of components. """

        # flag that labels if the component is a node or edge
        self._add_conn = not (type(component) == place.Place or type(component) == transition.Transition)

        # check if a component should be added
        if status:
            # create snapshot
            self._model.create_snapshot()
            # set values
            self._component = component
            self._add_component = True
            self._select = False
            self._multi_select = False
            self._move_items = False
            # add component to the core data
            self._model.data.add(self._component)
        else:
            # set values
            self._component = None
            self._add_component = False
            self._add_conn = False
            self._select = True
            self._multi_select = False
            self._move_items = False
            # remove new component from the core data
            self._model.data.remove_key("new_comp")

    def reset(self):
        """ Reset the configuration settings to the default ones. """

        # check if the last snapshot needs to be removed
        if self._selected_components != None or self._paste or (self._component != None and self._add_component):
            self._model.remove_last_snapshot()
        
        # check if the user is in the add component modus
        if self._add_component:
            # reset flags and values
            self._component = None
            self._add_component = False
            self._add_conn = False
            self._select = True
            self._multi_select = False
            self._move_items = False
            # remove new component from the core data
            self._model.data.remove_key("new_comp")

        # reset general flags
        self._select = True
        self._selected = False
        self._multi_select = False
        self._move_items = False
        self._zoom = False
        self._arc_selection = False

        # check if the user is in the paste modus
        if self._paste:
            # iteration through all copied components
            for i in range(len(self._copied_components)):
                # remove all copied components
                self._model.data.remove_key(self._copied_components[i].key)

        # reset general flags
        self._paste = False
        self._lock_components = False
        self._add_component = False

        # check if the user has selected a single component
        if self._component != None:
            try:
                # reset labelling of the selected component
                self._component.rgb_edge = [0, 0, 0]
                if type(self._component) != place.Place or type(self._component) != transition.Transition:
                    self._component.origin.rgb_edge = [0, 0, 0]
                    if self._component.target != None:
                        self._component.target.rgb_edge = [0, 0, 0]
                        if type(self._component.target) == transition.Transition:
                            self._component.target.rgb_fill = [0, 0, 0]
                # update core data
                self._model.data.update(self._component, self._component.get_key())
            except AttributeError:
                pass

        # check if the user has selected multiple components
        if self._selected_components != None:
            # reset the labelling of all selected components
            for i in range(len(self._selected_components)):
                try:
                    self._selected_components[i].rgb_edge = [0, 0, 0]
                    # update core data
                    self._model.data.update(self._selected_components[i], self._selected_components[i].get_key())
                except AttributeError:
                    pass

        # reset general values
        self._component = None
        self._selected_components = None
        self._start_pos = None
        self._end_pos = None
        self._centered_pos = None

        # reset whole labelling of the components
        for key, item in self._model.data.places.items():
            try:
                self._model.data.places[key].rgb_edge = [0, 0, 0]
            except AttributeError:
                pass
        for key, item in self._model.data.transitions.items():
            try:
                self._model.data.transitions[key].rgb_edge = [0, 0, 0]
                self._model.data.transitions[key].rgb_fill = [0, 0, 0]
            except AttributeError:
                pass
        for key, item in self._model.data.arcs.items():
            try:
                self._model.data.arcs[key].rgb_edge = [0, 0, 0]
                self._model.data.arcs[key].origin.rgb_edge = [0, 0, 0]
                self._model.data.arcs[key].target.rgb_edge = [0, 0, 0]
            except AttributeError:
                pass

        # refresh the drawing area
        self.refresh()

    def delete(self):
        """ Delete the selected component or components. """

        # create a snapshot for the undo operation if needed
        self._model.create_snapshot()

        # check if multiple components are selected which should be deleted
        if self._selected_components != None:
            # remove the selected components
            self._model.data.remove(self._selected_components)
        # check if a single component is selected
        if self._component != None:
            # delete the selected component
            self._model.data.remove([self._component])

        # refresh the drawing area
        self.refresh()

    def refresh(self):
        """ Refresh the drawing area. """
        self._view.refresh()

    def button_press(self, position, event):
        """ Manage the button-press-event. """

        # check if the start-position needs to be stored
        if self._select and self._multi_select and self._move_items:
            self._start_pos = [position[0], position[1]]
            return

        # check if a single item could be selected and the user is not in the multi-select or moving modus
        if self._select and not self._multi_select and not self._move_items:
            # check if a selection was done before
            if self._component != None:
                # reset labelling of the previous component
                self._component.rgb_edge = [0, 0, 0]
                if type(self._component) != place.Place:
                    self._component.rgb_fill = [0, 0, 0]
                # update core data
                self._model.data.update(self._component, self._component.key)
            # check if multiple components were selected before
            if self._selected_components != None and len(self._selected_components) != 0:
                # iteration through all selected components
                for i in range(len(self._selected_components)):
                    # reset labelling of the selected components
                    self._selected_components[i].rgb_edge = [0, 0, 0]
                    if type(self._selected_components[i]) != place.Place:
                        self._selected_components[i].rgb_fill = [0, 0, 0]
                    # update core data
                    self._model.data.update(self._selected_components[i], self._selected_components[i].key)
            # identify selected component
            self._component = self._model.data.get_nearest_component(position)
            # save start position
            self._start_pos = [position[0], position[1]]
            # check if a component could not be selected and the ctrl key is pressed
            if self._component == None and self._ctrl:
                # activate multi-select modus
                self._multi_select = True
            else:
                # check if a component could be identified
                if self._component != None:
                    # creat a snapshot
                    self._model.create_snapshot()
                    self._orig_pos = self._component.position
                    # label component
                    self._component.rgb_edge = [0, 0, 250]
                    if type(self._component) != place.Place:
                        self._component.rgb_fill = [0, 0, 250]
                    # update core data
                    self._model.data.update(self._component, self._component.key)
                    # set flags
                    self._multi_select = False
                    self._move_items = True
                    # refresh drawing area
                    self.refresh()
                else:
                    # user is in the multi-select modus and multiple components need to be selected
                    self._selected_components = self._model.data.get_selected_arcs(position)
                    # check if components could be identified
                    if self._selected_components != None and len(self._selected_components) != 0:
                        # labelling of the selected components
                        self._arc_selection = True
                        for i in range(len(self._selected_components)):
                            self._selected_components[i].rgb_edge = [0, 0, 250]
                            if type(self._selected_components[i]) != place.Place:
                                self._selected_components[i].rgb_fill = [0, 0, 250]
                            # update core data
                            self._model.data.update(self._selected_components[i], self._selected_components[i].key)
                    else:
                        # reset the container for selected components
                        self._selected_components = None

        # check if the user does not want to add a component and executed a double click event
        if not self._add_component and event.type == gtk.gdk._2BUTTON_PRESS:
            # check if a component is selected
            if self._component != None:
                # reset labelling
                self._component.rgb_edge = [0, 0, 0]
                if type(self._component) != place.Place:
                    self._component.rgb_fill = [0, 0, 0]
                # update core data
                self._model.data.update(self._component, self._component.key)
            # select nearest component
            self._component = self._model.data.get_nearest_component(position)
            # check if a component could be identified
            if self._component != None:
                # label the selected component
                self._component.rgb_edge = [0, 0, 250]
                if type(self._component) != place.Place:
                    self._component.rgb_fill = [0, 0, 250]
                # update core data
                self._model.data.update(self._component, self._component.key)
                # detrmine the type of component and instantiate the correct configuration window
                controller = None
                view = None
                # check if the selected component is a place or transitions
                if type(self._component) == place.Place or type(self._component) == transition.Transition:
                    # check if the component is a place
                    if type(self._component) == place.Place:
                        controller = controller_configuration_place.ControllerConfigurationPlace()
                        view = view_configuration_place.ViewConfigurationPlace()
                    # check if the component is a transition
                    if type(self._component) == transition.Transition:
                        controller = controller_configuration_transition.ControllerConfigurationTransition()
                        view = view_configuration_transition.ViewConfigurationTransition()
                    # check if the instantiations for the configuration window were successful
                    if view != None and controller != None:
                        # set objects
                        controller.model = self._model
                        controller.view = view
                        controller.component = self._component
                        view.model = self._model
                        view.controller = controller
                        # show configuration window
                        view.show()
            # check if an arc is selected
            if self._arc_selection and self._selected_components != None:
                # instantiate objects for the arc configuration window
                controller = controller_configuration_arc.ControllerConfigurationArc()
                view = view_configuration_arc.ViewConfigurationArc()
                # set objects
                controller.model = self._model
                controller.view = view
                controller.selected_components = self._selected_components
                view.model = self._model
                view.controller = controller
                # show configuration window
                view.show()
            # abort method
            return

        # check if the user is in the add component modus
        if self._add_component and not self._select:
            # check if the user is not adding an arc
            if not self._add_conn:
                # check if a component has been set
                if self._component != None:
                    # clone the current component and assign new default values
                    new_component = self._component.clone()
                    new_component.position = position
                    new_component.key = "new component"
                    # add component to the core date
                    self._model.data.add(new_component)
                    # instantiate objects for the configuration of the new component
                    controller = None
                    view = None
                    # check if component is a place
                    if type(self._component) == place.Place:
                        controller = controller_configuration_place.ControllerConfigurationPlace()
                        view = view_configuration_place.ViewConfigurationPlace()
                    # check if component is a transition
                    if type(self._component) == transition.Transition:
                        controller = controller_configuration_transition.ControllerConfigurationTransition()
                        view = view_configuration_transition.ViewConfigurationTransition()
                    # check if the instantiations for the configuration window were successful
                    if view != None and controller != None:
                        # set objects
                        controller.model = self._model
                        controller.view = view
                        controller.component = new_component
                        view.model = self._model
                        view.controller = controller
                        # show configuration window
                        view.show()
            else:
                # check if both, the origin and target has been set
                if self._component.origin != None and self._component.target != None:
                    # clone object and set some new values
                    new_component = self._component.clone()
                    new_component.position = position
                    new_component.key = "new component"
                    new_component.origin = self._model.data.get_component(self._component.origin.key)
                    new_component.target = self._model.data.get_component(self._component.target.key)
                    # add component to the core data
                    self._model.data.add(new_component)
                    # instantiate window for the configuration of arcs
                    controller = controller_configuration_arc.ControllerConfigurationArc()
                    view = view_configuration_arc.ViewConfigurationArc()
                    # set objects
                    controller.model = self._model
                    controller.view = view
                    controller.component = new_component
                    view.model = self._model
                    view.controller = controller
                    # show configuration window
                    view.show()
                else:
                    # check if neither the origin nor target has been defined
                    if self._component.origin == None and self._component.target == None:
                        # determine nearest component
                        self._origin = self._model.data.get_nearest_component(position)
                        # check if component could be identified
                        if self._origin != None:
                            # set origin of arc
                            if type(self._component) != arc.Arc:
                                if type(self._origin) == place.Place:
                                    self._component.origin = self._origin
                            else:
                                self._component.origin = self._origin
                    

    def button_release(self, position):
        """ Manage the button-release-event. """

        # check if the user has selected a single component and wants to move it around
        if self._select and not self._multi_select and self._move_items and self._component != None:
            # check if the component is moved out of the buffer zone to move it around (prevents from an unwanted relocation through a double click) - Manhattan Distance
            if math.fabs(position[0] - self._orig_pos[0]) + math.fabs(position[1] - self._orig_pos[1]) > 20:
                # set the new position to the component
                self._component.position = position
                # reset labelling
                self._component.rgb_edge = [0, 0, 0]
                if type(self._component) != place.Place:
                    self._component.rgb_fill = [0, 0, 0]
                # update core data
                self._model.data.update(self._component, self._component.key)
            # reset flags
            self._select = True
            self._move_items = False
            self._start_pos = None
            self._orig_pos = None

        # check if the user is in the multi-select modus and does not want to move components yet
        if self._multi_select and self._component == None and not self._move_items:
            # check if a start-position is defined
            if self._start_pos != None and len(self._start_pos) == 2:
                # markier alle componenten blau!!!
                self._selected_components = self._model.data.get_selected_components_with_arcs(self._start_pos, position)
                if self._selected_components != None and len(self._selected_components) > 0:
                    # create a snapshot
                    self._model.create_snapshot()
                # iteration through all components
                for i in range(len(self._selected_components)):
                    # label the component
                    self._selected_components[i].rgb_edge = [0, 0, 250]
                    if type(self._selected_components[i]) == place.Place:
                        self._selected_components[i].rgb_fill = [0., 0., 250.]
                    # update core data
                    self._model.data.update(self._selected_components[i], self._selected_components[i].key)
                # set flags
                self._selected = True
                self._move_items = True
                # reset start position
                self._start_pos = []
            # abort method
            return

        # check if the user wants to move multiple component around
        if self._multi_select and self._component == None and self._selected_components != None and self._move_items:
            # check if a start position has been defined
            if self._start_pos != None and len(self._start_pos) == 2:
                # define the end-position
                self._end_pos = position
                # calculate difference between the start- and end-position
                dx = self._end_pos[0] - self._start_pos[0]
                dy = self._end_pos[1] - self._start_pos[1]
                # iteration through all selected components
                for i in range(len(self._selected_components)):
                    # calculate new position
                    self._selected_components[i].position = [self._selected_components[i].position[0] + dx, self._selected_components[i].position[1] + dy]
                    # label component
                    self._selected_components[i].rgb_edge = [0., 0., 0.]
                    if type(self._selected_components[i]) == place.Place:
                        self._selected_components[i].rgb_fill = [0., 0., 0.]
                    # update core data
                    self._model.data.update(self._selected_components[i], self._selected_components[i].key)
                # reset flags and values
                self._selected_components = None
                self._start_pos = None
                self._end_pos = None
                self._multi_select = False
                self._move_items = False
        
        # check if the user wants to paste components
        if self._paste and self._copied_components != None and self._centered_pos != None:
            # calculate the difference between the previous position and the actual one
            dx = position[0] - self._centered_pos[0]
            dy = position[1] - self._centered_pos[1]
            # the new centre of the selected components is the current position
            self._centered_pos = position
            # iteration through all copied elements
            for i in range(len(self._copied_components)):
                # calculate new position for a place or transition - not necessary for arcx
                if type(self._copied_components[i]) == place.Place or type(self._copied_components[i]) == transition.Transition:
                    self._copied_components[i].position = [self._copied_components[i].position[0] + dx, self._copied_components[i].position[1] + dy]
                    # update core data
                    self._model.data.update(self._copied_components[i], self._copied_components[i].key)
            # adapt matrices
            self._model.data.convert_matrices()
            # reset flags and values
            self._copied_components = None
            self._paste = False
            self._select = True
            # refresh drawing area
            self.refresh()

    def motion_notify(self, position, ctx):
        """ Manage the motion-notify-event. """

        # check if the user has selected a single component and wants to move it around
        if self._select and not self._multi_select and self._move_items and self._component != None:
            # check if the component is moved out of the buffer zone to move it around (prevents from an unwanted relocation through a double click) - Manhattan Distance
            # only the original position of the component will be regarded
            if math.fabs(position[0] - self._orig_pos[0]) + math.fabs(position[1] - self._orig_pos[1]) > 20:
                # set new position
                self._component.position = position
                # update core data
                self._model.data.update(self._component, self._component.key)
                # refresh drawing area
                self.refresh()
            # abort method
            return

        # check if the user wants to select multiple components
        if self._multi_select and self._component == None and not self._move_items:
            # check if a start position has been defined
            if self._start_pos != None and len(self._start_pos) == 2:
                # draw rectangle
                self.refresh()
                ctx.set_source_rgba(0, 0, 1, 0.50)
                ctx.rectangle(self._start_pos[0], self._start_pos[1], position[0] - self._start_pos[0], position[1] - self._start_pos[1])
                ctx.fill()
                ctx.stroke()
                ctx.clip()
                return

        # check if the user wants to move multiple components around
        if self._multi_select and self._component == None and self._selected_components != None and self._move_items:
            # move the single items from the start- to the end-position but the distances between the components will be the same
            if self._start_pos != None and len(self._start_pos) == 2:
                self._end_pos = position
                dx = self._end_pos[0] - self._start_pos[0]
                dy = self._end_pos[1] - self._start_pos[1]
                self._start_pos = self._end_pos
                # iteration through all selected components
                for i in range(len(self._selected_components)):
                    # calculate new position
                    self._selected_components[i].position = [self._selected_components[i].position[0] + dx, self._selected_components[i].position[1] + dy]
                    # update core data
                    self._model.data.update(self._selected_components[i], self._selected_components[i].key)
            # refresh drawing area
            self.refresh()

        # check if the user wants to paste copied components
        if self._paste and self._copied_components != None and self._centered_pos != None:
            # calculate difference to the previous position - Manhattan Distance
            dx = position[0] - self._centered_pos[0]
            dy = position[1] - self._centered_pos[1]
            self._centered_pos = position
            # iteration through all copied components to assign the new position
            for i in range(len(self._copied_components)):
                # calculate new position
                if type(self._copied_components[i]) == place.Place or type(self._copied_components[i]) == transition.Transition:
                    self._copied_components[i].position = [self._copied_components[i].position[0] + dx, self._copied_components[i].position[1] + dy]
                    # update core data
                    self._model.data.update(self._copied_components[i], self._copied_components[i].key)
            # refresh drawing area
            self.refresh()
            
        # check if a single selected component needs to be moved around
        if not self._select and self._component != None and self._add_component and not self._add_conn:
            # assign new possition
            self._component.position = position
            # update core data
            self._model.data.update(self._component, self._component.key)      
            # refresh drawing area
            self.refresh()
            # abort method
            return

        # check if a new arc needs to be added
        if not self._select and self._component != None and self._add_component and self._add_conn:
            # check if an origin has been defined
            if self._component.origin != None:
                # check if a target has been defined
                if self._component.target != None:
                    # reset labelling
                    self._component.target.rgb_edge = [0, 0, 0]
                    if type(self._component.target) != place.Place:
                        self._component.target.rgb_fill = [0, 0, 0]
                    # update core data
                    self._model.data.update(self._component.target, self._component.target.key)
                # read the new nearest component
                self._component.target = self._model.data.get_nearest_component(position)
                # check if a nearest component could be determined
                if self._component.target != None:
                    # check if the connection is valid
                    if self._model.data.valid_connection(self._component):
                        # label valid component
                        self._component.target_position = None
                        self._component.target.rgb_edge = [0, 255, 0]
                        if type(self._component.target) != place.Place:
                            self._component.target.rgb_fill = [0, 255, 0]
                        self._model.data.update(self._component.target, self._component.target.key)
                    else:
                        # label invalid component
                        self._component.target.rgb_edge = [255, 0, 0]
                        if type(self._component.target) != place.Place:
                            self._component.target.rgb_fill = [255, 0, 0]
                        self._component.target_position = position
                    # update core data
                    self._model.data.update(self._component.target, self._component.target.key)
                else:
                    # set target position of the arc
                    self._component.target = None
                    self._component.target_position = position
            # update core data
            self._model.data.update(self._component, self._component.key)
            # refresh drawing area
            self.refresh()

    def leave_drawing_area(self):
        """ Method is called when the mouse is leaving the drawing area. If the user is in the modus for adding a component the actual component will be hidden removed. """
        
        # check if the user is currently in the add component modus
        if self._add_component:   
            # remove component
            self._model.data.remove_key("new_comp")
            # refresh drawing area
            self.refresh()

    def enter_drawing_area(self):
        """ Method is called when the mouse is entering the drawing area. If the user is in the modus for adding a component the actual component will be added again. """
        
        # check if the user is currently in the add component modus
        if self._add_component:   
            # add component again
            self._model.data.add(self._component)
            # refresh drawing area
            self.refresh()

    def layout(self):
        """ Layouting of the components through opening a configuration window for the different algorithms. """

        # instantiate and show the configuration view for the different layouting algorithms
        controller = controller_layout.ControllerLayout()
        view = view_layout.ViewLayout()
        controller.model = self._model
        controller.view = view
        view.model = self._model
        view.controller = controller
        
        # set the current width and height of the drawing area
        controller.width = self._drawing_area.get_allocation()[2]
        controller.height = self._drawing_area.get_allocation()[3]

        # set selected components
        if self._selected_components != None:
            controller.selected_components = self._selected_components
        else:
            if self._component != None:
                if self._component.key.lower() != "new_comp" or self._component.key.lower() != "new component":
                    controller.selected_components = [self._component]

        # show window
        view.show()

    def export(self):
        """ Exportation of the graph visualisation through opening a configuration window for the acutal operation. """

        # instantiate and show the configuration view for the exportation of the graph visualisation
        controller = controller_petri_net_export.ControllerPetriNetExport()
        view = view_petri_net_export.ViewPetriNetExport()
        controller.model = self._model
        controller.view = view
        controller.drawing_area = self._drawing_area
        view.model = self._model
        view.controller = controller

        # show window
        view.show()
