import numpy as np

class PetriNetData(object):
    """
    Contains data elements for a given petri net.
    Constructor initialises empty object; data elements must be set explicitly.

    Variables:
    - Mandatory: places, transitions, rates, initial_marking, stoichiometry.
    - Optional: test_arcs, inhibitory_arcs, capacities.

    Methods:
    - __init__: initialises empty PetriNetData object.
    - clone: returns copy of PetriNetData object.

    """

    ##############################################
    ##  Class Constructor
    ##############################################
    
    def __init__(self):
        """ Initialise empty PetriNetData object. """
        self.__places = None
        self.__transitions = None
        self.__test_arcs = None
        self.__inhibitory_arcs = None
        self.__capacities = None
        self.__rates = None
        self.__initial_marking = None
        self.__stoichiometry = None
        

    ##############################################
    ##  Instance Variables: Getters and Setters
    ##############################################

    @property
    def places(self):
        """ Return places. """
        return self.__places

    @places.setter
    def places(self, p):
        """ Set places (1D array). """
        self.__places = p
    
    @property
    def transitions(self):
        """ Return transitions. """
        return self.__transitions

    @transitions.setter
    def transitions(self, t):
        """ Set transitions (1D array of length T). """
        self.__transitions = t

    @property
    def rates(self):
        """ Return rates. """
        return self.__rates

    @rates.setter
    def rates(self, r):
        """ Set rates (1D array of length T). """
        self.__rates = r

    @property
    def initial_marking(self):
        """ Return initial marking. """
        return self.__initial_marking

    @initial_marking.setter
    def initial_marking(self, m0):
        """ Set initial marking (1D array length P). """
        self.__initial_marking = m0
        
    @property
    def stoichiometry(self):
        """ Return stoichiometry object. """
        return self.__stoichiometry

    @stoichiometry.setter
    def stoichiometry(self, s):
        """ Set stoichiometry (object of Stoichiometry class). """
        self.__stoichiometry = s

    @property
    def test_arcs(self):
        """ Return test arcs. """
        return self.__test_arcs

    @test_arcs.setter
    def test_arcs(self, test):
        """ Set test arcs (optional, matrix of dimensions TxP). """
        self.__test_arcs = test

    @property
    def inhibitory_arcs(self):
        """ Return inhibitory arcs. """
        return self.__inhibitory_arcs

    @inhibitory_arcs.setter
    def inhibitory_arcs(self, inhib):
        """ Set inhibitory arcs (optional, matrix of dimensions TxP). """
        self.__inhibitory_arcs = inhib

    @property
    def capacities(self):
        """ Return capacities. """
        return self.__capacities

    @capacities.setter
    def capacities(self, c):
        """ Set capacities (optional, 1D array of length P). """
        self.__capacities = c


    ##############################################
    ##  Clone Method
    ##############################################
        
    def clone(self):
        """ Return copy of PetriNetData object. """
        data = PetriNetData()
        data.places = np.copy(self.places)
        data.transitions = np.copy(self.transitions)
        if self.test_arcs != None:
            data.test_arcs = np.copy(self.test_arcs)
        if self.inhibitory_arcs != None:
            data.inhibitory_arcs = np.copy(self.inhibitory_arcs)
        if self.capacities != None:
            data.capacities = np.copy(self.capacities)
        data.rates = np.copy(self.rates)
        data.initial_marking = np.copy(self.initial_marking)
        try:
            data.stoichiometry = self.stoichiometry.clone()
        except AttributeError:
            data.stoichiometry = None
        return data
