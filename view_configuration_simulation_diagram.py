#!/usr/bin/python

import pygtk
import gtk

import view_configuration_simulation as view

import diagram
import diagram_visualisation
import trajectory

class ViewConfigurationSimulationDiagram(view.ViewConfigurationSimulation):
    """ The ViewConfigurationSimulationDiagram class is a specific view that inherits from the general ViewConfigurationSimulation class and is used to visualise the configuration window for the visualisation of the simulation results and contains a ControllerConfigurationSimulationDiagram object. """

    _places = dict()
    _simulations = dict()
    _simulation_diagrams = dict()

    def __init__(self):
        """ Constructor of ViewConfigurationSimulationDiagram. """
        
        # call constructor of parent class
        view.ViewConfigurationSimulation.__init__(self)

        # set algorithm and window size
        self._algorithm = self.A_GILLESPIE
        self._window.resize(150, 150)

        # set default values
        self._color = None
        self._selected_place = None
        self._selected_simulation = None
        self._selected_simulation_index = 0
        self._places = dict()
        self._simulations = dict()
        self._simulations_diagrams = dict()
        self._color_button = None
        self._auto_color = True
        self._show_title = False
        self._show_legend = True
        self._create_subplots = False

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewConfigurationSimulationDiagram. """
        
        # call constructor of parent class
        view.ViewConfigurationSimulation.__init__(self, model, controller)

        # set algorithm and window size
        self._algorithm = self.A_GILLESPIE
        self._window.resize(150, 150)

        # set default values
        self._color = None
        self._selected_place = None
        self._selected_simulation = None
        self._selected_simulation_index = 0
        self._places = dict()
        self._simulations = dict()
        self._simulations_diagrams = dict()
        self._color_button = None
        self._auto_color = True
        self._show_title = False
        self._show_legend = True
        self._create_subplots = False

    def show(self):
        """ Interface to create and display the GUI on the screen. """

        # call show method from the parent class
        view.ViewConfigurationSimulation.show(self)

        # create the table
        self._table = gtk.Table(32, 4, False)

        # create the list for the simulations
        self._add_label("What should be displayed within the diagrams?", [3, 4, 0, 1])
        self._add_label("", [3, 4, 1, 2])
        self._add_label("<b>Simulations:</b>", [3, 4, 2, 3])
        self._sim_list_store = gtk.ListStore(bool, str, str)
        self._tv_sim = gtk.TreeView(self._sim_list_store)
        cell_sim_check = gtk.CellRendererToggle()
        cell_sim_text = gtk.CellRendererText()
        cell_sim_index = gtk.CellRendererText()
        cell_sim_check.connect("toggled", self._on_tree_view_toggle, self._sim_list_store)
        col_sim_check = gtk.TreeViewColumn("Plot", cell_sim_check, active = 0)
        col_sim_text = gtk.TreeViewColumn("Simulation", cell_sim_text, text = 1)
        col_sim_index = gtk.TreeViewColumn("Index", cell_sim_index, text = 2)
        self._tv_sim.append_column(col_sim_check)
        self._tv_sim.append_column(col_sim_text)
        self._tv_sim.append_column(col_sim_index)
        self._tv_sim.connect('cursor-changed', self._on_tree_view_sim_cursor_change)
        self._sim_list_store.append([True, "Simulation 1", 1])

        # the simulation list will be embedded into a scrolled window
        scrolled_window_sim = gtk.ScrolledWindow()
        scrolled_window_sim.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window_sim.add(self._tv_sim)
        self._table.attach(scrolled_window_sim, 3, 4, 3, 16)

        # create a menu to choose the algorithm
        self._add_label("Algorithm:", [0, 1, 0, 1])
        radio_button_gillespie = gtk.RadioButton(None, "Gillespie")
        radio_button_gillespie.connect("toggled", self._on_radio_button_changed, "gillespie")
        radio_button_tau_leap = gtk.RadioButton(radio_button_gillespie, "Tau Leap")
        radio_button_tau_leap.connect("toggled", self._on_radio_button_changed, "tauleap")
        self._table.attach(radio_button_gillespie, 1, 2, 0, 1)
        self._table.attach(radio_button_tau_leap, 2, 3, 0, 1)

        # create widgets to read the simulation parameter
        self._add_label("Runtime:", [0, 1, 1, 2])
        self._add_label("Time Step:", [0, 1, 2, 3])
        self._add_label("Number of Simulations:", [0, 1, 3, 4])
        self._add_label("Epsilon (Tau Leap only):", [0, 1, 4, 5])
        self._add_label("Control Parameter (Tau Leap):", [0, 1, 5, 6])
        self._add_label("Number of SSA Runs (Tau Leap):", [0, 1, 6, 7])
        self._ent_runtime = self._add_entry("50", [1, 2, 1, 2])
        self._ent_time_step = self._add_entry("1", [1, 2, 2, 3])
        self._ent_num_sim = self._add_entry("1", [1, 2, 3, 4])
        self._ent_epsilon = self._add_entry("0.03", [1, 2, 4, 5])
        self._ent_control_parameter = self._add_entry("10", [1, 2, 5, 6])
        self._ent_num_ssa_runs = self._add_entry("100", [1, 2, 6, 7])
        self._ent_num_sim.connect("changed", self._text_changed)

        # create widgets to configure the general diagram settings
        self._add_label("<b>Plot Settings:</b>", [0, 1, 7, 8])
        self._add_label("Title:", [0, 1, 8, 9])
        self._add_label("X Label:", [0, 1, 9, 10])
        self._add_label("Y Label", [0, 1, 10, 11])
        self._add_label("Line Width:", [0, 1, 11, 12])
        self._ent_title = self._add_entry("Simulation", [1, 2, 8, 9])
        self._ent_xlabel = self._add_entry("Runtime", [1, 2, 9, 10])
        self._ent_ylabel = self._add_entry("Marking", [1, 2, 10, 11])
        self._ent_line_width = self._add_entry("1", [1, 2, 11, 12])
        self._check_button_legend = self._add_checkbutton("Show Legend", [2, 3, 12, 13], self._on_change_checkbutton, True)
        self._add_label("Legend Position:", [0, 1, 12, 13])
        self._ent_legend_position = self._add_entry("0", [1, 2, 12, 13])
        self._check_button_title = self._add_checkbutton("Show Title", [2, 3, 8, 9], self._on_change_checkbutton, True)
        self._add_label("Subplot Rows and Columns:", [0, 1, 14, 15])
        self._ent_num_rows = self._add_entry("1", [1, 2, 14, 15])
        self._ent_num_cols = self._add_entry("1", [2, 3, 14, 15])
        self._check_button_subplots = self._add_checkbutton("Create Subplots", [1, 2, 13, 14], self._on_change_checkbutton, False)
        self._check_button_auto_position_subplot = self._add_checkbutton("Automatic Position Allocation", [2, 3, 13, 14], self._on_change_checkbutton, True)

        # create widgets to configure specific diagram settings
        self._add_label("<b>Subplot Settings:</b>", [0, 1, 15, 16])
        self._add_label("Title:", [0, 1, 16, 17])
        self._add_label("X Label:", [0, 1, 17, 18])
        self._add_label("Y Label", [0, 1, 18, 19])
        self._add_label("Subplot Position:", [0, 1, 19, 20])
        self._check_button_subplot_title = self._add_checkbutton("Show Subtitle", [2, 3, 16, 17], self._on_change_checkbutton, True)
        self._ent_subplot_position = self._add_entry("0", [1, 2, 19, 20])
        self._check_button_subplot_legend = self._add_checkbutton("Show Subplot Legend", [2, 3, 20, 21], self._on_change_checkbutton, True)
        self._add_label("Legend Position:", [0, 1, 20, 21])
        self._ent_subplot_legend_position = self._add_entry("0", [1, 2, 20, 21])
        self._ent_subplot_title = self._add_entry("", [1, 2, 16, 17])
        self._ent_subplot_xlabel = self._add_entry("Runtime", [1, 2, 17, 18])
        self._ent_subplot_ylabel = self._add_entry("Marking", [1, 2, 18, 19])
        #self._ent_subplot_position = self._add_entry("0", [1, 2, 17, 18])
        button_save_sim = gtk.Button("Save Settings")
        button_save_sim.connect("clicked", self._on_save_sim_clicked)
        self._table.attach(button_save_sim, 1, 2, 22, 23)

        # create widgets to configure specific trajectory settings
        self._add_label("<b>Line Settings:</b>", [0, 1, 24, 25])
        self._add_label("Legend Text:", [0, 1, 25, 26])        
        self._ent_place_legend_text = self._add_entry("", [1, 2, 25, 26])
        self._add_label("Colour:", [0, 1, 26, 27])
        self._color_button = gtk.ColorButton(gtk.gdk.color_parse('blue'))
        self._color_button.set_use_alpha(True)
        self._color_button.set_title("Select a Color")
        #color_button.set_alpha(32767)
        self._color_button.connect("color-set", self.color_set_cb)
        self._table.attach(self._color_button, 1, 2, 26, 27)
        self._check_button_auto_color = self._add_checkbutton("Automatic Colour Allocation", [2, 3, 26, 27], self._on_change_checkbutton, True)
        button_save_plot = gtk.Button("Save Line")
        button_save_plot.connect("clicked", self._on_save_plot_clicked)
        self._table.attach(button_save_plot, 1, 2, 27, 28)

        # create a list containing all species / places of a given petri net
        if self._model != None:
            self._add_label("", [3, 4, 19, 20])
            self._add_label("<b>Places:</b>", [3, 4, 16, 17])
            self._p_list_store = gtk.ListStore(bool, str, str)
            for key, item in self._model.data.places.items():
                if item != None and key != "new_comp":
                    self._p_list_store.append([True, key, item.label])
            self._tv_p = gtk.TreeView(self._p_list_store)
            cell_p_check = gtk.CellRendererToggle()
            cell_p_key = gtk.CellRendererText()
            cell_p_label = gtk.CellRendererText()
            cell_p_check.connect("toggled", self._on_tree_view_toggle, self._p_list_store)
            col_p_check = gtk.TreeViewColumn("Plot", cell_p_check, active = 0)
            col_p_key = gtk.TreeViewColumn("Place-Key", cell_p_key, text = 1)
            col_p_label = gtk.TreeViewColumn("Place-Label", cell_p_label, text = 1)
            self._tv_p.append_column(col_p_check)
            self._tv_p.append_column(col_p_key)
            self._tv_p.append_column(col_p_label)
            self._tv_p.connect('cursor-changed', self._on_tree_view_place_cursor_change)
            scrolled_window_p = gtk.ScrolledWindow()
            scrolled_window_p.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrolled_window_p.add(self._tv_p)
            self._table.attach(scrolled_window_p, 3, 4, 17, 32)

        # create general buttons needed to create the simulation and visualise the results
        button_ok = gtk.Button("Show Plot")
        button_ok.connect("clicked", self._on_ok_clicked)
        button_cancel = gtk.Button("Cancel")
        button_cancel.connect("clicked", self._on_cancel_clicked)
        button_simulate = gtk.Button("Start Simulation")
        button_simulate.connect("clicked", self._on_simulate_clicked)
        self._table.attach(button_simulate, 0, 1, 31, 32)
        self._table.attach(button_ok, 1, 2, 31, 32)
        self._table.attach(button_cancel, 2, 3, 31, 32)

        # attach the table to the window
        self._window.add(self._table)
        # show all components
        self._window.show_all()
        self._window.show()

    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """
        pass

    def update_component(self, key):
        """ Interface to notify Observer objects about a data change of a component. """
        pass

    def update_output(self):
        """ Interface to notify Observer objects about a data change of simulation results. """
        pass

    def undo(self):
        """ Interface to notify Observer objects about an undo. """
        pass

    def _add_label(self, text, position):
        """ Add a label with a text to the table at the defined position and returns a reference. """
        # create label
        label = gtk.Label()
        label.set_markup(text)
        # attach label to the table
        self._table.attach(label, *position)
        # return reference
        return label

    def _add_entry(self, initial_value, position):
        """ Add an entry box with an initial value to the table at the defined position and returns a reference. """
        # create an entry box
        ent = gtk.Entry()
        ent.set_text(initial_value) 
        # attach entry box to the table
        self._table.attach(ent, *position)
        # return reference
        return ent

    def _add_checkbutton(self, text, position, method, checked):
        """ Add a checkbutton with an initial state, text and connected method to the table at the defined position and returns a reference. """
        # create a checkbutton
        btn = gtk.CheckButton(text)
        btn.set_active(checked)
        btn.connect("toggled", method, text)
        # attach checkbutton to the table
        self._table.attach(btn, *position)
        # return reference
        return btn

    def _text_changed(self, *args):
        """ Is called if a text change event ocurrs. """
        try:
            # adapt the list of simulations for the new value
            self._sim_list_store.clear()
            # recreate list
            for i in range(int(self._ent_num_sim.get_text())):
                self._sim_list_store.append([True, "Simulation " + str((i + 1)), str((i + 1))])
        except ValueError:
            pass

    def _on_tree_view_place_cursor_change(self, widget, data = None):
        """ Is called if the location of the cursor within the treeview for the places changes. """
        try:
            # get selection of the treeview
            selection = self._tv_p.get_selection()
            # set selection mode
            selection.set_mode(gtk.SELECTION_SINGLE)
            # get model and index of the selected item
            tv_model, tv_index = selection.get_selected()
            # selected item is the selected place here
            self._selected_place = tv_model.get_value(tv_index, 1) # = key
            # check if this key is available which means that a configuration can be loaded
            if self._places.has_key(self._selected_place):
                # set values
                self._places[self._selected_place].color
                try:
                    self._color_button.set_color(gtk.gdk.color_parse(str(self._places[self._selected_place].color)))
                except ValueError:
                    pass
                self._ent_place_legend_text.set_text(self._places[self._selected_place].legend_text)
                self._check_button_auto_color.set_active(self._places[self._selected_place].auto_color_allocation)
            else:
                # set default values
                self._ent_place_legend_text.set_text(str(tv_model.get_value(tv_index, 2)))
                try:
                    self._check_button_auto_color.set_active(True)
                except ValueError:
                    pass
        except TypeError:
            pass

    def _on_tree_view_sim_cursor_change(self, widget, data = None):
        """ Is called if the location of the cursor within the treeview for the simulations changes. """
        try:
            # get selection of the treeview
            selection = self._tv_sim.get_selection()
            # set selection mode
            selection.set_mode(gtk.SELECTION_SINGLE)
            # get model and index of the selected item
            tv_model, tv_index = selection.get_selected()
            # index is the same as the indexth simulation
            self._selected_simulation = tv_model.get_value(tv_index, 1) # = Simulation
            self._selected_simulation_index = int(tv_model.get_value(tv_index, 2))
            # check if this key is available which means that a configuration can be loaded
            if self._simulations.has_key(self._selected_simulation_index):
                # set values
                self._ent_subplot_title.set_text(str(self._simulations[self._selected_simulation_index].title))
                self._ent_subplot_xlabel.set_text(str(self._simulations[self._selected_simulation_index].xlabel))
                self._ent_subplot_ylabel.set_text(str(self._simulations[self._selected_simulation_index].ylabel))
                self._check_button_subplot_title.set_active(self._simulations[self._selected_simulation_index].title_visibility)
                self._check_button_subplot_legend.set_active(self._simulations[self._selected_simulation_index].legend_visibility)
                self._ent_subplot_legend_position.set_text(str(self._simulations[self._selected_simulation_index].legend_position))
                self._ent_subplot_position.set_text(str(self._simulations[self._selected_simulation_index].subplot_position))
            else:
                # set default values
                self._ent_subplot_title.set_text(self._selected_simulation)
                self._ent_subplot_xlabel.set_text("Runtime")
                self._ent_subplot_ylabel.set_text("Marking")
                self._check_button_subplot_title.set_active(True)
                self._check_button_subplot_legend.set_active(True)
                self._ent_subplot_legend_position.set_text("0")
                self._ent_subplot_position.set_text("0")
        except TypeError:
            pass
                
    def _on_tree_view_toggle(cell, item, index, list_store):
        """ Is called if the status of a checkbos within a treeview changes. """

        # invert the value
        list_store[index][0] = not list_store[index][0]

    def _on_change_checkbutton(self, widget, data = None):
        """ Is called if the status of a checkbutton changes. """

        # read the status of the checkbutton which was changed and save it
        if data.lower() == "show legend":
            self._show_legend = widget.get_active()
        if data.lower() == "create subplots":
            self._create_subplots = widget.get_active()
        if data.lower() == "automatic color allocation":
            self._auto_color = widget.get_active()
        if data.lower() == "show title":
            self._show_title = widget.get_active()

    def _on_simulate_clicked(self, button):
        """ Is called if the simulation button sends the clicked event. """

        try:
            # read the simulation parameters and set them within the controller
            self._controller.run_time = float(self._ent_runtime.get_text())
            self._controller.time_step = float(self._ent_time_step.get_text())
            self._controller.number_simulations = int(self._ent_num_sim.get_text())        

            err = False

            # check parameters
            self._controller.epsilon = float(self._ent_epsilon.get_text())
            if self._controller.epsilon < 0 or self._controller.epsilon > 1:
                self.show_message_box_error("The parameter epsilon has to be between 0 and 1!")
                err = True

            self._controller.number_ssa_runs = int(self._ent_num_ssa_runs.get_text())
            if self._controller.number_ssa_runs < 0:
                self.show_message_box_error("The silon has to be between 0 and 1!")
                err = True

            self._controller.control_parameter = float(self._ent_control_parameter.get_text())
            if self._controller.control_parameter < 0:
                self.show_message_box_error("The control parameter has to be a positive integer (preferably between 2 and 20)!")
                err = True

            if not err:
                # run the simulation for the chosen algorithms
                if self._algorithm == self.A_GILLESPIE:
                    self._controller.gillespie_algorithm()
                    self.show_message_box_info("Simulation is finished!")
                if self._algorithm == self.A_TAULEAP:
                    self._controller.tauleap_algorithm()
                    self.show_message_box_info("Simulation is finished!")

        except ValueError:
            self.show_message_box_error("There are invalid entries!")

    def _on_ok_clicked(self, button):
        """ Is called if the OK button sends the clicked event. """

        try:
        # iteration through the list of places
            item =  self._p_list_store.get_iter_first()
            while (item != None):
                #print self._p_list_store.get_value(item, 0)
                # get key of the current place
                key = self._p_list_store.get_value(item, 1)
                if self._p_list_store.get_value(item, 0):
                    # check if a Trajectory object for the current place is available
                    if not self._places.has_key(key):
                        # create a new Trajectory object with standard values because the user didn't create one
                        t_obj = trajectory.Trajectory()
                        # set properties
                        t_obj.legend_text = self._p_list_store.get_value(item, 2)
                        t_obj.auto_color_allocation = True
                        # add Trajectory object to the dictionary
                        self._places[key] = t_obj
                else:
                    # remove invalid Trajectory object from the list
                    if self._places.has_key(key):
                        del self._places[key]
                # next item
                item = self._p_list_store.iter_next(item)

            # iteration through the list of simulations
            item =  self._sim_list_store.get_iter_first()
            ctr = 0
            ctr_subplot = 1
            while (item != None):
                ctr += 1
                if self._sim_list_store.get_value(item, 0):
                    # check if a Diagram object for the current simulation is available
                    if not self._simulations.has_key(ctr):
                        # create a new Diagram object with standard values because the user didn't create one
                        d_obj = diagram.Diagram()
                        # set properties
                        d_obj.title = self._sim_list_store.get_value(item, 1)
                        d_obj.xlabel = self._ent_xlabel.get_text()
                        d_obj.ylabel = self._ent_ylabel.get_text()
                        d_obj.legend_position = int(self._ent_legend_position.get_text())

                        # determine automatically the position of the subplot
                        ctr_subplot = 0
                        loop = True
                        while loop:
                            loop = False
                            for key, item_sim in self._simulations.items():
                                if ctr_subplot == item_sim.subplot_position:
                                    ctr_subplot += 1
                                    loop = True
                                    break

                        d_obj.subplot_position = int(ctr_subplot)
                        d_obj.title_visibility = self._check_button_title.get_active()
                        d_obj.legend_visibility = self._check_button_legend.get_active()

                        # add Diagram object to the dictionary
                        self._simulations[ctr] = d_obj
                else:
                    # remove invalid Diagram object
                    if self._simulations.has_key(ctr):
                        del self._simulations[ctr]
                # next item
                item = self._sim_list_store.iter_next(item)

            if len(self._simulations) == 0:
                self.show_message_box_error("Visualisation is not possible without any data!")
                return

            # set properties for the controller
            self._controller.simulations = self._simulations
            self._controller.run_time = float(self._ent_runtime.get_text())
            self._controller.time_step = float(self._ent_time_step.get_text())
            self._controller.number_simulations = int(self._ent_num_sim.get_text())
            self._controller.epsilon = float(self._ent_epsilon.get_text())
            self._controller.num_ssa_runs = int(self._ent_num_ssa_runs.get_text())
            self._controller.control_parameter = float(self._ent_control_parameter.get_text())
            self._controller.number_rows = int(self._ent_num_rows.get_text())
            self._controller.number_columns = int(self._ent_num_cols.get_text())
            self._controller.auto_subplot_position_allocation = self._check_button_auto_position_subplot.get_active()
            if self._controller.number_rows * self._controller.number_columns < self._controller.number_simulations:
                if self._create_subplots:
                    self.show_message_box_error("Invalid grid dimensions for the subplot!\nAll suplots will be allocated automatically.")
                self._controller.auto_subplot_position_allocation = True
            self._controller.title = self._ent_title.get_text()
            self._controller.title_visibility = self._check_button_title.get_active()
            self._controller.xlabel = self._ent_xlabel.get_text()
            self._controller.ylabel = self._ent_ylabel.get_text()
            self._controller.line_width = int(self._ent_line_width.get_text())
            self._controller.legend_position = int(self._ent_legend_position.get_text())
            self._controller.legend_visibility = self._check_button_legend.get_active()
            self._controller.subplots = self._create_subplots

            self._controller.trajectory_configuration = self._places
            # plot diagram
            self._controller.plot()
        except ValueError:
            self.show_message_box_error("There are invalid entries!")

    def _on_save_plot_clicked(self, button):
        """ Is called if the plot button sends the clicked event. """

        try:
            # create a new Trajectory object which stores the configuration of the chosen trajectory
            t_obj = trajectory.Trajectory()
            # set properties
            self._color = str(self._color)
            if len(self._color) >= 10:
                self._color = "#" + self._color[1] + self._color[2] + self._color[5] + self._color[6] + self._color[9] + self._color[10]
            else:
                 self._color = "#" + self._color[1] + self._color[2] + self._color[3] + self._color[4] + self._color[5] + self._color[6]
            t_obj.color = self._color
            t_obj.legend_text = self._ent_place_legend_text.get_text()
            t_obj.auto_color_allocation = self._check_button_auto_color.get_active()
            # add or replace the Trajectory object
            self._places[self._selected_place] = t_obj
        except ValueError:
            self.show_message_box_error("There are invalid entries!")

    def _on_save_sim_clicked(self, button):
        """ Is called if the save simulation button sends the clicked event. """

        try:
            # create a new Diagram object which stores the configuration of the chosen simulation
            d_obj = diagram.Diagram()
            # set properties
            d_obj.title = self._ent_subplot_title.get_text()
            d_obj.xlabel = self._ent_subplot_xlabel.get_text()
            d_obj.ylabel = self._ent_subplot_ylabel.get_text()
            d_obj.legend_position = int(self._ent_subplot_legend_position.get_text())
            d_obj.subplot_position = int(self._ent_subplot_position.get_text())
            d_obj.title_visibility = self._check_button_subplot_title.get_active()
            d_obj.legend_visibility = self._check_button_subplot_legend.get_active()
            # add or replace the Diagram object
            self._simulations[self._selected_simulation_index] = d_obj
        except ValueError:
            self.show_message_box_error("There are invalid entries!")

    def _on_cancel_clicked(self, button):
        """ Is called if the Cancel button sends the clicked event. """
        self._window.destroy()

    def _on_radio_button_changed(self, widget, data = None):
        """ Is called if the status of a radio button changes. """
        
        # determine which algorithm is chosen
        if widget.get_active() and data.lower() == "gillespie":
            self._algorithm = self.A_GILLESPIE
        if widget.get_active() and data.lower() == "tauleap":
            self._algorithm = self.A_TAULEAP

    def color_set_cb(self, colorbutton):
        """ Set the current colour. """
        self._color = self._color_button.get_color()

if __name__ == "__main__":
    app = ViewConfigurationSimulationDiagram()
    app.show()
    gtk.main()
