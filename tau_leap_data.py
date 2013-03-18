from sim_data import SimData

class TauLeapData(SimData):
    """
    Subclass of SimData for storing output data from Tau Leap SSA runs.

    Methods:
    __init__ : creates new object with instance variables initialised to none.

    """

    ##############################################
    ##  Class Constructor
    ##############################################

    def __init__(self):
        """ Initialises a new data storage object. """
        self._times = None
        self._markings = None
        self._event_freqs = None
        self._events = None
        self._iterations = None
