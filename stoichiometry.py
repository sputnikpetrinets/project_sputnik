import numpy as np

class Stoich(object):
    """
    Contains stoichiometry data elements for a given petri net.
    Constructor initialises empty object; data elements must be set explicitly.

    Instance Variables:
    - Set manually: pre_arcs, post_arcs.
    - Calculated via class methods:
        - stoichiometry_matrix
        - dependency_matrix
        - consumed_matrix
        - species_hors.

    Interface Methods:
    - calculate_stoichiometry_matrix
    - calculate_dependency_matrix
    - calculate_consumed
    - calculate_species_hors
    - clone: returns copy of PetriNetData object.

    Other methods:
    - __init__: initialises empty Stoich object.

    """

    ##############################################
    ##  Class Constructor
    ##############################################

    def __init__(self):
        """ Class constructor, all variables initialised to None. """
        self.__pre_arcs = None
        self.__post_arcs = None
        self.__stoichiometry_matrix = None
        self.__dependency_matrix = None
        self.__consumed_matrix = None
        self.__species_hors = None


    ##############################################
    ##  Instance Variables: Getters and Setters
    ##############################################
        
    @property
    def pre_arcs(self):
        """ Return pre arcs. """
        return self.__pre_arcs

    @pre_arcs.setter
    def pre_arcs(self, pre):
        """ Set pre arcs (matrix of dimension TxP). """
        self.__pre_arcs = pre
    
    @property
    def post_arcs(self):
        """ Return post arcs. """
        return self.__post_arcs

    @post_arcs.setter
    def post_arcs(self, post):
        """ Set post arcs (matrix of dimension TxP). """
        self.__post_arcs = post

    @property
    def stoichiometry_matrix(self):
        """ Return stoichiometry matrix. """
        return self.__stoichiometry_matrix

    @stoichiometry_matrix.setter
    def stoichiometry_matrix(self, matrix):
        """ Set stoichiometry matrix (matrix of dimension TxP). """
        self.__stoichiometry_matrix = matrix

    @property
    def dependency_matrix(self):
        """ Return dependency matrix. """
        return self.__dependency_matrix

    @dependency_matrix.setter
    def dependency_matrix(self, matrix):
        """ Set stoichiometry matrix (matrix of dimension TxP). """
        self.__dependency_matrix = matrix

    @property
    def consumed_matrix(self):
        """ Return consumed matrix. """
        return self.__consumed_matrix

    @consumed_matrix.setter
    def consumed_matrix(self, c):
        """ Set consumed (matrix of dimension TxP). """
        self.__consumed_matrix = c

    @property
    def species_hors(self):
        """ Return species' highest order of reaction. """
        return self.__species_hors

    @species_hors.setter
    def species_hors(self, s):
        """ Set species' highest order of reaction (2D array of dimension Px2). """
        self.__species_hors = s


    ##############################################
    ##  Calculation Methods
    ##############################################

    def calculate_stoichiometry_matrix(self):
        """ Calculate stoichiometry matrix from pre and post arcs and set as instance variable. """
        self.__stoichiometry_matrix = self.__post_arcs - self.__pre_arcs

    def calculate_dependency_matrix(self):
        """
        Calculate dependency matrix and set as instance variable.
        Requires stoichiometry matrix to be calculated prior.

        """        
        pre_arcs = self.pre_arcs
        stoichiometry_matrix = np.asarray(self.stoichiometry_matrix)
        num_places = stoichiometry_matrix.shape[1]
        num_transitions = stoichiometry_matrix.shape[0]
        dependency_matrix = np.zeros((num_transitions, num_transitions), dtype=int)
        places = range(num_places)
        transitions = range(num_transitions)
        for i in transitions:
            marking_change = stoichiometry_matrix[i,:]
            for j in places:
                place_change = marking_change[j]
                if place_change != 0:
                    affected_transitions = pre_arcs[:,j]
                    for k in transitions:
                        if affected_transitions[k] != 0:
                            dependency_matrix[i, k] = 1
        self.dependency_matrix = np.asmatrix(dependency_matrix)

    def calculate_consumed(self):
        """
        Calculate matrix of species consumed by each reaction.
        Needed for Tau Leap simulation.
        Requires stoichiometry matrix to be calculated prior.

        """
        stoichiometry_matrix = self.stoichiometry_matrix
        self.consumed_matrix = np.where(stoichiometry_matrix < 0, abs(stoichiometry_matrix), 0)

    def calculate_species_hors(self):
        """
        Calculate species' highest order of reaction.
        2D array of dimension Px2.
        1st column gives highest order of reactant of ith species.
        2nd column gives number of molecules of i involved in that reaction.
        Needed for Tau Leap simulation.
        Requires stoichiometry matrix and consumed matrix to be calculated prior.

        """
        pre_arcs = self.pre_arcs
        num_places = pre_arcs.shape[1]
        stoichiometry_matrix = self.stoichiometry_matrix
        # Reaction order vector is 1D array of length T
        reaction_order_vector = np.sum(pre_arcs, axis=1)
        species_hors = np.zeros((num_places, 2), dtype=int)
        for j in range(num_places):
            species_input = pre_arcs[:, j]
            # Calculate orders of reactions species j partakes in
            species_reaction_orders = np.where(species_input != 0, reaction_order_vector, 0)
            # Calculate highest order reaction species j partakes in
            species_hor = species_reaction_orders.max()
            # Calculate stoichiometry of j in highest order reactions
            species_hor_inputs = np.where(species_reaction_orders == species_hor, species_input, 0)
            # Fill array with calculated values
            species_hors[j, 0] = species_hor
            species_hors[j, 1] = species_hor_inputs.max()
        self.species_hors = species_hors


    ##############################################
    ##  Clone Method
    ##############################################

    def clone(self):
        """ Return copy of Stoich object. """
        s = Stoich()
        s.pre_arcs = np.copy(self.pre_arcs)
        s.post_arcs = np.copy(self.post_arcs)
        s.stoichiometry_matrix = np.copy(self.stoichiometry_matrix)
        s.dependency_matrix = np.copy(self.dependency_matrix)
        if self.consumed_matrix != None:
            s.consumed_matrix = np.copy(self.consumed_matrix)
        if self.species_hors != None:
            s.species_hors = np.copy(self.species_hors)
        return s
