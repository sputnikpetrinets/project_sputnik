import numpy as np
import math

class Invariants(object):
    """
    Abstract base class for calculating invariants.

    Instance Variables:
    - _petri_net_data
    - p_invariants
    - t_invariants

    Interface Method:
    - calculate_invariants: private, accessed by PTInvariants object.

    Private Methods:
    - get_new_line
    - remove_lines
    - check_new_line
    - minimal_only
    - factorize

    """

    ##############################################
    ##  Instance Variables: Getters and Setters
    ##############################################
    
    def set_petri_net(self, p):
        """ Set petri net as PetriNetDat object that is passed. """
        self._petri_net_data = p
        self._stoichiometry_matrix = self._petri_net_data.stoichiometry.stoichiometry_matrix

    @property
    def p_invariants(self):
        """ Return P invariants (?xP array). """
        return self._p_invariants
    
    @property
    def t_invariants(self):
        """ Return T invariants (?xT array). """
        return self._t_invariants


    ##############################################
    ##  Interface Method
    ##############################################

    def _calculate_invariants(self, a_matrix):
        """ Calculate invariants of a given input matrix A. """
        # Concatenate stoichiometry / incidence matrix A with an identity matrix.
        # This new matrix is called Q
        a_height = a_matrix.shape[0]
        a_width = a_matrix.shape[1]
        i_matrix = np.identity(a_height, int)
        q_matrix = np.concatenate((a_matrix, i_matrix), axis = 1)
        # For each column i in matrix Q from A carry out simple row operations
        for i in range(0, a_width):
            # Add to matrix Q as many lines l as there are linear combinations
            # of two lines, with positive integer coefficients, such that
            # element[l, i] is zero.
            q_height = q_matrix.shape[0]
            for j in range(0, q_height-1):
                j_val = q_matrix[j, i]
                for k in range(j+1, q_height):
                    k_val = q_matrix[k, i]
                    if (j_val < 0 and k_val > 0) or (j_val > 0 and k_val < 0):
                        new_line = Invariants.__get_new_line(self,
                            q_matrix, j, k, j_val, k_val)
                        q_matrix = np.vstack((q_matrix, new_line))
            # Eliminate from matrix Q all the lines l whose element [l, i] is
            # not zero.
            q_matrix = Invariants.__remove_lines(self, q_matrix, i)
            if q_matrix.shape[0] == 0:
                break
        # Remove A' from Q
        q_matrix = q_matrix[:, a_width:]
        if q_matrix.shape[0] != 0:
            # Remove zero lines from Q
            q_matrix = Invariants.__check_empty_line(self, q_matrix)
            # Eliminate non-minimal invariants from Q
            q_matrix = Invariants.__minimal_only(self, q_matrix)
            # Simplify invariants if possible
            q_matrix = Invariants.__factorize(self, q_matrix)
        return q_matrix


    ##############################################
    ##  Private Methods
    ##############################################

    def __get_new_line(self, matrix, j, k, j_val, k_val):
        """ Produce new line from j and k such that ith element is zero. """
        if j_val + k_val == 0:
            j_coef = 1
            k_coef = 1
        elif j_val > 0:
            j_coef = -k_val
            k_coef = j_val
        elif j_val < 0:
            j_coef = k_val
            k_coef = -j_val
        j_line = matrix[j,:]
        k_line = matrix[k,:]
        new_line = j_coef * j_line + k_coef * k_line
        return new_line

    def __remove_lines(self, matrix, column):
        """ Remove all lines j where element [j, i] is not zero. """
        height = matrix.shape[0]
        del_list = np.array([], dtype = np.int)
        for j in range(0, height):
                if matrix[j, column] != 0:
                    del_list = np.append(del_list, [j])
        matrix = np.delete(matrix, del_list, 0)
        return matrix

    def __check_empty_line(self, matrix):
        """ Remove all-zero lines. """
        height = matrix.shape[0]
        del_list = np.array([], dtype = np.int)
        for i in range(0, height):
            line = matrix[i,:]
            line_check = np.equal(line, 0)
            if line_check.all():
                del_list = np.append(del_list, [i])
        matrix = np.delete(matrix, del_list, 0)
        return matrix

    def __minimal_only(self, matrix):
        """
        For pairs of lines j, k, if the support of line k is a superset
        of the support of j, line k is removed.

        """
        height = matrix.shape[0]
        del_list = np.array([], dtype = np.int)
        for j in range(0, height):
            if j not in del_list:
                j_line = matrix[j,:]
                j_support = np.not_equal(j_line, 0)
                for k in range(0, height):
                    if j != k and k not in del_list:
                        k_line = matrix[k,:]
                        k_support = np.not_equal(k_line, 0)
                        support_overlap = np.logical_and(j_support, k_support)
                        if np.equal(j_support, support_overlap).all():
                            del_list = np.append(del_list, [k])
        matrix = np.delete(matrix, del_list, 0)
        return matrix

    def __factorize(self, matrix):
        """
        For invariants whose smallest non-zero element c is >1, the line
        is simplified if possibe by testing for divisibility through factors 
        of c.

        """
        height = matrix.shape[0]
        masked_matrix = np.ma.masked_equal(matrix, 0, copy=False)
        for i in range(0, height):
            line = matrix[i,:]
            min_val = masked_matrix[i,:].min()
            if min_val != 1:
                max_factor = int(math.floor(math.sqrt(min_val) + 1))
                factors = reduce(list.__add__, ([i, min_val//i] \
                        for i in range(1, max_factor) if min_val % i == 0))
                factors.sort(reverse=True)
                factors.pop()
                for j in range(0, len(factors)):
                    if np.equal(line % factors[j], 0).all():
                        line = line // factors[j]
                        matrix[i,:] = line
                        break
        return matrix
