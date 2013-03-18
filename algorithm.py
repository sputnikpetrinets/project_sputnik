class Algorithm(object):
    """
    Abstract base class providing general methods and properties for each simulation
    algorithm

    Instance Variables:
    - petri_net
    - run_time
    - time_step
    - num_iterations
    - num_runs
    - algorithm
    - simulation_data

    Interface Method:
    - run_simulation

    """

    ##############################################
    ##  Instance Variables: Getters and Setters
    ##############################################
    
    @property
    def petri_net(self):
        """ Return petri net to be simulated. """
        return self._petri_net

    @petri_net.setter
    def petri_net(self, p):
        """ Set petri net data object to be simulated. """
        self._petri_net = p

    @property
    def run_time(self):
        """ Return run time of simulation. """
        return self._run_time

    @run_time.setter
    def run_time(self, t):
        """ Set run time for simulation(s). """
        self._run_time = t
        
    @property
    def time_step(self):
        """ Return time step for simulation. """
        return self._time_step

    @time_step.setter
    def time_step(self, t):
        """ Set time step for simulation. """
        self._time_step = t
        
    @property
    def num_iterations(self):
        """ Return number of iterations to be run. """
        return self._num_iterations

    @num_iterations.setter
    def num_iterations(self, n):
        """ Set number of iterations to be run. """
        self._num_iterations = int(n)
        
    @property
    def num_runs(self):
        """ Return number of simulations to be run. """
        return self._num_runs

    @num_runs.setter
    def num_runs(self, n):
        """ Set number of simulations to be run. """
        self._num_runs = n

    @property
    def algorithm(self):
        """ Return algorithm of subclass instance. """
        return self._algorithm
        
    @property
    def simulation_data(self):
        """ Return list of objects containing output data for each run. """
        return self._simulation_data
    

    ##############################################
    ##  Interface Method
    ##############################################
        
    def run_simulation(self):
        """ Runs simulation algorithm for specified number of runs, stores
        output data in new objects, and returns list of these objects. """
        for run in range(0, self._num_runs):
            run_output = self._algorithm(self)
            self._simulation_data.append(run_output)
