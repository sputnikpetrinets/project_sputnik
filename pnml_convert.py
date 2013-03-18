import convert

class WConverterPNML(convert.WConvert):    
    """
    Converter class takes a PetriNetData instance and
    write a file of given format, in this case: .pnml
    (Petri Net Markup Language)
    """
    
    def save(self, outfile):
        """
        Save the current working SPN to a file of a given name
        in the current dir. vdict contains the labels and data 
        of the vector vars, mdict is the matrices.
        """       
        import re
        import datetime
        from xml.dom.minidom import Document

        # Open file, build header
        f = open(outfile, 'w')
        doc = Document()
        # write header with program, date/time:
        comm = doc.createComment('Created by SPNlib on %s' \
                % str(datetime.datetime.now().strftime("%d-%m-%Y at %H:%M")))
        doc.appendChild(comm)
        pnml = doc.createElement("pnml")
        pnml.setAttribute("xmlns", 'http://www.pnml.org/version-2009/grammar/pnml')
        doc.appendChild(pnml)
        net = doc.createElement("net")
        net.setAttribute("id", "SPN")
        # Important: set net type: stochastic
        net.setAttribute("type", "Stochastic")
        pnml.appendChild(net)
        
        # build file body
        c1 = 0 # places count
        pdict = {}
        c2 = 0 # trans count
        c3 = 0 # inhib count
        c4 = 0 # test count

        # Set places, markings:
        for spe in self.vdict['p']:
            s = doc.createElement("place")
            s.setAttribute("id", spe)
            if self.vdict['c'] != None:
                s.setAttribute("capacity",str(self.vdict['c'][c1]))
            pdict[c1] = spe
            m = doc.createElement("initialMarking")
            v = doc.createElement("value")
            amount = doc.createTextNode(str(int(self.vdict['m'][c1])))
            v.appendChild(amount)
            m.appendChild(v)
            s.appendChild(m)
            net.appendChild(s)
            c1 += 1
        
        # Set transitions, rates:
        for reac in self.vdict['t']:
            r = doc.createElement("transition")
            r.setAttribute("id", reac)
            rate = doc.createElement("rate")
            v = doc.createElement("value")
            amount = doc.createTextNode(str(self.vdict['r'][c2]))
            v.appendChild(amount)
            rate.appendChild(v)
            r.appendChild(rate)
            net.appendChild(r)
            c2+=1

        # Set Inhibitory arcs:
        try:
            if len(self.mdict['inhib']) != 0:
                for iarc in self.mdict['inhib']:
                    for h in range(0,c1):
                        if iarc[0,h] != 0:
                           inhib = doc.createElement("arc")
                           inhib.setAttribute("source",self.vdict['p'][h])
                           inhib.setAttribute("target",self.vdict['t'][c3])
                           inhib.setAttribute("type","inhibitory")
                           inis = doc.createTextNode(str(iarc[0,h]))
                           va = doc.createElement("value")
                           va.appendChild(inis)
                           inhib.appendChild(va)
                           net.appendChild(inhib)
                    c3+=1
        except TypeError:
            pass
        
        # Set Test arcs:
        try:
            if len(self.mdict['test']) != 0:
                for tarc in self.mdict['test']:
                    for bx in range(0,c1):
                        if tarc[0,bx] != 0:
                           tar = doc.createElement("arc")
                           tar.setAttribute("source",self.vdict['p'][bx])
                           tar.setAttribute("target",self.vdict['t'][c4])
                           tar.setAttribute("type","test")
                           tis = doc.createTextNode(str(tarc[0,bx]))
                           val = doc.createElement("value")
                           val.appendChild(tis)
                           tar.appendChild(val)
                           net.appendChild(tar)
                    c4+=1         
        except TypeError:
            pass

        # row counting for pre/post
        rcr = 0
        rco = 0
        for bin in self.mdict['pre']:
        # here all from = place, all to = transitions
            for q in range(0,c1):
                if bin[0,q] != 0:
                    a = doc.createElement("arc")
                    a.setAttribute("source", self.vdict['p'][q])
                    a.setAttribute("target", self.vdict['t'][rcr])
                    stoich = doc.createTextNode(str(bin[0,q]))
                    v = doc.createElement("value")
                    v.appendChild(stoich)
                    a.appendChild(v)
                    net.appendChild(a)
            # row count pre
            rcr+=1
        for bin in self.mdict['post']:
        # here all from = trans, all to = place
        # bin = row
            for q in range(0,c1):
                # for each col
                if bin[0,q] != 0:
                    a = doc.createElement("arc")
                    a.setAttribute("source", self.vdict['t'][rco])
                    a.setAttribute("target", self.vdict['p'][q])
                    # c1 is count of places
                    # i.e. for LV, 0 and 1 (p1, p2)
                    # bin is row of post, e.g. [2,0] (row 0)
                    # this stoich of 2
                    stoich = doc.createTextNode(str(bin[0,q]))
                    v = doc.createElement("value")
                    v.appendChild(stoich)
                    a.appendChild(v)                   
                    net.appendChild(a)
                    q+=1
            # row count post
            rco+=1 
        
        # write file 
        out = doc.toprettyxml(indent="  ", encoding="UTF-8")
        f.write(out)
        f.close()
