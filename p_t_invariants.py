from invariants import Invariants

class PTInvariants(Invariants):
    """ Subclass of Invariants.

    Methods:
    - __init__ : initialises empty object; petri_net_data must be set explicitly.
    - calculate_p_invariants : interface method.
    - calculate_t_invariants : interface method.
    
    """

    ##############################################
    ##  Class Constructor
    ##############################################
    
    def __init__(self):
        """ Class constructor, all variables initialised to None. """
        self._petri_net_data = None
        self._stoichiometry_matrix = None


    ##############################################
    ##  Interface Methods
    ##############################################

    def calculate_p_invariants(self):
        """ Calculate P invariants and set as instance variable. """
        incidence_matrix = self._stoichiometry_matrix.T
        self._p_invariants = Invariants._calculate_invariants(self, incidence_matrix)

    def calculate_t_invariants(self):
        """ Calculate T invariants and set as instance variable. """
        incidence_matrix = self._stoichiometry_matrix
        self._t_invariants = Invariants._calculate_invariants(self, incidence_matrix)
