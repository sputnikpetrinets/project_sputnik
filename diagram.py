#!/usr/bin/python

class Diagram(object):
    """ The Diagram class is used to define a diagram which can contain multiple trajectories. Different properties can be set and all of these base on the matplotlib library. """

    _title = ""
    _xlabel = ""
    _ylabel = ""
    _legend_pos = 0
    _subplot_pos = 1
    _legend = False
    _title_visibility = False
    _auto_color = True
        
    # can contain multiple trajectories
    _trajectories = dict()

    def __init__(self):
        """ Constructor of Diagram and default values will be initialised. """

        self._title = ""
        self._xlabel = ""
        self._ylabel = ""
        self._legend_pos = 0
        self._subplot_pos = 1
        self._legend = False
        self._title_visibility = False
        self._auto_color = True
        
        # can contain multiple trajectories
        self._trajectories = dict()

    @property
    def title(self):
        """ Return title. """
        return self._title

    @property
    def xlabel(self):
        """ Return description of the x-axis. """
        return self._xlabel

    @property
    def ylabel(self):
        """ Return description of the y-axis. """
        return self._ylabel

    @property
    def legend_position(self):
        """ Return the position of the legend. """
        return self._legend_pos
    
    @property
    def subplot_position(self):
        """ Return the position of the subplot. """
        return self._subplot_pos

    @property
    def title_visibility(self):
        """ Return visibility of the title. """
        return self._title_visibility

    @property
    def legend_visibility(self):
        """ Return visibility of the legend. """
        return self._legend

    @property
    def auto_color_allocation(self):
        """ Return flag for an automatic colour allocation. """
        return self._auto_color

    @property
    def trajectories(self):
        """ Return trajectories. """
        return self._trajectories

    @title.setter
    def title(self, title):
        """ Set title. """
        self._title = title

    @xlabel.setter
    def xlabel(self, label):
        """ Set description of the x-axis. """
        self._xlabel = label

    @ylabel.setter
    def ylabel(self, label):
        """ Set description of the y-axis. """
        self._ylabel = label

    @legend_position.setter
    def legend_position(self, pos):
        """ Set position for the legend. """
        self._legend_pos = pos

    @subplot_position.setter
    def subplot_position(self, pos):
        """ Set position for a subplot. """
        self._subplot_pos = pos

    @title_visibility.setter
    def title_visibility(self, visible):
        """ Set visibility of the title. """
        self._title_visibility = visible

    @legend_visibility.setter
    def legend_visibility(self, visible):
        """ Set visibility of the legend. """
        self._legend = visible

    @auto_color_allocation.setter
    def auto_color_allocation(self, status):
        """ Set flag for an automatic colour allocation. """
        self._auto_color = status

    @trajectories.setter
    def trajectories(self, trajectories):
        """ Set trajectories. """
        self._trajectories = trajectories

    def add(self, trajectory, key):
        """ Add a trajectory with a key that defines the trajectory. """
        self._trajectories[key] = trajectory

    def remove(self, key):
        """ Remove a trajectory based on the key. """
        if self._trajectories.has_key(key):
            del self._trajectories[key]
            
