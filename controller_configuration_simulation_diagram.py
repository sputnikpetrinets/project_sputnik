#!/usr/bin/python

import copy

import model as m
import view_configuration_simulation_diagram
import controller_configuration_simulation

import numpy as np
import petri_net_data
import stoichiometry as stoich

import gillespie
import tau_leap

import trajectory
import diagram
import diagram_visualisation

class ControllerConfigurationSimulationDiagram(controller_configuration_simulation.ControllerConfigurationSimulation):
    """ The ControllerConfigurationSimulationDiagram class is a specific controller that inherits from the general ControllerConfigurationSimulation class and is used to manage the user interactions of the simulation configuration window and the application (ViewConfigurationConfigurationSimulationDiagram). """

    _run_time = 0
    _time_step = 0
    _num_simulations = 0
    _num_ssa_runs = 0
    _epsilon = 0
    _control_parameter = 0
    _num_rows = 1
    _num_cols = 1
    _title = "Simulation"
    _xlabel = "Runtime"
    _ylabel = "Marking"
    _legend_pos = 0
    _line_width = 1
    _legend = False
    _subplots = False
    _auto_color = True
    _auto_subplot = True
    _simulated = False
    _title_visibility = False
    _places = None
    _simulations = None

    def __init__(self):
        """ Constructor of ControllerConfigurationSimulationDiagram. """
        
        # call constructor of parent class
        controller_configuration_simulation.ControllerConfigurationSimulation.__init__(self)

        # set default values
        self._run_time = 0
        self._time_step = 0
        self._num_simulations = 0
        self._num_ssa_runs = 0
        self._epsilon = 0
        self._control_parameter = 0
        self._num_rows = 1
        self._num_cols = 1
        self._title = "Simulation"
        self._xlabel = "Runtime"
        self._ylabel = "Marking"
        self._legend_pos = 0
        self._line_width = 1
        self._legend = False
        self._subplots = False
        self._auto_color = True
        self._auto_subplot = True
        self._simulated = False
        self._title_visibility = False
        self._places = None
        self._simulations = None

    def __init__(self, model = None, view = None):
        """ Constructor of ControllerConfigurationSimulationDiagram. """
        
        # call constructor of parent class
        controller_configuration_simulation.ControllerConfigurationSimulation.__init__(self, model, view)

        # set default values
        self._run_time = 0
        self._time_step = 0
        self._num_simulations = 0
        self._num_ssa_runs = 0
        self._epsilon = 0
        self._control_parameter = 0
        self._num_rows = 1
        self._num_cols = 1
        self._title = "Simulation"
        self._xlabel = "Runtime"
        self._ylabel = "Marking"
        self._legend_pos = 0
        self._line_width = 1
        self._legend = False
        self._subplots = False
        self._auto_color = True
        self._auto_subplot = True
        self._simulated = False
        self._title_visibility = False
        self._places = None
        self._simulations = None

    @property
    def run_time(self):
        """ Return run time. """
        return self._run_time

    @property
    def time_step(self):
        """ Return time step. """
        return self._time_step

    @property
    def number_simulations(self):
        """ Return number of simulations. """
        return self._num_simulations

    @property
    def epsilon(self):
        """ Return epsilon. """
        return self._epsilon

    @property
    def control_parameter(self):
        """ Return control parameter. """
        return self._control_parameter

    @property
    def number_ssa_runs(self):
        """ Return number of SSA runs. """
        return self._num_ssa_runs

    @property
    def number_rows(self):
        """ Return number of rows. """
        return self._num_rows

    @property
    def number_columns(self):
        """ Return number of columns. """
        return self._num_cols

    @property
    def title(self):
        """ Return title. """
        return self._title

    @property
    def xlabel(self):
        """ Return label of the x axis. """
        return self._xlabel

    @property
    def ylabel(self):
        """ Return label of the y axis. """
        return self._ylabel

    @property
    def legend_position(self):
        """ Return legend position. """
        return self._legend_pos

    @property
    def line_width(self):
        """ Return line width. """
        return self._line_width

    @property
    def subplots(self):
        """ Return flag if subplots should be created. """
        return self._subplots

    @property
    def legend_visibility(self):
        """ Return visibility of the legend. """
        return self._legend

    @property
    def title_visibility(self):
        """ Return visibility of the title. """
        return self._title_visibility

    @property
    def auto_color_allocation(self):
        """ Return flag for an automatic colour allocation. """
        return self._auto_color

    @property
    def auto_subplot_position_allocation(self):
        """ Return flag for an automatic subplot position allocation. """
        return self._auto_subplot

    @property
    def trajectory_configuration(self):
        """ Return list of configurations for the single trajectories (dictionary key is the same as the label for the places). """
        return self._places

    @property
    def simulations(self):
        """ Return list of configurations for the single simulations (dictionary key is the ith simulation). """
        return self._simulations

    @run_time.setter
    def run_time(self, time):
        """ Set run time. """
        self._run_time = time

    @time_step.setter
    def time_step(self, step):
        """ Set time step. """
        self._time_step = step

    @number_simulations.setter
    def number_simulations(self, num):
        """ Set number of simulations. """
        self._num_simulations = num

    @epsilon.setter
    def epsilon(self, e):
        """ Set epsilon. """
        self._epsilon = e
        if self._epsilon < 0:
            self._epsilon *= -1

    @control_parameter.setter
    def control_parameter(self, c):
        """ Set control parameter. """
        self._control_parameter = c
        if self._control_parameter < 0:
            self._control_parameter *= -1

    @number_ssa_runs.setter
    def number_ssa_runs(self, r):
        """ Set number of SSA runs. """
        self._num_ssa_runs = r
        if self._num_ssa_runs < 0:
            self._num_ssa_runs *= -1

    @number_rows.setter
    def number_rows(self, num):
        """ Set number of rows. """
        self._num_rows = num
        if self._num_rows < 0:
            self._num_rows *= -1

    @number_columns.setter
    def number_columns(self, num):
        """ Set number of columns. """
        self._num_cols = num
        if self._num_cols < 0:
            self._num_cols *= -1

    @title.setter
    def title(self, title):
        """ Set title. """
        self._title = title

    @xlabel.setter
    def xlabel(self, label):
        """ Set label of the x axis. """
        self._xlabel = label

    @ylabel.setter
    def ylabel(self, label):
        """ Set label of the y axis. """
        self._ylabel = label

    @line_width.setter
    def line_width(self, width):
        """ Set line width. """
        self._line_width = width
        if self._line_width < 0:
            self._line_width *= -1

    @legend_position.setter
    def legend_position(self, pos):
        """ Set legend position. """
        self._legend_pos = pos

    @subplots.setter
    def subplots(self, visible):
        """ Set flag that labels if subplots should be created. """
        self._subplots = visible

    @legend_visibility.setter
    def legend_visibility(self, visible):
        """ Set visibility of the legend. """
        self._legend = visible

    @title_visibility.setter
    def title_visibility(self, visible):
        """ Set visibility of the title. """
        self._title_visibility = visible

    @auto_color_allocation.setter
    def auto_color_allocation(self, status):
        """ Set flag for an automatic colour allocation. """
        self._auto_color = status

    @auto_subplot_position_allocation.setter
    def auto_subplot_position_allocation(self, status):
        """ Set flag for an automatic subplot position allocation. """
        self._auto_subplot = status

    @trajectory_configuration.setter
    def trajectory_configuration(self, dictionary):
        """ Set dictionary of configurations for the single trajectories (dictionary key is the same as the label for the places). """
        self._places = dictionary

    @simulations.setter
    def simulations(self, dictionary):
        """ Set dictionary of configurations for the single simulations (dictionary key is the ith simulation). """
        self._simulations = dictionary

    def gillespie_algorithm(self):
        """ Execute Gillespie algorithm. """

        # instantiate an object used to simulate the petri net via a gillespie algorithms
        g = gillespie.Gillespie()
        # set properties
        g.petri_net = self._model.data.petri_net_data
        g.run_time = float(self._run_time)
        g.time_step = float(self._time_step)
        g.num_runs = int(self._num_simulations)
        # run simulation
        g.run_simulation()
        # set data
        self._model.output = g.simulation_data
        # set flag for the simulation process
        self._simulated = True

    def tauleap_algorithm(self):
        """ Execute Tau Leap algorithm. """

        # calculate stoichiometry properties needed for the tau leap algorithm
        self._model.data.petri_net_data.stoichiometry.calculate_consumed()
        self._model.data.petri_net_data.stoichiometry.calculate_species_hors()

        # recreate a PetriNetData object - issue with deepcopy
        p = petri_net_data.PetriNetData()
        s = stoich.Stoich()
        
        # set data
        s.pre_arcs = np.copy(self._model.data.petri_net_data.stoichiometry.pre_arcs)
        s.post_arcs = np.copy(self._model.data.petri_net_data.stoichiometry.post_arcs)
        s.calculate_stoichiometry_matrix()
        s.calculate_dependency_matrix()

        # these two are needed for Tau leap (not for gillespie)
        s.calculate_consumed()
        s.calculate_species_hors()

        # set properties
        p.stoichiometry = s
        p.places = np.copy(self._model.data.petri_net_data.places)
        p.transitions = np.copy(self._model.data.petri_net_data.transitions)
        p.rates = np.copy(self._model.data.petri_net_data.rates)
        p.initial_marking = np.copy(self._model.data.petri_net_data.initial_marking)

        # instantiate an object used to simulate the petri net via a tau leap algorithm
        t = tau_leap.TauLeap()
        # set properties
        t.petri_net = self._model.data.petri_net_data
        t.run_time = float(self._run_time)
        t.time_step = float(self._time_step)
        t.num_runs = int(self._num_simulations)
        t.epsilon = float(self._epsilon)
        t.control_parameter = float(self._control_parameter)
        t.num_ssa_runs = int(self._num_ssa_runs)
        # run simulation
        t.run_simulation()
        # set data
        self._model.output = t.simulation_data
        self._simulated = True

    def plot(self):

        # check if the simulation was executed before
        if not self._simulated:
            # abort method
            return

        # instantiate a general object that includes the single diagrams
        vis = diagram_visualisation.DiagramVisualisation()
        # set properties
        vis.title = self._title
        vis.legend_visibility = self._legend
        vis.title_visibility = self._title_visibility
        vis.subplots = self._subplots
        vis.number_rows = self._num_rows
        vis.number_cols = self._num_cols
        vis.auto_subplot_allocation = self._auto_subplot
        vis.line_width = self._line_width

        try:
            # iteration through all simulations
            for index_sim, item_sim in self._simulations.items():
                # recreate the object - otherwise you would have a referencing problem
                # instantiate an object that combines single trajectories
                d_obj = diagram.Diagram()
                # set properties
                d_obj.title = item_sim.title
                if not self._subplots:
                    d_obj.xlabel = self._xlabel
                    d_obj.ylabel = self._ylabel
                else:
                    d_obj.xlabel = item_sim.xlabel
                    d_obj.ylabel = item_sim.ylabel
                d_obj.legend_position = int(item_sim.legend_position)
                d_obj.subplot_position = int(item_sim.subplot_position)
                d_obj.title_visibility = item_sim.title_visibility
                d_obj.legend_visibility = item_sim.legend_visibility
                # determine x data
                x = []
                for i in range(len(self._model.output[index_sim - 1].times)):
                    x.append(self._model.output[index_sim - 1].times[i])

                # iteration through all trajectories
                for key, item in self._places.items():
                    # recreate the object - otherwise you would have a referencing problem
                    # instantiate a trajectory object
                    t_obj = trajectory.Trajectory()
                    # set properties
                    t_obj.color = item.color
                    t_obj.legend_text = item.legend_text
                    if not self._subplots and len(self._simulations) > 1:
                        t_obj.legend_text = t_obj.legend_text + " - Simulation " + str(index_sim)
                    t_obj.auto_color_allocation = item.auto_color_allocation
                    # set trajectory data
                    t_obj.x_data = copy.deepcopy(x)
                    t_obj.y_data = []
                    index = -1
                    for i in range(len(self._model.data.petri_net_data.places)):
                        if self._model.data.petri_net_data.places[i] == key:
                            index = i
                            break
                    if index != -1:
                        for i in range(len(self._model.output[index_sim - 1].markings)):
                            t_obj.y_data.append(self._model.output[index_sim - 1].markings[i][index])
                    # add trajectory object to the diagram object
                    d_obj.add(t_obj, t_obj.legend_text)

                    if len(self._simulations) == 1 and self._subplots:
                        d_obj_t = diagram.Diagram()
                        # set properties
                        d_obj_t.title = item.legend_text
                        if not self._subplots:
                            d_obj_t.xlabel = self._xlabel
                            d_obj_t.ylabel = self._ylabel
                        else:
                            d_obj_t.xlabel = item_sim.xlabel
                            d_obj_t.ylabel = item_sim.ylabel
                        d_obj_t.legend_position = int(item_sim.legend_position)
                        #d_obj_t.subplot_position = int(item_sim.subplot_position)
                        d_obj_t.title_visibility = item_sim.title_visibility
                        d_obj_t.legend_visibility = item_sim.legend_visibility
                        # add trajectory object to the diagram object
                        d_obj_t.add(t_obj, t_obj.legend_text)
                        vis.add(d_obj_t, d_obj_t.title)

                if len(self._simulations) > 1 or not self._subplots:
                    # add diagram object to the visualisation object
                    vis.add(d_obj, d_obj.title)
            # visualise diagrams
            vis.plot()
        except IndexError:
            print "Simulation needs to be executed after changing simulation parameter. "
