import lex

class RLexerSBML(lex.RLexer):
    """
    Lexer for SBML language
    """
    def test_file(self, filename):
        """
        Function for returning errors found in an SBML file.
        """
        import libsbml as lb

        reader = lb.SBMLReader()
        document = reader.readSBML(filename)
        if document.getNumErrors() != 0:
            document.printErrors()

    def lex(self, filename):
        """
        Takes a (correctly) formatted .xml SBML v3.1 file as input, and returns
        an unordered list of token objects, with properties 'label'
        and 'value'.
        """       
        import libsbml as lb
        import numpy as np
        import parse_tokens as pat
        import numpy as np

        # Initialise vars
        rates = []
        reactlist =[]
        prodlist = []
        rdict = {}
        pdict = {} 
        TOK = []

        # Retrieve SBML model
        self.input = filename
        reader = lb.SBMLReader()
        document = reader.readSBML(filename.name)
        sbmlModel = document.getModel()  
        
        # Get places, transitions, initial markings:
        pnum = sbmlModel.getNumSpecies()
        tnum = sbmlModel.getNumReactions()
        Plist = [sbmlModel.getSpecies(i).getId() for i in range(pnum)]
        Mlist = [int(sbmlModel.getSpecies(r).getInitialAmount()) \
                     for r in range(pnum)]
        Tlist = [sbmlModel.getReaction(q).getId() for q in range(tnum)]
       
        # Get reactions:
        for r in range(sbmlModel.getNumReactions()):
            reaction = sbmlModel.getReaction(r)
            for rt in range(reaction.getNumReactants()):
                # for pre matix
                rdict[reaction.getId(),rt] = \
                    reaction.getReactant(rt).getSpecies(),\
                    reaction.getReactant(rt).getStoichiometry()
                reactlist.append([reaction.getId(), \
                                  reaction.getReactant(rt).getSpecies(), \
                                  reaction.getReactant(rt).getStoichiometry()])
            for rp in range(reaction.getNumProducts()):
                # for post matrix
                pdict[reaction.getId()] = \
                    reaction.getProduct(rp).getSpecies(),\
                    reaction.getProduct(rp).getStoichiometry()
                prodlist.append([reaction.getId(), \
                                   reaction.getProduct(rp).getSpecies(),\
                                   reaction.getProduct(rp).getStoichiometry()])
            # Get rates:
            # NOTE: requires reaction rates encoded in KineticLaw 
            for qr in range(reaction.getKineticLaw().getNumLocalParameters()):
                rates.append \
                    (reaction.getKineticLaw().getLocalParameter(qr).getValue())
                
        # Pre matrices is t x p
        # each row: a transition from p1 ... px
        # initialise blank matrices of correct size:
        pre = np.zeros(shape=(tnum, pnum), dtype=int)
        post = pre.copy()

        # Set up labeling of pre and post matrices for conversion
        cols={}
        for i in range(pnum):
            cols[Plist[i]] = i

        rows={}
        for j in range(tnum):
            rows[Tlist[j]] = j 

        try:
            for j in reactlist:
                # row co-ords: rows[j[0]]
                # colum co-ords:  cols[j[1]]
                # new val: j[2] - note INTEGER!
                pre[rows[j[0]], cols[j[1]]] = int(j[2])
        except KeyError:
            # Missing place or transition
            print "Error with place or transition identifiers"
            # Malformed input file
            raise AttributeError

        for p in prodlist:
            post[rows[p[0]], cols[p[1]]] = int(p[2])
        
        ## Build token list
        vectok = { 'p': Plist, 't': Tlist, 'r': rates, 'm' : Mlist }        
        mattok = {'pre':pre, 'post':post}
        
        for key in vectok.keys():
            if len(vectok[key]) != 0:
                TOK.append(pat.Token(key, np.array(vectok[key])))

        for ky in mattok.keys():
            TOK.append(pat.Token(ky, np.matrix(mattok[ky])))

        # Error handling via parent class
        self.check(TOK)

        # return unordered list of token objects
        return TOK
