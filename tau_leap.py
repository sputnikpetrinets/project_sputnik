from algorithm import Algorithm
import tau_leap_data
import numpy as np
import random
import math

class TauLeap(Algorithm):
    """
    Subclass of Algorithm, allows Tau Leap algorithm to be run, for a specified
    run time or number of iterations, for a specified number of runs.

    Instance Variables:
    - epsilon
    - control_parameter
    - num_ssa_runs

    Methods:
    __init__: Tau Leap parameters set to default values
    tau_leap: protected, accessed by Algorithm.run_simulation
    run_ssa: private, accessed by tau_leap

    """

    ##############################################
    ##  Class Constructor
    ##############################################

    def __init__(self):
        self._petri_net = None
        self._run_time = None
        self._time_step = None
        self._num_runs = 1
        self._epsilon = 0.03
        self._control_parameter = 10
        self._num_ssa_runs = 100
        self._num_iterations = None
        self._simulation_data = []
        self._algorithm = TauLeap._tau_leap


    ##############################################
    ##  Instance Variables: Getters and Setters
    ##############################################
        
    @property
    def epsilon(self):
        """ Return epsilon. """
        return self._epsilon

    @epsilon.setter
    def epsilon(self, e):
        """ Set epsilon. """
        e = float(e)
        if 0 < e and e < 1:
            self._epsilon = e
            if e > 0.1:
                print 'Warning: epsilon is >0.1, consider reducing for better accuracy.'
        else:
            print 'Error: epsilon must be between 0 and 1.'

    @property
    def control_parameter(self):
        """ Return control parameter """
        return self._control_parameter

    @control_parameter.setter
    def control_parameter(self, c):
        """ Set control parameter """
        if c > 0:
            try:
                self._control_parameter = int(c)
            except:
                print 'Error: number of runs must be an integer.'
            if not (2 <= c and c <= 20):
                print 'Warning: control parameter is not in the range 2-20, consider revising.'
        else:
            print 'Error: control parameter must be a positive integer.'                

    @property
    def num_ssa_runs(self):
        """ Return number of SSA runs """
        return self._num_ssa_runs

    @num_ssa_runs.setter
    def num_ssa_runs(self, r):
        """ Set number of SSA runs """
        if r > 0:
            try:
                self._sum_ssa_runs = int(r)
            except:
                print 'Error: number of runs must be an integer.'
        else:
            print 'Error: number of runs must be a positive integer.'


    ##############################################
    ##  Simulation Algorithm
    ##############################################

    def _tau_leap(self):
        """ Run the Tau Leap algorithm for the specified petri net and simulation variables. """
        
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
            consumed_matrix = np.asarray(data.stoichiometry.consumed_matrix, dtype=int)
            species_hors = np.asarray(data.stoichiometry.species_hors)
        except:
            print 'Error: calculate stoichiometry_matrix, dependency_matrix consumed_matrix and species_hors'
            return
        if data.capacities != None:
            print 'Warning: Tau Leap ignores capacities, consider using Gillespie instead.'
        if data.test_arcs != None:
            print 'Warning: Tau Leap ignores test arcs, consider using Gillespie instead.'
        if data.inhibitory_arcs != None:
            print 'Warning: Tau Leap ignores inhibitory arcs, consider using Gillespie instead.'

        # Simulation variables
        epsilon = self.epsilon
        control_parameter = self.control_parameter
        num_iterations = self.num_iterations
        num_ssa_runs = self.num_ssa_runs
        run_time = self.run_time
        time_step = self.time_step
        if not epsilon:
            print 'Error: must specify epsilon'
            return
        if not control_parameter:
            print 'Error: must specify control parameter'
        if not num_iterations:
            if not run_time or not time_step:
                print 'Error: specify num_iterations or both run_time and time_step'
                return
            else:
                by_iteration = False
        else:
            by_iteration = True

        # Dot eliminators
        random_unif = random.random
        random_exp = random.expovariate
        random_pois = np.random.poisson
        local_zeros = np.zeros
        local_any = any
        local_sum = sum
        local_all = all
        local_min = min
        local_max = max
        local_abs = abs
        local_range = range
        local_where = np.where
        local_inf = np.inf

        # Ranges
        transitions = local_range(num_transitions)
        places = local_range(num_places)
        ssa_runs = local_range(num_ssa_runs)

        # Algorithm data storage initialisation
        current_time = 0
        current_marking = np.copy(initial_marking)
        event_freqs = local_zeros(num_transitions, dtype=int)
        local_hazards = [0] * num_transitions
        permitted = local_zeros(num_places, dtype=float)
        channel = num_transitions
        net_dead = False
        info = local_zeros((num_places, 7), dtype=float)

        # Simulation for specified number of events (iterations)
        if by_iteration:
            record_points = num_iterations + 1
            time_array = local_zeros(record_points, dtype=float)
            events = local_zeros((record_points - 1, num_transitions), dtype=int)
        else:
            time_array = np.arange(0, run_time + time_step, time_step, dtype=float)
            record_points = len(time_array)
            events = local_zeros((record_points - 1, num_transitions), dtype=np.int)
        marking_array = local_zeros((record_points, num_places), dtype=np.int)
        marking_array[0, :] = np.copy(initial_marking)
        critical = local_zeros(num_transitions, dtype=int)
        # Simulation algorithm
        i = 0
        while i < record_points - 1:
            i += 1
            # Extra loop required when by_iteration == False
            while 1:
                # Check if waiting time jumped past multiple timepoints
                if not by_iteration:
                    if current_time >= time_array[i]:
                        break
                # Calculate local hazards and number of permitted firings for each transition
                for j in transitions:
                    permitted = []
                    partial_hazard = 1
                    for k in places:
                        stoich_change = consumed_matrix[j, k]
                        if stoich_change != 0:
                            max_times = current_marking[k] / stoich_change
                            permitted.append(max_times)
                        stoichiometry = pre_arcs[j, k]
                        if stoichiometry == 0:
                            pass
                        elif stoichiometry == 1:
                            partial_hazard *= current_marking[k]
                        else:
                            species_amount = current_marking[k]
                            if species_amount >= stoichiometry:
                                for l in local_range(stoichiometry):
                                    partial_hazard *= ((species_amount - l) * (1.0/(l+1)))
                            else:
                                partial_hazard = 0
                                break
                    local_hazards[j] = partial_hazard * rates[j]
                    # Determine which transitions are critical
                    if local_hazards[j] == 0:
                        critical[j] = 1
                    elif permitted == []:
                        critical[j] = 0
                    elif local_min(permitted) < control_parameter:
                        critical[j] = 1
                    else:
                        critical[j] = 0
                global_hazard = local_sum(local_hazards)
                # If global hazard is 0, net is dead - adjust data storage and end simulation
                if global_hazard == 0:
                    net_dead = True
                    print "Net is dead!"
                    time_array = time_array[0:i]
                    marking_array = marking_array[0:i,:]
                    events = events[0:i-1]
                    break
                # If all transitions critical, run the Gillespie for a while then check again
                if local_all(critical):
                    [time_array, marking_array, events, event_freqs, current_time, current_marking, i, net_dead] = TauLeap.__run_ssa(self, data,
                        i, current_time, current_marking, by_iteration, net_dead, time_array, marking_array, events, event_freqs, record_points)
                    if net_dead == True:
                            break
                    new_events = events[i-1,:]
                # Otherwise, calculate tau
                else:
                    # Calculate tau for non-critical reactions only
                    for k in places:
                        # Calculate epsilon divisor for each species
                        if species_hors[k, 0] == 0:
                                info[k, 6] = local_inf
                        else:
                            if species_hors[k, 0] == 1:
                                info[k, 0] = 1
                            elif species_hors[k, 0] == 2:
                                if species_hors[k, 1] == 1:
                                    info[k, 0] = 2
                                else:
                                    if current_marking[k] > 2:
                                        info[k, 0] = (2 + 1.0 / (current_marking[k] - 1))
                                    else:
                                        info[k, 0] = 3
                            elif species_hors[k, 0] == 3:
                                if species_hors[k, 1] == 1:
                                    info[k, 0] = 3
                                elif species_hors[k, 1] == 2:
                                    if current_marking[k] > 2:
                                        info[k, 0] = 1.5 * (2 + 1.0 / (current_marking[k] - 1))
                                    else:
                                        info[k, 0] = 4.5
                                else:
                                    if current_marking[k] > 3:
                                        info[k, 0] = 3 + 1.0 / (current_marking[k] - 1) + 2 / (current_marking[k] - 2)
                                    else:
                                        info[k, 0] = 5.5
                            # Generalisation to higher order reactions
                            else:
                                if species_hors[k, 1] == 1:
                                    info[k, 0] = species_hors[k, 0]
                                else:
                                    temp_mark = current_marking[k]
                                    if temp_mark < species_hors[k, 1]:
                                        temp_mark = species_hors[k, 1]
                                    info[k, 0] = species_hors[k, 1]
                                    for l in range(1, species_hors[k, 1]):
                                        info[k, 0] += (float(l) / (temp_mark - l))
                                    info[k, 0] *= species_hors[k, 0]
                                    info[k, 0] /= species_hors[k, 1]
                            # Calculate mean and variance of expected change in species marking for non-critical firings
                            info[k, 1] = 0
                            info[k, 2] = 0
                            for j in transitions:
                                # Non-critical only
                                if critical[j] == 0:
                                    info[k, 1] += (stoichiometry_matrix[j, k] * local_hazards[j])
                                    info[k, 2] += ((stoichiometry_matrix[j, k] ** 2) * local_hazards[j])
                            info[k, 1] = local_abs(info[k, 1])
                            # Calculate tau of non-critical reactions using the above
                            info[k, 3] = float(local_max(1, float(epsilon * current_marking[k])/info[k,0]))
                            if info[k, 1] == 0:
                                info[k, 4] = local_inf
                            else:
                                info[k, 4] = info[k, 3] / info[k,1]
                            if info[k, 2] == 0:
                                info[k, 5] = local_inf
                            else:
                                info[k, 5] = (info[k, 3]**2)/info[k,2]
                            info[k, 6] = local_min(info[k, 4], info[k, 5])
                    tau_ncr = local_min(info[:, 6])
                    # If non-critical tau is too small, run the Gillespie for a while
                    if tau_ncr < (10 / global_hazard):
                        [time_array, marking_array, events, event_freqs, current_time, current_marking, i, net_dead] = TauLeap.__run_ssa(self, data,
                            i, current_time, current_marking, by_iteration, net_dead, time_array, marking_array, events, event_freqs, record_points)
                        if net_dead == True:
                            break
                        new_events = events[i-1,:]
                    # Otherwise simulate a tau leap
                    else:
                        while 1:
                            new_events = local_zeros(num_transitions, dtype=int)
                            new_marking = local_zeros(num_places, dtype=int)
                            # Calculate total hazard of critical reactions and simulate waiting time to first event
                            critical_hazard = 0
                            for j in transitions:
                                if critical[j] == 1:
                                    critical_hazard += local_hazards[j]
                            if critical_hazard == 0:
                                tau_cr = np.inf
                            else:        
                                tau_cr = random_exp(critical_hazard)
                            # Choose tau as smaller of critical and non-critical timesteps
                            if tau_ncr < tau_cr:
                                tau = tau_ncr
                            # If tau critical is small, simulate a critical event to occur
                            else:
                                tau = tau_cr
                                random_fraction = random_unif()
                                total_fraction = 0
                                channel = -1
                                while total_fraction < random_fraction:
                                    channel += 1
                                    if critical[channel] == 1:
                                        total_fraction += (local_hazards[channel] / critical_hazard)
                                new_events[channel] = 1
                            # Sample frequencies of non-critical transitions from a Poisson distribution
                            for j in transitions:
                                if critical[j] == 0:
                                    new_events[j] = random_pois(lam=(local_hazards[j]*tau))
                            for j in transitions:    
                                new_marking += (new_events[j] * stoichiometry_matrix[j, :])
                            # If any marking goes negative, halve non-critical tau and resample frequencies
                            if local_any(np.less((current_marking + new_marking), 0)):
                                tau_ncr /= 2
                                print 'Too large tau encountered and adjusted - consider reducing epsilon or increasing control parameter.'
                            else:
                                break
                        # Store results of simulation iteration
                        event_freqs += new_events
                        current_marking += new_marking
                        current_time += tau
                        if by_iteration:
                            time_array[i] = current_time
                            break
                        # If by run time, keep looping until next time point exceeded
                        if current_time >= time_array[i]:
                            break
            # Update marking array
            try:
                marking_array[i, :] = current_marking
                events[i-1,:] = new_events
            # End if net dead
            except(IndexError):
                i -= 1
                break
        # Simulation finished - store data and return output.
        output = tau_leap_data.TauLeapData()
        output.times = time_array
        output.markings = marking_array
        output.iterations = i
        output.events = events
        output.event_freqs = event_freqs
        return output


    def __run_ssa(self, data, i, current_time, current_marking, by_iteration, net_dead, time_array, marking_array, events, event_freqs, record_points):
        """ Run the Gillespie SSA for a specified number of iterations when Tau Leap conditions do not hold. """

        # Petri net data to local variables
        pre_arcs = np.asarray(data.stoichiometry.pre_arcs, dtype=int)
        num_transitions = pre_arcs.shape[0]
        num_places = pre_arcs.shape[1]
        rates = np.asarray(data.rates, dtype=float)
        initial_marking = data.initial_marking
        stoichiometry_matrix = np.asarray(data.stoichiometry.stoichiometry_matrix, dtype=int)
        dependency_matrix = np.asarray(data.stoichiometry.dependency_matrix, dtype=int)
        dependency_matrix = np.vstack((dependency_matrix, np.ones(num_transitions, dtype=int)))

        # Simulation variables to local variables
        num_iterations = self.num_iterations
        run_time = self.run_time
        time_step = self.time_step
        num_ssa_runs = self._num_ssa_runs

        # Dot eliminators
        random_unif = random.random
        random_exp = random.expovariate
        local_sum = sum
        local_any = any

        # Ranges
        transitions = range(num_transitions)
        places = range(num_places)
        
        local_hazards = [0] * num_transitions
        channel = num_transitions

        # Decide number of iterations to run
        if i + num_ssa_runs < record_points:
            end_ssa_range = i + num_ssa_runs
        else:
            end_ssa_range = record_points
        # Simulation algorithm
        for i in range(i, end_ssa_range):
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
                    net_dead = True
                    print "Net went dead at time: %f" %time_array[-1]
                    if not by_iteration:
                        marking_array[i, :] = current_marking
                        events = events[0:i-1, :]
                        i +=1
                    else:
                        events = events[0:i-1]
                    time_array = time_array[0:i]
                    marking_array = marking_array[0:i,:]
                    return [time_array, marking_array, events, event_freqs, current_time, current_marking, i, net_dead]
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
                events[i-1, channel] += 1
                # Store result
                if by_iteration:
                    time_array[i] = current_time
                    break
                # If by run time, keep looping until next time point exceeded
                if current_time >= time_array[i]:
                    break
            # Update marking array
            marking_array[i, :] = current_marking
        return [time_array, marking_array, events, event_freqs, current_time, current_marking, i, net_dead]
