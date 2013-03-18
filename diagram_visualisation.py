#!/usr/bin/python

import matplotlib.pyplot as plt
import pylab

import trajectory
import diagram

class DiagramVisualisation(object):
    """ The DiagramVisualisation class is used to visualise the diagram and show it on the screen. It is possible to create subplots which are defined through multiple Diagram objects as well as combining them in one diagram. Different properties for this trajectory as well as the data for the x- and y-dimension can be set and all of these base on the matplotlib library. """ 

    _title = ""
    _num_rows = 1
    _num_cols = 1
    _legend_position = 0
    _auto_subplot = True
    _subplots = False
    _title_visibility = False
    _legend_visibility = True
    _line_width = 1

    # two dimensional - for multiple simulations
    _diagrams = dict()

    def __init__(self):   
        """ Constructor of DiagramVisualisation and default values will be initialised. """

        self._title = ""
        self._num_rows = 1
        self._num_cols = 1
        self._legend_position = 0
        self._auto_subplot = True
        self._subplots = False
        self._title_visibility = False
        self._legend_visibility = True
        self._line_width = 1

        # two dimensional - for multiple simulations
        self._diagrams = dict()

    @property
    def number_rows(self):
        """ Return number of rows for subplots. """
        return self._num_rows

    @property
    def number_cols(self):
        """ Return number of columns for subplots. """
        return self._num_cols

    @property
    def diagrams(self):
        """ Return diagrams (dictionary containing Diagram objects). """
        return self._diagrams

    @property
    def subplots(self):
        """ Return flag that define if subplots should be created. """
        return self._subplots

    @property
    def auto_subplot_allocation(self):
        """ Return flag for an automatic colour allocation. """
        return self._auto_subplot

    @property
    def line_width(self):
        """ Return line width of the trajectories. """
        return self._line_width

    @property
    def title(self):
        """ Return title. """
        return self._title

    @property
    def title_visibility(self):
        """ Return visibility of the title. """
        return self._title_visibility

    @property
    def legend_position(self):
        """ Return position of the legend. """
        return self._legend_position

    @property
    def legend_visibility(self):
        """ Return visibility of the legend. """
        return self._legend_visibility

    @number_rows.setter
    def number_rows(self, num):
        """ Set number of rows for subplots. """
        self._num_rows = int(num)
        if self._num_rows < 0:
            self._num_rows *= -1

    @number_cols.setter
    def number_cols(self, num):
        """ Set number of columns for subplots. """
        self._num_cols = num
        if self._num_cols < 0:
            self._num_cols *= -1

    @diagrams.setter
    def diagrams(self, diagrams):
        """ Return diagrams (dictionary containing Diagram objects). """
        self._diagrams = diagrams

    @auto_subplot_allocation.setter
    def auto_subplot_allocation(self, status):
        """ Set flag for an automatic colour allocation. """
        self._auto_subplot = status

    @subplots.setter
    def subplots(self, status):
        """ Set flag that define if subplots should be created. """
        self._subplots = status

    @line_width.setter
    def line_width(self, width):
        """ Set line width of the trajectories. """
        self._line_width = width
        if self._line_width < 0:
            self._line_width *= -1

    @title.setter
    def title(self, t):
        """ Set title. """
        self._title = t

    @legend_position.setter
    def legend_position(self, position):
        """ Set position of the legend. """
        self._legend_position = position

    @legend_visibility.setter
    def legend_visibility(self, visible):
        """ Set visibility of the legend. """
        self._legend_visibility = visible

    @title_visibility.setter
    def title_visibility(self, visible):
        """ Set visibility of the title. """
        self._title_visibility = visible

    def add(self, diagram, key):
        """ Add a diagram with a key that defines a collection of trajectories with associated properties. """
        self._diagrams[key] = diagram

    def remove(self, key):
        """ Remove a diagram defined through a key that defines a collection of trajectories with associated properties. """
        if self._diagrams.has_key(key):
            del self._diagrams[key]

    def plot(self):
	""" Create the actual visualisation of the whole diagram. """

        pylab.clf()

	# check if position of subplots will be assigned automatically
        if self._auto_subplot:
            # parameters
            num_diagrams = len(self._diagrams)
            num_rows = 1
            num_cols = 1

            loop = True
            while loop:
                # check if total number of possible diagrams is bigger than the actual number of diagrams
                total = int(num_rows * num_cols)
                if total >= num_diagrams:
                    # enough free slots
                    loop = False
                    self._num_rows = num_rows
                    self._num_cols = num_cols
                # adjust number of rows an columns
                if num_cols == num_rows:
                    # increase number of rows
                    num_rows += 1
                    while loop:
                        new_total = int(num_rows * num_cols)
                        if new_total <= total + 1:
                            break
                        else:
                            num_cols -= 1
                else:
                    num_cols += 1

	# position of the subplot
	pos = 1
	# legend descriptions
	legend = []

	# iteration through the defined diagrams
	for key, diagram in self._diagrams.items():
            # add new diagram to the visualisation
            self._add_plot(diagram, pos)
            # iteration through all trajectories
            for key, trajectory in diagram.trajectories.items():
                # create legend
                legend.append(trajectory.legend_text)
            # increasing the counter by 1
            pos += 1

        # check if no subplots need to be created
        if not self._subplots:
            # assigns the label of the x-axis
            pylab.xlabel(diagram.xlabel)
            # assigns the label of the y-axis
            pylab.ylabel(diagram.ylabel)
            # check if the legend is visible
            if self._legend_visibility:
                # add legend
                pylab.legend(legend, loc = self._legend_position)

        # check if title should be visible
        if self._title_visibility:
            # add title to visualisation
            pylab.suptitle(self._title)

	# displays the plots
	pylab.show()

    def _add_plot(self, diagram, subplot_position):
	""" Add a new plot defined through the parameter diagram to the already existing diagram. If subplots are used the parameter subplot_position defines the postion of the diagram. """

        ax = None
	# check if a subplot should be created
	if self._subplots:
            # create subplot
            ax = None
            # check if a position is set or the postion needs to be determined
            if not self._auto_subplot:
                # check if position is valid and add the subplot
                if diagram.subplot_position <= self._num_rows * self._num_cols:
                    ax = pylab.subplot(self._num_rows, self._num_cols, diagram.subplot_position)
                else:
                    ax = pylab.subplot(self._num_rows, self._num_cols, subplot_position)
            else:
                # add the subplot
                ax = pylab.subplot(self._num_rows, self._num_cols, subplot_position)
            # adjust visualisation property (vertical distance between subplots)
            pylab.subplots_adjust(hspace = 0.4)

        
        trajectories = []
        legend = []

        # adds all trajectories to the diagram
        for key, trajectory in diagram.trajectories.items():
            p = None
            # check if subplots need to be created
            if self._subplots:
                # check if colour needs to be allocated automatically
                if trajectory.auto_color_allocation:
                    # add plot
                    p, = ax.plot(trajectory.x_data, trajectory.y_data, linewidth = self._line_width, label = trajectory.legend_text)
                else:
                    # add plot
                    p, = ax.plot(trajectory.x_data, trajectory.y_data, color = trajectory.color, linewidth = self._line_width, label = trajectory.legend_text)

                # assigns the label of the x-axis
                ax.set_xlabel(diagram.xlabel)
                # assigns the label of the y-axis
                ax.set_ylabel(diagram.ylabel)
                # attaches the legend if it is visible
                #if diagram.legend_visibility:
                #    ax.legend(trajectories, legend, loc = diagram.legend_position)
            else:
                # check if each trajectory gets automatically a colour
                if trajectory.auto_color_allocation:
                    # add plot
                    pylab.plot(trajectory.x_data, trajectory.y_data, linewidth = self._line_width, label = trajectory.legend_text)
                else:
                    # add plot
                    pylab.plot(trajectory.x_data, trajectory.y_data, color = trajectory.color, linewidth = self._line_width, label = trajectory.legend_text)
                
            # check if legend should be visible
            if diagram.legend_visibility:
                if p != None:
                    # create legend
                    trajectories.append(p)
                    legend.append(trajectory.legend_text)

        # checks if subplots need to be created
        if self._subplots:
            # assigns the label of the x-axis
            pylab.xlabel(diagram.xlabel)
            # assigns the label of the y-axis
            pylab.ylabel(diagram.ylabel)
            
            # attaches the legend if it is visible
            if diagram.legend_visibility:
                ax.legend(trajectories, legend, loc = diagram.legend_position)

            # attaches the tile if it is visible
            if diagram.title_visibility: 
                pylab.title(diagram.title)
