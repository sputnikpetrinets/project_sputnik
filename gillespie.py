from algorithm import Algorithm
import gillespie_data
import numpy as np
import random
import math

class Gillespie(Algorithm):
    """
    Subclass of Algorithm, allows Gillespie stochastic simulation algorithm (SSA) to
    be run, for a specified run time or number of iterations, for a specified number of runs.

    Methods:
    __init__
    gillespie: protected, accessed by Algorithm.run_simulation
    
    """

    ##############################################
    ##  Class Constructor
    ##############################################
    
    def __init__(self):
        self._petri_net = None
        self._run_time = None
        self._num_runs = 1
        self._time_step = None
        self._num_iterations = None
        self._simulation_data = []
        self._algorithm = Gillespie._gillespie


    ##############################################
    ##  Simulation Algorithm
    ##############################################
        
    def _gillespie(self):
        """ Run the Gillespie algorithm for the specified petri net and simulation variables. """
        
        # Petri net data to local variables
        try:
            data = self._petri_net
        except:
            print 'Error: petri_net not set.'
            return
        try:
            pre_arcs = np.asarray(data.stoichiometry.pre_arcs, dtype=int)
            num_transitions = pre_arcs.shape[0]
            num_places = pre_arcs.shape[1]
        except:
            print 'Error: pre_arcs missing.'
            return
        try:
            rates = np.asarray(data.rates, dtype=float)
        except:
            print 'Error: rates missing.'
            return
        try:
            initial_marking = data.initial_marking
        except:
            print 'Error: initial_marking missing.'
            return
        try:
            stoichiometry_matrix = np.asarray(data.stoichiometry.stoichiometry_matrix, dtype=int)
            dependency_matrix = np.asarray(data.stoichiometry.dependency_matrix, dtype=int)
            dependency_matrix = np.vstack((dependency_matrix, np.ones(num_transitions, dtype=int)))
        except:
            print 'Error: calculate stoichiometry_matrix and dependency_matrix'
            return
        capacities = data.capacities
        if capacities != None:
            capacities = np.asarray(capacities, dtype=int)
        test_arcs = data.test_arcs
        if test_arcs != None:
            test_arcs = np.asarray(test_arcs, dtype=int)
            test_vector = np.any(test_arcs, axis=1)
        inhibitory_arcs = data.inhibitory_arcs
        if inhibitory_arcs != None:
            inhibitory_arcs = np.asarray(inhibitory_arcs, dtype=int)
            inhib_vector = np.any(inhibitory_arcs, axis=1)

        # Simulation variables to local variables
        num_iterations = self.num_iterations
        run_time = self.run_time
        time_step = self.time_step
        if not num_iterations:
            if not run_time or not time_step:
                print 'Error: specify num_iterations or both run_time and time_step.'
                return
            else:
                by_iteration = False
        else:
            by_iteration = True

        # Dot eliminators
        random_unif = random.random
        random_exp = random.expovariate
        local_sum = sum
        local_any = any
        local_less = np.less
        local_logical_and = np.logical_and
        local_greater = np.greater
        local_greater_equal = np.greater_equal

        # Ranges
        transitions = range(num_transitions)
        places = range(num_places)

        # Algorithm data storage initialisation
        current_time = 0
        current_marking = np.copy(initial_marking)
        event_freqs = [0] * num_transitions
        local_hazards = [0] * num_transitions
        channel = num_transitions
        if by_iteration:
            record_points = num_iterations + 1
            time_array = np.zeros(record_points, dtype=float)
            events = np.zeros(record_points - 1, dtype=int)
        else:
            time_array = np.arange(0, run_time + time_step, time_step, dtype=float)
            record_points = len(time_array)
            events = np.zeros((record_points - 1, num_transitions), dtype=int)
        marking_array = np.zeros((record_points, num_places), dtype=int)
        marking_array[0, :] = np.copy(initial_marking)
        record_points = range(1, record_points)
        
        # Simulation algorithm
        for i in record_points:
            # Extra loop required when by_iteration == False
            while 1:
                # Check if waiting time jumped past multiple timepoints
                if not by_iteration:
                    if current_time >= time_array[i]:
                        break
                # Calculate local hazards for each transition
                for j in transitions:
                    # Check if local hazard needs to be recalculated
                    if dependency_matrix[channel, j] == 0:
                        pass
                    # Check if test arcs, inhibitory arcs or capacities block transition
                    elif test_arcs != None and test_vector[j] and local_any(local_less(current_marking, test_arcs[j,:])):
                        local_hazards[j] = 0
                    elif inhibitory_arcs != None and inhib_vector[j] and local_any(local_logical_and(
                            local_greater_equal(current_marking, inhibitory_arcs[j,:]), local_greater(inhibitory_arcs[j,:], 0))):
                        local_hazards[j] = 0
                    elif capacities != None and local_any(local_logical_and(local_greater(
                            (current_marking + stoichiometry_matrix[j,:]), capacities), local_greater(capacities, 0))):
                        local_hazards[j] = 0
                    # Otherwise calculate local hazard
                    else:
                        partial_hazard = 1
                        for k in places:
                            stoichiometry = pre_arcs[j, k]
                            if stoichiometry == 0:
                                pass
                            elif stoichiometry == 1:
                                partial_hazard *= current_marking[k]
                            else:
                                species_amount = current_marking[k]
                                if species_amount >= stoichiometry:
                                    for l in range(0, stoichiometry):
                                        partial_hazard *= ((species_amount - l) * (1.0/(l+1)))
                                else:
                                    partial_hazard = 0
                                    break
                        local_hazards[j] = partial_hazard * rates[j]
                # Calculate global hazard and simulate waiting time
                global_hazard = local_sum(local_hazards)
                if global_hazard != 0:
                    time_change = random_exp(global_hazard)
                # If global hazard is 0, net is dead - adjust data storage and end simulation
                else:
                    if not by_iteration:
                        marking_array[i, :] = current_marking
                        events = events[0:i-1, :]
                        i +=1
                    else:
                        events = events[0:i-1]
                    time_array = time_array[0:i]
                    marking_array = marking_array[0:i,:]
                    output = gillespie_data.GillespieData()
                    output.times = time_array
                    output.markings = marking_array
                    output.event_freqs = event_freqs
                    output.iterations = i-1
                    output.events = events
                    print "Net went dead at time: %f" %time_array[-1]
                    return output
                # Simulate which transition will fire after waiting time
                random_fraction = random_unif()
                total_fraction = 0
                channel = -1
                while total_fraction < random_fraction:
                    channel += 1
                    total_fraction += (local_hazards[channel] / global_hazard)
                current_marking += stoichiometry_matrix[channel, :]
                event_freqs[channel] += 1
                current_time += time_change
                # Store result
                if by_iteration:
                    time_array[i] = current_time
                    events[i-1] = channel
                    break
                # If by run time, keep looping until next time point exceeded
                events[i-1, channel] += 1
                if current_time >= time_array[i]:
                    break
            # Update marking array
            marking_array[i, :] = current_marking
        # Simulation finished - store data and return output.
        output = gillespie_data.GillespieData()
        output.times = time_array
        output.markings = marking_array
        output.event_freqs = event_freqs
        output.iterations = i
        output.events = events
        return output
