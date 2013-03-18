
class WConvert(object):
     """
     Parent converter class for converters to inherit from. Contains method
     to pull PetriNetData into object.
     """
     def __init__(self, SPN):
        """Grab stiochiometry data, set class vars"""
        self.SPNs = SPN.stoichiometry
        # Vector dictionary
        self.vdict = {'p':SPN.places, 't':SPN.transitions, 'c':SPN.capacities,\
                 'r':SPN.rates, 'm':SPN.initial_marking}
        # Matrices dictionary
        self.mdict = {'pre':self.SPNs.pre_arcs, 'post':self.SPNs.post_arcs, \
                         'test':SPN.test_arcs, 'inhib':SPN.inhibitory_arcs}    
     
     def getPetriNetData(self):
        """ Construct list of tokens from SPN, returns. """
        import parse_tokens as pat

        TLIST=[]
        for i in self.vdict.keys():
            TLIST.append(pat.Token(i, self.vdict[i]))
        for j in self.mdict.keys():
            TLIST.append(pat.Token(j, self.vdict[i]))
        
        return TLIST

     def save(self, outfile):
         pass
