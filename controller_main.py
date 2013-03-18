#!/usr/bin/python

import pygtk
import gtk

import model as m
import view_main as v
import controller as c

import petri_net
import place
import transition
import arc
import inhibitory_arc
import test_arc

import view_configuration_place
import view_configuration_transition
import view_configuration_arc
import view_file_type
import view_configuration_simulation_diagram
import view_configuration_token_game_animation
import view_results
import view_layout
import controller_configuration_place
import controller_configuration_transition
import controller_configuration_arc
import controller_file_type
import controller_configuration_token_game_animation
import controller_configuration_simulation_diagram
import controller_results
import controller_layout

import converter_matrixtostochasticpetrinet
import converter_stochasticpetrinettomatrix

import force_a as vis

import p_t_invariants

import rparser as rpa
import sbml_lex
import pnml_lex
import txt_convert
import txt2_lex

import_libsbml = True

try:
    import sbml_convert
except AttributeError:
    import_libsbml = False

import pnml_convert
import petri_net_data
import layout

import glib

def yieldsleep(func):
    """ Function is used to set the token game animation to sleep for a defined period without locking the whole application. """
    # Reference: http://stackoverflow.com/
    def start(*args, **kwds):
        iterable = func(*args, **kwds)
        def step(*args, **kwds):
            try:
                time = next(iterable)
                glib.timeout_add_seconds(time, step)
            except StopIteration:
                pass
        glib.idle_add(step)
    return start

class ControllerMain(c.Controller):
    """ The ControllerMain class is a specific controller that inherits from the general Controller class and is used to manage the user interactions of the main window of the application (ViewMain). """

    _iteration_pos = 1
    _ctrl = False
    _alt = False
    _play = False
    _pause = False
    _lock = False
    _add_component = False
    _path_collection = None
    _controller_drawing_area = None

    def __init__(self):
        """ Constructor of ControllerMain. """
        
        # call constructor of parent class
        c.Controller.__init__(self)

        # default values
        self._iteration_pos = 1
        self._ctrl = False
        self._alt = False
        self._play = False
        self._pause = False
        self._lock = False
        self._add_component = False
        self._path_collection = None
        self._controller_drawing_area = None

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerMain. """

        # call constructor of parent class
        c.Controller.__init__(self, model, view)
        
        # default values
        self._iteration_pos = 1
        self._ctrl = False
        self._alt = False
        self._play = False
        self._pause = False
        self._lock = False
        self._add_component = False
        self._path_collection = None
        self._controller_drawing_area = None

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """
        pass

    def update_component(self, key):
        """ Interface to notify Observer objects about a data change of a component. """
        pass

    def update_output(self):
        """ Interface to notify Observer objects about a data change of simulation results. """
        pass

    def reset(self):
        """ Interface to notify MVCObserver objects about a reset event. """
        pass

    def undo(self):
        """ Interface to notify Observer objects about an undo. """
        self._controller_drawing_area.reset()
        self._model.undo()
        self._controller_drawing_area.refresh()

    @property
    def view_drawing_area(self):
        """ Return ViewDrawingArea object. """
        return self._view_drawing_area

    @property
    def controller_drawing_area(self):
        """ Return ControllerDrawingArea object. """
        return self._controller_drawing_area
    
    @view_drawing_area.setter
    def view_drawing_area(self, f):
        """ Set ViewDrawingArea object. """
        self._view_drawing_area = f

    @controller_drawing_area.setter
    def controller_drawing_area(self, controller):
        """ Set ControllerDrawingArea object. """
        self._controller_drawing_area = controller

    def key_press(self, key):
        """ Key press events will be analysed and if necessary different commands will be executed which are associated to special key shortcuts. """

        if key == "Control_L" or key == "Control_R":
            self._ctrl = True
            if self._controller_drawing_area != None:
                self._controller_drawing_area.ctrl_key = self._ctrl

        if key == "Alt_L" or key == "Alt_R" or key == "ISO_Level3_Shift":
            self._alt = True

        if key == "o" and self._ctrl and not self._alt:
            self.open_file(None)

        if key == "s" and self._ctrl and not self._alt:
            self.save_file(None)

        if key == "Delete" and not self._ctrl and not self._alt:
            if self._controller_drawing_area != None:
                self._controller_drawing_area.delete()
        if key == "Escape":
            #self._controller_drawing_area.add_component(False, None)
            self._model.notify_reset()

        if key == "plus" and not self._ctrl and not self._alt:
            self.zoom(1.25)
        if key == "minus" and not self._ctrl and not self._alt:
            self.zoom(float(1 / 1.25))

        if key == "p" and self._ctrl and not self._alt:
            self.export()

        if key == "c" and self._ctrl and not self._alt:
            self.copy()
        if key == "v" and self._ctrl and not self._alt:
            self.paste()
        if key == "z" and self._ctrl and not self._alt:
            self.undo()

        if key == "F5" and not self._ctrl and not self._alt:
            self._controller_drawing_area.refresh()

        if key == "space" and not self._ctrl and not self._alt:
            self.pause_simulation_movie()

        if key == "i" and self._ctrl and not self._alt:
            self.open_layout_file()

        if key == "e" and self._ctrl and not self._alt:
            self.save_layout_file()

        if key == "g" and self._alt and not self._ctrl:
            self.simulation_movie()

        if key == "d" and self._alt and not self._ctrl:
            self.simulation_diagram()

        if key == "i" and self._alt and not self._ctrl:
            self.calculate_invariants()

        if key == "l" and self._alt and not self._ctrl:
            self.layout()

        if key == "r" and not self._ctrl and not self._alt:
            self.start_simulation_movie()

        if key == "p" and not self._ctrl and not self._alt:
            self.pause_simulation_movie()

        if key == "b" and not self._ctrl and not self._alt:
            self.next_simulation_movie()

        if key == "f" and not self._ctrl and not self._alt:
            self.previous_simulation_movie()

        if key == "s" and not self._ctrl and not self._alt:
            self.stop_simulation_movie()

        if key == "l" and self._ctrl and not self._alt:
            self.lock()

        if key == "F6" and not self._ctrl and not self._alt:
            self.add_place()

        if key == "F7" and not self._ctrl and not self._alt:
            self.add_transition()

        if key == "F8" and not self._ctrl and not self._alt:
            self.add_arc()

        if key == "F9" and not self._ctrl and not self._alt:
            self.add_inhibitory_arc()

        if key == "F10" and not self._ctrl and not self._alt:
            self.add_test_arc()

    def key_release(self, key):
        """ Key release events will be analysed and if necessary different commands will be executed which are associated to special key shortcuts. """

        if key == "Control_L" or key == "Control_R":
            self._ctrl = False
            self._controller_drawing_area.ctrl_key = self._ctrl

        if key == "Alt_L" or key == "Alt_R" or key == "ISO_Level3_Shift":
            self._alt = False

    def open_file(self, path = None):
        """ Input file with the define path will be opened, analysed and a PetriNet object will be created if possible and assigned to the functional core of the MVC architecture. """
        
        # check if a path is defined
        if path == None:
            # read input path if no path is defined
            file_chooser = gtk.FileChooserDialog("Choose Input File", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))        
            if file_chooser.run() == gtk.RESPONSE_OK:
                try:
                    path = file_chooser.get_filename()
                except AttributeError:
                    self._view.show_message_box_warning("Invalid File Format!")
            file_chooser.destroy()

        # check if a path could be read
        if path == None:
            # abort method
            return

        # open file
        f = open(path, 'r')

        # Lexing input to tokens
        # check if the parser can be determined automatically through the extenstion of the file
        if '.txt' in f.name:
            lexer = txt2_lex.RLexerTxt()
        elif '.sbml' in f.name and import_libsbml:
            lexer = sbml_lex.RLexerSBML()
        elif '.pnml' in f.name:
            lexer = pnml_lex.RLexerPNML()
        else:
            if '.sbml' in f.name and not import_libsbml:
                self._view.show_message_box_warning("LibSBML is not installed and the SBML format is not usable!")
            # the parser cannot be determined automatically
            # close file
            f.close()
            # open window which is used to choose the correct parser
            controller = controller_file_type.ControllerFileType()
            view = view_file_type.ViewFileType()
            controller.modus = controller.M_OPEN
            controller.path = path
            controller.model = self._model
            controller.view = view
            view.model = self._model
            view.controller = controller
            view.show()
            # abort method
            return

        # create token list
        token_list = lexer.lex(f)

        # set parser
        parser = rpa.RParser()
        # set token list 
        parser.data = token_list
        # parse token list to PetriNetData
        parser.parse()

        # set the data
        self._model.data = petri_net.PetriNet()
        self._model.data.petri_net_data = parser.output
        # set converter
        self._model.data.converter_components = converter_matrixtostochasticpetrinet.ConverterMatrixToStochasticPetriNet()
        self._model.data.converter_matrices = converter_stochasticpetrinettomatrix.ConverterStochasticPetriNetToMatrix()

        # instantiate algorithm to calculate the positions of the individual components
        layout = vis.ForceDirected()
        # initial properties
        layout.width = 900
        layout.height = 600
        layout.border = 85
        layout.iterations = 85

        # check if a drawing area is available and if yes the width and heigth will be determined
        # and used for the initial properties of the layouting algorithm
        if self._controller_drawing_area != None:
            if self._controller_drawing_area.drawing_area != None:
                layout.width = self._controller_drawing_area.drawing_area.get_allocation()[2]
                layout.height = self._controller_drawing_area.drawing_area.get_allocation()[3]

        # set algorithm
        self._model.data.converter_components.layout = layout
        # set data
        self._model.data.converter_components.layout.data = self._model.data.petri_net_data
        # convert components
        self._model.data.convert_components()
        # notification ot the other observers
        self._model.notify()

    def save_file(self, path = None):
        """ Output file with the defined path will be created through a defined format. For this the data stored in the model of the MVC architecture is used. """

        # check if a path is defined
        if path == None:
            # read path to save output file
            file_chooser = gtk.FileChooserDialog("Save File", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))        
            if file_chooser.run() == gtk.RESPONSE_OK:
                try:
                    path = file_chooser.get_filename()
                except AttributeError:
                    self._view.show_message_box_warning("Invalid File Format!")
            file_chooser.destroy()

        # check if an output path is defined
        if path == None:
            # abort
            return

        converter = None
        # check if an extension is defined and determine the converter automatically if possible
        if path.lower().endswith(".txt"):
            converter = txt_convert.WConverterTxt(self._model.data.petri_net_data)
        elif path.lower().endswith(".sbml") and import_libsbml:
            converter = sbml_convert.WConverterSBML(self._model.data.petri_net_data)
        elif path.lower().endswith(".pnml"):
            converter = pnml_convert.WConverterPNML(self._model.data.petri_net_data)
        else:
            if path.lower().endswith(".sbml") and not import_libsbml:
                self._view.show_message_box_warning("LibSBML is not installed and the SBML format is not usable!")
            # converter could not be determined automatically
            # open window which is used to choose the file format for the export
            controller = controller_file_type.ControllerFileType()
            view = view_file_type.ViewFileType()
            controller.modus = controller.M_SAVE
            controller.path = path
            controller.model = self._model
            controller.view = view
            view.model = self._model
            view.controller = controller
            view.show()
            # abort method
            return
        
        # create token list from the PetriNetData object
        token = converter.getPetriNetData()
        # create output file
        converter.save(path)

    def open_layout_file(self, path = None):
        """ Input file with the define path will be opened, analysed and the positions will be assigned to the components of the PetriNet object stored in the model. """

        # check if a path is defined
        if path == None:
            # read input file path
            file_chooser = gtk.FileChooserDialog("Choose Input File", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))        
            if file_chooser.run() == gtk.RESPONSE_OK:
                try:
                    path = file_chooser.get_filename()
                except AttributeError:
                    self._view.show_message_box_warning("Invalid File Format!")
            file_chooser.destroy()

        # check if a path is defined
        if path == None:
            # abort method
            return

        # instantiate a LSLayout object which is responsible to import the position information
        l = layout.LSLayout()
        # load positions from the file
        positions = l.load(path)

        # set positions
        for key, value in l.positions.items():
            component = self._model.data.get_component(key)
            if component != None:
                component.position = value
                self._model.data.update(component, key)
        # notify all observers
        self._model.notify()

    def save_layout_file(self, path):
        """ Output file with the defined path will be created with all positions of the components of the PetriNet object stored in the model. """

        # check if a path is defined
        if path == None:
            # read output file path
            file_chooser = gtk.FileChooserDialog("Save File", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))        
            if file_chooser.run() == gtk.RESPONSE_OK:
                try:
                    path = file_chooser.get_filename()
                except AttributeError:
                    self._view.show_message_box_warning("Invalid File Format!")
            file_chooser.destroy()
            
        # check if a path is defined
        if path == None:
            # abort method
            return

        # instantiate a LSLayout object which is responsible to export the position information
        l = layout.LSLayout()
        # read position information
        l.positions = self._model.data.get_positions()
        # save position information
        positions = l.save(path)

    def copy(self):
        """ Forward copy operation to the ControllerDrawingArea object. """
        if self._controller_drawing_area != None:
            self._controller_drawing_area.copy()

    def paste(self):
        """ Forward paste operation to the ControllerDrawingArea object. """
        if self._controller_drawing_area != None:
            self._controller_drawing_area.paste()

    def delete(self):
        """ Forward delete command to the ControllerDrawingArea object. """
        if self._controller_drawing_area != None:
            self._controller_drawing_area.delete()

    def calculate_invariants(self):
        """ Calculate the P- and T-Invariants and the results will be displayed within a separate window. """

        # instantiate an object to calculate the invariants
        i = p_t_invariants.PTInvariants()
        # set petri net data
        i.set_petri_net(self._model.data.petri_net_data)
        # calculate invariants
        i.calculate_t_invariants()
        i.calculate_p_invariants()

        # create view which is used to visualise the results
        controller = controller_results.ControllerResults()
        view = view_results.ViewResults()
        controller.model = self._model
        controller.view = view

        # add text to the view which displays the results
        controller.add_text("")
        controller.add_text("Places: ")
        controller.add_text(str(self._model.data.petri_net_data.places))
        controller.add_text("")
        controller.add_text("Transitions: ")
        controller.add_text(str(self._model.data.petri_net_data.transitions))
        controller.add_text("")
        controller.add_text("P-Invariants: ")
        controller.add_text(str(i.p_invariants))
        controller.add_text("")
        controller.add_text("T-Invariants: ")
        controller.add_text(str(i.t_invariants))

        # show view
        view.model = self._model
        view.controller = controller
        view.show()

    def simulation_diagram(self):
        """ Show window to configure the simulation for creating diagrams representing the simulation results. """

        controller = controller_configuration_simulation_diagram.ControllerConfigurationSimulationDiagram()
        view = view_configuration_simulation_diagram.ViewConfigurationSimulationDiagram()
        controller.model = self._model
        controller.view = view
        view.model = self._model
        view.controller = controller
        view.show()

    def simulation_token_game_animation(self):
        """ Show window to configure the simulation for the token game animation. """
        
        self._model.data.create_petri_net_data_backup()
        controller = controller_configuration_token_game_animation.ControllerConfigurationTokenGameAnimation()
        view = view_configuration_token_game_animation.ViewConfigurationTokenGameAnimation()
        controller.model = self._model
        controller.view = view
        view.model = self._model
        view.controller = controller
        view.show()

    def pause_simulation_token_game_animation(self):
        """ Pause or continue the token game animation. """

        if self._play:
            self._pause = not self._pause
            if not self._pause:
                self.start_simulation_token_game_animation()

    def stop_simulation_token_game_animation(self):
        """ Stop the token game animation. """

        # reset the player properties
        self._play = False
        self._pause = True
        self._iteration_pos = 1
        # reset the scale
        self._view.player_scale_value = int(self._iteration_pos)
        self._view.player_scale_visibility(False)
        # reset the labelling
        if self._path_collection != None:
            for path in self._path_collection:
                for item in path:
                    item.rgb_edge = [0, 0, 0]
                    item.rgb_fill = [0, 0, 0]
                    self._model.data.update(item, item.key)
        # notify observers
        self._model.data.reset()

    @yieldsleep
    def start_simulation_token_game_animation(self):
        """ Start or continue the token game animation. """

        # set visibility and value of the scale
        self._view.player_scale_visibility(True)
        if self._iteration_pos != self._view.player_scale_value:
            self._iteration_pos = int(self._view.player_scale_value)
        itr = self._iteration_pos
        # check if pause is still activated
        if self._play and self._pause:
            self._pause = False
        self._play = True
        # iteration through all firing events
        for i in range(self._iteration_pos, int(len(self._model.output[0].markings))):
            # check if pause is active
            if self._pause:
                # save position of the animation
                self._iteration_pos = itr
                # check if animation is stopped
                if not self._play:
                    # reset properties
                    self._iteration_pos = 1
                    self._view.player_scale_value = int(self._iteration_pos)
                    self._view.player_scale_visibility(False)
                    # reset labelling
                    if self._path_collection != None:
                        for path in self._path_collection:
                            for item in path:
                                item.rgb_edge = [0, 0, 0]
                                item.rgb_fill = [0, 0, 0]
                                self._model.data.update(item, item.key)
                    # refresh drawing area
                    if self._view_drawing_area != None:
                        self._view_drawing_area.refresh()
                # abort method
                return
            # next step
            itr += 1
            self._view.player_scale_value = int(itr)
            target_place = None
            origin_place = None
            # determine next event and the involved components
            for j in range(len(self._model.data.petri_net_data.places)):
                # check if an increase of the marking ocurred from the previous step to the current one
                if self._model.output[0].markings[i, j] < self._model.output[0].markings[i - 1, j]:
                    # read component details
                    origin_place = self._model.data.get_place(self._model.data.petri_net_data.places[j])
                    origin_place.marking = self._model.output[0].markings[i, j]
                    self._model.data.update(origin_place, origin_place.key)
                # check if a decrease of the marking ocurred from the previous step to the current one
                if self._model.output[0].markings[i, j] > self._model.output[0].markings[i - 1, j]:
                    # read component details
                    target_place = self._model.data.get_place(self._model.data.petri_net_data.places[j])
                    target_place.marking = self._model.output[0].markings[i, j]
                    self._model.data.update(target_place, target_place.key)
            # read transition key
            transition_label = self._model.data.petri_net_data.transitions[self._model.output[0].events[i - 1]]
            # reset labelling of the previous step
            if self._path_collection != None:
                for path in self._path_collection:
                    for item in path:
                        item.rgb_edge = [0, 0, 0]
                        item.rgb_fill = [0, 0, 0]
                        self._model.data.update(item, item.key)
            # determine event firing path
            self._path_collection = self._model.data.get_detailed_paths(self._model.data.get_transition(transition_label))
            # check if a path could be determined
            if self._path_collection != None:
                # label path
                for path in self._path_collection:
                    find_transition = False
                    for item in path:
                        if item.label == transition_label:
                            find_transition = True
                            break
                    for item in path:
                        item.rgb_edge = [255, 0, 0]
                        item.rgb_fill = [255, 0, 0]
                        self._model.data.update(item, item.key)
            # refresh drawing area
            if self._view_drawing_area != None:
                self._view_drawing_area.refresh()
            # sleep for one second
            yield 1
        # stop token game animation
        self.stop_simulation_token_game_animation()

    def next_step_simulation_token_game_animation(self):
        """ Jump to the next step of the token game animation. """

        # set visibility and value of the scale
        self._view.player_scale_visibility(True)
        if self._iteration_pos != self._view.player_scale_value:
            self._iteration_pos = int(self._view.player_scale_value)
        # set position
        itr = self._iteration_pos
        # iteration through all firing events
        for i in range(self._iteration_pos, int(len(self._model.output[0].markings))):
            # increase counter
            itr += 1
            self._view.player_scale_value = int(itr)
            target_place = None
            origin_place = None
            # determine next event and involved components
            for j in range(len(self._model.data.petri_net_data.places)):
                # check if an increase of the marking ocurred from the previous step to the current one
                if self._model.output[0].markings[i, j] < self._model.output[0].markings[i - 1, j]:
                    # read component properties
                    origin_place = self._model.data.get_place(self._model.data.petri_net_data.places[j])
                    origin_place.marking = self._model.output[0].markings[i, j]
                    self._model.data.update(origin_place, origin_place.key)
                # check if a decrease of the marking ocurred from the previous step to the current one
                if self._model.output[0].markings[i, j] > self._model.output[0].markings[i - 1, j]:
                    # read component properties
                    target_place = self._model.data.get_place(self._model.data.petri_net_data.places[j])
                    target_place.marking = self._model.output[0].markings[i, j]
                    self._model.data.update(target_place, target_place.key)
            # read transition key
            transition_label = self._model.data.petri_net_data.transitions[self._model.output[0].events[i - 1]]
            # reset labelling of the previous step
            if self._path_collection != None:
                for path in self._path_collection:
                    for item in path:
                        item.rgb_edge = [0, 0, 0]
                        item.rgb_fill = [0, 0, 0]
                        self._model.data.update(item, item.key)
            # determine event firing path
            self._path_collection = self._model.data.get_detailed_paths(self._model.data.get_transition(transition_label))
            # check if a path could be determined
            if self._path_collection != None:
                # labelling the determined path
                for path in self._path_collection:
                    find_transition = False
                    for item in path:
                        if item.label == transition_label:
                            find_transition = True
                            break
                    for item in path:
                        item.rgb_edge = [255, 0, 0]
                        item.rgb_fill = [255, 0, 0]
                        self._model.data.update(item, item.key)
            # refresh drawing area
            if self._view_drawing_area != None:   
                self._view_drawing_area.refresh()
            return

    def previous_step_simulation_token_game_animation(self):
        """ Jump to the previous step of the token game animation. """

        # set visibility and value of the scale
        self._view.player_scale_visibility(True)
        if self._iteration_pos != self._view.player_scale_value:
            self._iteration_pos = int(self._view.player_scale_value)
        # set position
        itr = self._iteration_pos
        # reverse iteration through all the firing events
        while itr >= 1:
            # reduce iterator
            i = itr - 2
            if i < 1:
                self._view.player_scale_value = 1
                # reset the labelling
                if self._path_collection != None:
                    for path in self._path_collection:
                        for item in path:
                            item.rgb_edge = [0, 0, 0]
                            item.rgb_fill = [0, 0, 0]
                            self._model.data.update(item, item.key)
                # notify observers
                self._model.data.reset()
                # refresh drawing area
                if self._view_drawing_area != None:   
                    self._view_drawing_area.refresh()
                break
            self._view.player_scale_value = int(itr)
            target_place = None
            origin_place = None
            # determine next event and involved components
            for j in range(len(self._model.data.petri_net_data.places)):
                # check if an increase of the marking ocurred from the previous step to the current one
                if self._model.output[0].markings[i, j] < self._model.output[0].markings[i - 1, j]:
                    # read component properties
                    origin_place = self._model.data.get_place(self._model.data.petri_net_data.places[j])
                    origin_place.marking = self._model.output[0].markings[i, j]
                    self._model.data.update(origin_place, origin_place.key)
                # check if a decrease of the marking ocurred from the previous step to the current one
                if self._model.output[0].markings[i, j] > self._model.output[0].markings[i - 1, j]:
                    # read component properties
                    target_place = self._model.data.get_place(self._model.data.petri_net_data.places[j])
                    target_place.marking = self._model.output[0].markings[i, j]
                    self._model.data.update(target_place, target_place.key)
            # read transition key
            transition_label = self._model.data.petri_net_data.transitions[self._model.output[0].events[i - 1]]
            # reset labelling of the previous step
            if self._path_collection != None:
                for path in self._path_collection:
                    for item in path:
                        item.rgb_edge = [0, 0, 0]
                        item.rgb_fill = [0, 0, 0]
                        self._model.data.update(item, item.key)
            # determine event firing path
            self._path_collection = self._model.data.get_detailed_paths(self._model.data.get_transition(transition_label))
            # label event firing path
            if self._path_collection != None:
                for path in self._path_collection:
                    find_transition = False
                    for item in path:
                        if item.label == transition_label:
                            find_transition = True
                            break
                    for item in path:
                        item.rgb_edge = [255, 0, 0]
                        item.rgb_fill = [255, 0, 0]
                        self._model.data.update(item, item.key)
            # refresh drawing area
            if self._view_drawing_area != None:
                self._view_drawing_area.refresh()
            # reduce iterator  
            itr -= 1
            #if itr == 0:
            #    self._model.notify_reset()
            self._view.player_scale_value = int(itr)
            return

    def layout(self):
        """ Forward command to show the window to configure the layouting algorithm. """
        if self._controller_drawing_area != None:
            self._controller_drawing_area.layout()

    def lock(self):
        """ Forward command to lock the screen. """
        if self._controller_drawing_area != None:
            self._lock = not self._lock
            self._controller_drawing_area.lock = self._lock

    def add_place(self):
        """ Create a new place component with default settings and forwards it to the ControllerDrawingArea which is responsible for displaying it. """
        if self._controller_drawing_area != None:
            # reset previous settings
            self._model.notify_reset()

            # instantiate new place object
            self._component = place.Place()
            self._component.label = "New Place"
            self._component.key = "new_comp"
            self._component.marking = 0
            self._component.radius = 15

            # check if places are already available and if yes the size of them is used as template (zoom could be activated)
            adapt = False
            if self._model.data != None:
                for key, item in self._model.data.places.items():
                    if item != None:
                        self._component.radius = item.radius
                        adapt = True
                        break
                # if no place is available it will be checked for available transitions which could be used as template to keep the proportions constant 
                # between different component types
                if not adapt:
                    for key, item in self._model.data.transitions.items():
                        if item != None:
                            self._component.radius = item.dimension[0]
                            adapt = True
                            break 
            # forward component
            if self._controller_drawing_area != None:
                self._controller_drawing_area.add_component(True, self._component)

    def add_transition(self):
        """ Create a new transition component with default settings and forwards it to the ControllerDrawingArea which is responsible for displaying it. """
        if self._controller_drawing_area != None:
            # reset previous settings
            self._model.notify_reset()

            # instantiate new transitions object
            self._component = transition.Transition()
            self._component.label = "New Transition"
            self._component.key = "new_comp"
            self._component.rate = 1
            self._component.dimension = [15, 30]

            # check if transitions are already available and if yes the size of them is used as template (zoom could be activated)
            adapt = False
            if self._model.data != None:
                for key, item in self._model.data.transitions.items():
                    if item != None:
                        self._component.dimension = item.dimension
                        adapt = True
                        break
                # if no place is available it will be checked for available places which could be used as template to keep the proportions constant 
                # between different component types
                if not adapt:
                    for key, item in self._model.data.places.items():
                        if item != None:
                            self._component.dimension = [item.radius, 2 * item.radius]
                            adapt = True
                            break 

            # forward component
            if self._controller_drawing_area != None:
                self._controller_drawing_area.add_component(True, self._component)

    def add_standard_arc(self):
        """ Create a new standard arc component with default settings and forwards it to the ControllerDrawingArea which is responsible for displaying it. """
        self.add_arc(arc.Arc())

    def add_inhibitory_arc(self):
        """ Create a new inhibitory arc component with default settings and forwards it to the ControllerDrawingArea which is responsible for displaying it. """
        self.add_arc(inhibitory_arc.InhibitoryArc())

    def add_test_arc(self):
        """ Create a new test arc component with default settings and forwards it to the ControllerDrawingArea which is responsible for displaying it. """
        self.add_arc(test_arc.TestArc())

    def add_arc(self, a):
        """ Forwards a defined arc a to the ControllerDrawingArea which is responsible for displaying it. """
        if self._controller_drawing_area != None:            
            # reset previous settings
            self._model.notify_reset()

            self._component = a
            self._component.label = "New Arc"
            self._component.key = "new_comp"

            # forward component
            self._controller_drawing_area.add_component(True, self._component)

    def zoom(self, factor):
        """ Forward zoom command including the defined scaling factor. """
        if self._controller_drawing_area != None:
            self._controller_drawing_area.zoom(factor)

    def export(self):
        """ Forward export command . """
        if self._controller_drawing_area != None:
            self._controller_drawing_area.export()
