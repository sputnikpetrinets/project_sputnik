#!/usr/bin/python

import os
import time
import pygtk
import gtk
import cairo

import view
import view_drawing_area
import controller_drawing_area

class ViewMain(view.View):
    """ The ViewMain class is a specific view that inherits from the general View class and is used to create the main window of the application. """

    def __init__(self):
        """ Constructor of ViewMain. """

        # call constructor of parent class
        view.View.__init__(self)

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewMain. """

        # call constructor of parent class
        view.View.__init__(self, model, controller)

    def show(self):
        """ Interface to create and display the GUI on the screen. """

        # basic path of the resources
        self._basic_res_path = "res/png/"
        # lists used to create and define a toolbar
        # text
        self._list_text_main = ["Open", "Load Positions", "Save", "Save Positions", "Export Petri Net", "SEP", "Undo", "Delete", "Zoom Out", "Zoom In", "Copy", "Paste", "SEP", "Refresh", "Layout", "SEP",
                                "Simulation - Diagram", "Calculate Invariants", "SEP", "Simulation - Movie", "Backward", "Run", "Pause", "Stop", "Forward", "SEP", "Lock", "Place", 
                                "Transition", "Arc", "Inhibitory Arc", "Test Arc", "SEP", "Exit"]
        # image paths
        self._list_img_path_main = [self._basic_res_path + "fileopen.png",                                   
                                    self._basic_res_path + "import_positions.png",
                                    self._basic_res_path + "filesave.png",
                                    self._basic_res_path + "export_positions.png",
                                    self._basic_res_path + "export.png", None,
                                    self._basic_res_path + "undo.png",
                                    self._basic_res_path + "delete.png",
                                    self._basic_res_path + "zoom_minus.png",
                                    self._basic_res_path + "zoom_plus.png",
                                    self._basic_res_path + "editcopy.png", 
                                    self._basic_res_path + "editpaste.png", None,
                                    self._basic_res_path + "refresh.png", 
                                    self._basic_res_path + "layout.png", None,
                                    self._basic_res_path + "simulation_diagram.png",                                   
                                    self._basic_res_path + "calculate_invariants.png", None,
                                    self._basic_res_path + "simulation_movie.png",
                                    self._basic_res_path + "player_backward.png", 
                                    self._basic_res_path + "player_play.png", 
                                    self._basic_res_path + "player_pause.png", 
                                    self._basic_res_path + "player_stop.png", 
                                    self._basic_res_path + "player_forward.png",None,
                                    self._basic_res_path + "lock.png",
                                    self._basic_res_path + "comp_place.png",
                                    self._basic_res_path + "comp_transition.png",
                                    self._basic_res_path + "comp_arc.png",
                                    self._basic_res_path + "comp_arc_inhib.png", 
                                    self._basic_res_path + "comp_arc_test.png", None, 
                                    self._basic_res_path + "exit.png"]
        # position on the toolbar
        self._list_position_main = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
        # connected methods
        self._list_method_main = [self._btn_open, self._btn_open_layout_file, self._btn_save, self._btn_save_layout_file, self._btn_export, None, 
                                  self._btn_undo, self._btn_delete,  self._btn_zoom_out, self._btn_zoom_in, 
                                  self._btn_copy, self._btn_paste, None, self._btn_reload, self._btn_layout, None, self._btn_simulation_diagram, self._btn_calculate_invariants, 
                                  None, self._btn_simulation_movie, self._btn_backward, self._btn_play, self._btn_pause, self._btn_stop, 
                                    self._btn_forward, None, self._btn_lock, self._btn_add_place, self._btn_add_transition,  
                                  self._btn_add_arc, self._btn_add_inhibitory_arc, self._btn_add_test_arc, None, self._btn_exit]
        # button type
        self._list_btn_type_main = ["normal", "normal", "normal", "normal", "normal", "", "normal", "normal", "normal", "normal", 
                                    "normal", "normal", "",  "normal", "normal", "", "normal", "normal",
                                    "", "normal", "normal", "normal", "normal", "normal", "normal", "",
                                    "toggle", "normal", "normal", "normal", "normal", "normal", "",  "normal"]

        # vertical box that contains the main window components
        self._vbox = gtk.VBox(False, 4)

        # instantiate a ViewDrawingArea object which is used to display the graph
        # and will be nested into this view
        self._view_drawing_area = view_drawing_area.ViewDrawingArea()
        self._controller_drawing_area = controller_drawing_area.ControllerDrawingArea()
        self._controller_drawing_area.view = self._view_drawing_area
        self._controller_drawing_area.model = self._model
        self._view_drawing_area.model = self._model
        self._view_drawing_area.controller = self._controller_drawing_area
        self._controller.controller_drawing_area = self._controller_drawing_area
        self._view_drawing_area.show()
        if self._controller != None:
            self._controller.view_drawing_area = self._view_drawing_area
        
        # create a scale object which is used for the token game animation
        self._scale = gtk.HScale()
        self._scale.set_range(1, 100)
        self._scale.set_increments(1, 10)
        self._scale.set_digits(0)

        # add toolbar to the window
        self._vbox.pack_start(self._toolbar(self._list_text_main, self._list_img_path_main, 
                                            self._list_position_main, self._list_method_main, gtk.TOOLBAR_ICONS, self._list_btn_type_main), False, False)
        self._vbox.pack_start(self._scale, False, False)
        self._vbox.pack_start(self._view_drawing_area)

        # add key-press and release events to the GUI
        self._window.connect("key-press-event", self._key_press_event)
        self._window.connect("key-release-event", self._key_release_event)
        
        # add the vertical box containing all important components to the window
        self._window.add(self._vbox)
        self._window.resize(1000, 700)
        self._window.set_title("Stochastic Petri Net Simulator")
        self._window.show_all()
        self._window.show()

        # hide scale - only visible during the token game animation
        self._scale.hide()

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """
        pass

    def update_component(self, key):
        """ Interface to notify Observer objects about a data change of a component. """
        pass

    def update_output(self):
        """ Interface to notify Observer objects about a data change of simulation results. """
        self._scale.set_range(1, int(self._model.output_args[1]))
        self._scale.set_value(1)
        self._scale.show()

    def reset(self):
        """ Interface to notify MVCObserver objects about a reset event. """
        pass

    def undo(self):
        """ Interface to notify Observer objects about an undo. """
        pass

    @property
    def player_scale_value(self):
        """ Return value of the scale. """
        return self._scale.get_value()

    @player_scale_value.setter
    def player_scale_value(self, value):
        """ Set value of the scale. """
        self._scale.set_value(int(value))

    def _key_press_event(self, widget, event):
        """ Used to recognize key-press-events. """
        self._controller.key_press(gtk.gdk.keyval_name(event.keyval))

    def _key_release_event(self, widget, event):
        """ Used to recognize key-release-events. """
        self._controller.key_release(gtk.gdk.keyval_name(event.keyval))

    def _toolbar(self, list_text, list_img_path, list_position, list_method, style, list_btn_type):
        """ Create a toolbar according to the specifications within the lists. The texts of the buttons is defined through list_text, the image path through list_img_path, the position within the toolbar through list_position, the connected method through list_method, the style of the toolbar and the type of the button (normal or toggle). """

        # check dimensionality of the lists
        if len(list_text) != len(list_img_path) or len(list_text) != len(list_position) or len(list_text) != len(list_method):
            # invalid dimensionality and an empty toolbar will be returned
            return gtk.Toolbar()
        # instantiate a new toolbar with the defined style
        toolbar = gtk.Toolbar()
        toolbar.set_style(style)
        # iteration through all buttons that need to be added
        for i in range(len(list_text)):
            # is the actual item a separator
            if list_text[i] == "SEP":
                # add separator
                toolbar.insert(gtk.SeparatorToolItem(), list_position[i])
            else:
                # is the actual item a toggle button
                if list_btn_type[i].lower() == "toggle":
                    # add toggle button
                    self._toolbar_togglebtn(toolbar, list_text[i], self._get_image(list_img_path[i], 24, 24), 
                                            list_position[i], list_method[i])
                # is the actual item a normal button
                if list_btn_type[i].lower() == "normal":
                    # add normal button
                    self._toolbar_btn(toolbar, list_text[i], self._get_image(list_img_path[i], 24, 24), 
                                      list_position[i], list_method[i])
        # return toolbar
        return toolbar

    def _toolbar_togglebtn(self, toolbar, text, image, position, met):
        """ Add toggle button to the defined toolbar referenced through toolbar. Additionally the text, image, position and method can be defined. """
        btn = gtk.ToggleToolButton()
        btn.set_icon_widget(image)
        btn.set_label(text)
        btn.set_tooltip(gtk.Tooltips(), text)
        btn.connect('clicked', met)
        toolbar.insert(btn, position)
        btn.show()

    def _toolbar_btn(self, toolbar, text, image, position, met):
        """ Add normal button to the defined toolbar referenced through toolbar. Additionally the text, image, position and method can be defined. """
        btn = gtk.ToolButton()
        btn.set_icon_widget(image)
        btn.set_label(text)
        btn.set_tooltip(gtk.Tooltips(), text)
        btn.connect('clicked', met)
        toolbar.insert(btn, position)
        btn.show()

    def _get_image(self, img_path, width, height):
        """ Create a gtk.Image object with a defined width and height for an image defined through its path. """
        img = gtk.Image()
        img.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(img_path , width, height))
        img.show()
        return img

    def _btn_open(self, widget):
        """ View part of the file open dialog for reading an input file that defines a petri net in matrix form. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            file_chooser = gtk.FileChooserDialog("Choose Input File", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))        
            if file_chooser.run() == gtk.RESPONSE_OK:
                try:
                    self._controller.open_file(file_chooser.get_filename())
                except AttributeError:
                    self.show_message_box_warning("It was not possible to open the chosen file!")
            file_chooser.destroy()   
        else:
            self.show_message_box_warning("No controller or model has been defined!")     

    def _btn_save(self, widget):
        """ View part of the file save dialog for saving the petri net in matrix form. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            file_chooser = gtk.FileChooserDialog("Save File", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))        
            if file_chooser.run() == gtk.RESPONSE_OK:
                self._controller.save_file(file_chooser.get_filename())
            file_chooser.destroy()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_export(self, widget):
        """ View part to export the graph representation of the petri net. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.export()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_open_layout_file(self, widget):
        """ View part of the file open dialog for reading an input file that defines the positions of the components. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            file_chooser = gtk.FileChooserDialog("Choose Input File", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))        
            if file_chooser.run() == gtk.RESPONSE_OK:
                try:
                    self._controller.open_layout_file(file_chooser.get_filename())
                except AttributeError:
                    self.show_message_box_warning("Invalid File Format!")
            file_chooser.destroy()   
        else:
            self.show_message_box_warning("No controller or model has been defined!") 

    def _btn_save_layout_file(self, widget):
        """ View part of the file save dialog for saving the positions of the component. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            file_chooser = gtk.FileChooserDialog("Save File", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))        
            if file_chooser.run() == gtk.RESPONSE_OK:
                self._controller.save_layout_file(file_chooser.get_filename())
            file_chooser.destroy()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_delete(self, widget):
        """ View part to delete selected components. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.delete()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_undo(self, widget):
        """ View part to restor a previous state of the petri net. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.undo()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_copy(self, widget):
        """ View part to copy selected components. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.copy()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_paste(self, widget):
        """ View part to paste previous copied components. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.paste()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_simulation_diagram(self, widget):
        """ View part for starting the simulation window for the visualisation of the results as a diagram. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            # check if model data and simulation results are available
            if self._model.data != None and self._model.data.petri_net_data != None:
                if len(self._model.data.places) != 0 and len(self._model.data.transitions) != 0 and len(self._model.data.arcs) != 0:
                    self._controller.simulation_diagram()
                else:
                    self.show_message_box_warning("No valid petri net available!")
            else:
                self.show_message_box_warning("No valid petri net available!")
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_simulation_movie(self, widget):
        """ View part for starting the simulation window for the token game animation. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            # check if model data and simulation results are available
            if self._model.data != None and self._model.data.petri_net_data != None:
                if len(self._model.data.places) != 0 and len(self._model.data.transitions) != 0 and len(self._model.data.arcs) != 0:
                    self._controller.simulation_token_game_animation()
                else:
                    self.show_message_box_warning("No valid petri net available!")
            else:
                self.show_message_box_warning("No valid petri net available!")
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_calculate_invariants(self, widget):
        """ View part for calculating the P- and T-Invariants. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            # check if model data and simulation results are available
            if self._model.data != None and self._model.data.petri_net_data != None:
                self._controller.calculate_invariants()
            else:
                self.show_message_box_warning("No valid petri net available!")
        else:
            self.show_message_box_warning("No controller or model has been defined!")
        

    def player_scale_visibility(self, status):
        """ Set visibility of the scale. """
        if status:
            self._scale.show()
        else:
            self._scale.hide()

    def _btn_reload(self, widget):
        """ View part to refresh. """
        self._view_drawing_area.refresh()

    def _btn_layout(self, widget):
        """ View part for starting the configuration window for layouting the components. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.layout()
        else:
            self.show_message_box_warning("No controller or model has been defined!")
    
    def _btn_backward(self, widget):
        """ View part to jump to the previous event within the token game animation. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            # check if model data and simulation results are available
            if self._model.data != None and self._model.output != None:
                self._controller.previous_step_simulation_token_game_animation()
            else:
                self.show_message_box_warning("There are no data to simulate available! Please simulate the petri net first.")        
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_play(self, widget):
        """ View part to start token game animation. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            # check if model data and simulation results are available
            if self._model.data != None and self._model.output != None:
                self._controller.start_simulation_token_game_animation()
            else:
                self.show_message_box_warning("There are no data to simulate available! Please simulate the petri net first.")        
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_pause(self, widget):
        """ View part to pause token game animation. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            # check if model data and simulation results are available
            if self._model.data != None and self._model.output != None:
                self._controller.pause_simulation_token_game_animation()
            else:
                self.show_message_box_warning("There are no data to simulate available! Please simulate the petri net first.")
        else:
            self.show_message_box_warning("No controller or model has been defined!")
    
    def _btn_stop(self, widget):
        """ View part to stop token game animation. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            # check if model data and simulation results are available
            if self._model.data != None and self._model.output != None:
                self._controller.stop_simulation_token_game_animation()
            else:
                self.show_message_box_warning("There are no data to simulate available! Please simulate the petri net first.")
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_forward(self, widget):
        """ View part to jump to the next step within the token game animation. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            # check if model data and simulation results are available
            if self._model.data != None and self._model.output != None:
                self._controller.next_step_simulation_token_game_animation()
            else:
                self.show_message_box_warning("There are no data to simulate available! Please simulate the petri net first.")
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_lock(self, widget):
        """ View part to lock the screen. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.lock()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_add_place(self, widget):
        """ View part to add a new place. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.add_place()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_add_transition(self, widget):
        """ View part to add a new transition. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.add_transition()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_add_arc(self, widget):
        """ View part to add a new standard arc. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.add_standard_arc()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_add_inhibitory_arc(self, widget):
        """ View part to add a new inhibitory arc. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.add_inhibitory_arc()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_add_test_arc(self, widget):
        """ View part to add a new test arc. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.add_test_arc()
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_exit(self, widget):
        """ Close application completely. """
        gtk.main_quit()

    def close(self, widget):
        """ Close application completely. """
        gtk.main_quit()

    def _btn_zoom_in(self, widget):
        """ View part to increase component size. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.zoom(1.25)
        else:
            self.show_message_box_warning("No controller or model has been defined!")

    def _btn_zoom_out(self, widget):
        """ View part to decrease component size. """
        # check if a controller and model are defined
        if self._controller != None and self._model != None:
            self._controller.zoom(float(1 / 1.25))
        else:
            self.show_message_box_warning("No controller or model has been defined!")

if __name__ == "__main__":
    model = m.Model()
    model.data = petri_net.PetriNet()
    controller = controller_main.ControllerMain()
    app = ViewMain()
    controller.view = app
    controller.model = model
    app.model = model
    app.controller = controller
    app.show()
    gtk.main()

    
