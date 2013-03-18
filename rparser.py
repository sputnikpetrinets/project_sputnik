class RParser(object):
    """
    Class containing parser which converts a list of token objects to a
    PetriNetData class
    """
    def __init__(self):
        self.data = None
        
    def parse(self):
        """
        Takes a list of token objects (outputted from a lexer) and returns
        a PetriNetObject with set parameters for the token values contained
        in the list of tokens.
        """
        import petri_net_data as ep
        import stoichiometry as es
        
        t_list = self.data
        self._spn = ep.PetriNetData()
        self._spn_s = es.Stoich()
        #parsed = {'p':'places','t':'transitions', 'pre':''
        for n in range(0, len(t_list)):
            if t_list[n].label == 'p':
                self._spn.places = t_list[n].value
            if t_list[n].label == 't':
                self._spn.transitions = t_list[n].value
            if t_list[n].label == 'pre':
                self._spn_s.pre_arcs = t_list[n].value
            if t_list[n].label == 'post':
                self._spn_s.post_arcs = t_list[n].value
            if t_list[n].label == 'test':
                self._spn.test_arcs = t_list[n].value
            if t_list[n].label == 'inhib':
                self._spn.inhibitory_arcs = t_list[n].value
            if t_list[n].label == 'c':
                self._spn.capacities = t_list[n].value
            if t_list[n].label == 'r':
                self._spn.rates = t_list[n].value
            if t_list[n].label == 'm':
                self._spn.initial_marking = t_list[n].value
        # Prerequisite functions for any stochastic smulation
        self._spn_s.calculate_stoichiometry_matrix()
        self._spn_s.calculate_dependency_matrix()
        # Functions for Tau-leap simulation
        self._spn_s.calculate_consumed()
        self._spn_s.calculate_species_hors()
        self._spn.stoichiometry = self._spn_s

    @property
    def output(self):
        return self._spn
