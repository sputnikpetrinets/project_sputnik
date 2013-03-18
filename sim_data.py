class SimData(object):
    """
    Abstract class; subclass instances store output data for an individual simulation run.

    Instance Variables:
    - times
    - markings
    - event_freqs
    - events
    - iterations

    """

    ##############################################
    ##  Instance Variables: Getters and Setters
    ##############################################
    
    @property
    def times(self):
        """ 1D array of times corresponding to marking data. """
        return self._times

    @times.setter
    def times(self, t):
        """ Stores times. """
        self._times = t
        
    @property
    def markings(self):
        """
        2D array of marking data for each timepoint in times.
        Dimensions: len(times) x P

        """
        return self._markings

    @markings.setter
    def markings(self, m):
        """ Stores the markings. """
        self._markings = m

    @property
    def events(self):
        """
        Array of events (transitions) that occurred between each timepoint in times.
        Dimensions: i x 

        """
        return self._events

    @events.setter
    def events(self, e):
        """ Stores the events. """
        self._events = e
        
    @property
    def event_freqs(self):
        """ List (length T) giving number of times each transition fired during simulation. """
        return self._event_freqs

    @event_freqs.setter
    def event_freqs(self, e):
        """ Stores the event frequencies. """
        self._event_freqs = e

    @property
    def iterations(self):
        """ Number of iterations simulated. """
        return self._iterations

    @iterations.setter
    def iterations(self, i):
        """ Stores the number of iterations. """
        self._iterations = i
