import convert
try:
    import libsbml as lb
except ImportError:
    print "NOTE: libSBML Python API not installed - Sputnik is unable to read or write SBML. To install libSBML see: http://sbml.org/Software/libSBML"
    raise AttributeError

class WConverterSBML(convert.WConvert):
    """
    Converter class takes a PetriNetData instance and
    write a file of given format, in this case: .xml (SBML)x
    """

    def save(self, outfile):
        """
        Save the current working SPN to a file of a given name
        in the current dir. vdict contains the labels and data 
        of the vector vars, mdict is the matrices.
        (Note on SBML version compatibility:
        SBML output is written for Level 3 Version 1, but has no
        errors with any Level 2 versions. 6 Errors occur with an L1
        compatibility check if non-integer rates are used.)
        """
        import re
        import libsbml as lb

        # build SBML document and header
        f = open(outfile, 'w') 
        lev = 3
        ver = 1
        out = lb.SBMLDocument(lev,ver)
        model = out.createModel()
        model.setId('StochasticPetriNet')
        
        # Build file body
        cell = model.createCompartment()
        cell.setId('Cell')
        # Causes an error if omitted in earlier levels of SBML
        cell.setSpatialDimensions(3)
        model.addCompartment(cell)
        c1 = 0 # places count
        pdict = {}
        c2 = 0 # trans count? 
        for spe in self.vdict['p']:
            s = model.createSpecies()
            s.setId(spe)
            pdict[c1] = spe
            s.setCompartment(cell.getId())
            s.setInitialAmount(int(self.vdict['m'][c1]))
            model.addSpecies(s)
            c1 += 1
        for reac in self.vdict['t']:
            r = model.createReaction()
            r.setId(reac)
            kl = r.createKineticLaw()
            # Get 'rate' params, insert into KineticLaw local param field
            lp = kl.createLocalParameter()
            lp.setValue(self.vdict['r'][c2])
            lp.setId('rate' + str(c2))
            model.addReaction(r) 
            # Use pre matrix to write named reactants & stoichiometries
            for bin in self.mdict['pre'][c2]:
                # For each place
                for q in range(0, c1):
                    if bin[0,q] != 0 :
                        t = model.createReactant()
                        t.setSpecies(self.vdict['p'][q])
                        # Convert type numpy.int64 -> int
                        t.setStoichiometry(int(bin[0,q]))
            # Same for post matrix
            for bon in self.mdict['post'][c2]:
                # For each place
                for t in range(0, c1):
                    if bon[0,t] != 0 :
                        p = model.createProduct()
                        p.setSpecies(self.vdict['p'][t])
                        # Convert type numpy.int64 -> int
                        p.setStoichiometry(int(bon[0,t]))
            c2+=1
        
        ## Compatibility checks
        # Uncomment print statements to view errors
        print '\t1.0 err: ',  out.checkL1Compatibility()
        # print out.printErrors()
        print '\t2.1 err: ', out.checkL2v1Compatibility()
        # print out.printErrors()
        print '\t2.2 err: ', out.checkL2v2Compatibility()
        # print out.printErrors()
        print '\t2.3 err: ', out.checkL2v3Compatibility()
        # print out.printErrors()
        print '\t2.4 err: ', out.checkL2v4Compatibility()
        # print out.printErrors()
        print '\t3.1 err: ', out.checkL3v1Compatibility()
 
        # write to file
        w = lb.SBMLWriter()
        w.setProgramName('SPNlib')
        w.setProgramVersion('1.0')
        w.writeSBML(out, outfile)
        
