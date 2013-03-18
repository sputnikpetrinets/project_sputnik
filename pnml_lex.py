import lex

class RLexerPNML(lex.RLexer):
    """
    Lexer for Petri Net Markup Language (PNML)
    """
    def lex(self, filename):
        """
        Takes a (correctly) formatted PNML file as input, and returns
        an unordered list of token objects, with properties 'label'
        and 'value'. This list should then be passed to an RParser
        object.
        """       
        from xml.dom.minidom import parseString      
        import parse_tokens as pat
        import numpy as np
        import re

        self.input = filename
        data = self.input.read()
        self.input.close()
        getpid = re.compile('(?i)place(?:.*)id\w?=\w?\"?([a-zA-Z_0-9]*)\"?')
        gettid = re.compile('(?i)transition(?:.*)id\w?=\w?\"?([a-zA-Z_0-9]*)\"?')
        getaid = re.compile('(?i)arc(?:.*)id\w?=\w?\"?([a-zA-Z_0-9]*)\"?')
        getatype = re.compile('(?i)type\w?=\w?\"?([a-zA-Z_0-9]*)\"?')
        getnid = re.compile('(?i)net(?:.*)id\w?=\w?\"?([a-zA-Z_0-9 ]*)\"?')
        getcapac = re.compile('(?i)capacity\w?=\w?\"?([0-9]*)\"?')
        getsource = re.compile('(?i)source\w?=\w?\"?([a-zA-Z_0-9]*)\"?')
        gettarg = re.compile('(?i)target\w?=\w?\"?([a-zA-Z_0-9]*)\"?')
        dom = parseString(data)
        
        plist = []
        mlist = []
        clist = []
        pcount = 0
        for place in dom.getElementsByTagName('place'):
            tag = place.toxml()
            m = None
            try:
                # For places where the place name is encoded in the 
                # <place> .. <name> .. <text> 
                data = str(place.getElementsByTagName('name')[0]\
                              .getElementsByTagName('text')[0]\
                               .firstChild.data).rstrip()
            except IndexError:
                pass
            try:
                # For places where the place id tag is the name of the place
                data = str(re.search(getpid, tag).group(1).rstrip())
            except AttributeError:
                pass
            try:
                # Try different ways of retrieving the marking, allows 
                # flexibility in input file. #1 = <marking><value>X</.. </..
                m = int(place.getElementsByTagName('marking')[0]\
                            .getElementsByTagName('value')[0].firstChild.data)
            except IndexError:
                pass
            try:
                # #2 = <initialMarking><valueX</.. </..
                # Takes precendence over the above
                m = int(place.getElementsByTagName('initialMarking')[0]\
                            .getElementsByTagName('value')[0].firstChild.data)
            except IndexError:
                pass
            try:
                # #3 = <initialMarking><text>X</.. </..
                # Takes precendence over the above
                m = int(place.getElementsByTagName('initialMarking')[0]\
                            .getElementsByTagName('text')[0].firstChild.data)
            except IndexError:
                pass
            if m == None:
                print "Note: No initial markings detected, set to 0"
                ### WARNING NO INITIAL MARKING SET FOR PLACE ###
                mlist.append(0)
            else:
                mlist.append(m)
            try:
                cap = int(re.search(getcapac, tag).group(1).rstrip())
                if cap != 0:
                    clist.append(cap)
            except:
                pass
            plist.append(data)
            pcount +=1
        
        tlist = []
        rates = []
        tcount = 0
        for trans in dom.getElementsByTagName('transition'):
            # Initialise to blank each time
            tid = None
            tag = trans.toxml()
            
            # ALT methods of retrieving transition names: 
            # NOTE: arc source/target (should) use transition id as a reference
            # try:
            #     #preferably get the name from <name>..<value> OR <text>
            #     tid = str(trans.getElementsByTagName('name')[0]\
            #                .getElementsByTagName('value')[0].firstChild.data)\
            #                .rstrip()
            # except:
            #     pass
            # try:
            #     tid = str(trans.getElementsByTagName('name')[0]\
            #                 .getElementsByTagName('text')[0].firstChild.data)\
            #                 .rstrip()
            # except:
            #     pass
            
            try:
                # Is transition name encoded in id?
                tid = str(re.search(gettid, tag).group(1))
            except:
                # else assign out own IDs
                tid = 't_' + str(tcount)
  
            tlist.append(tid)
            tcount +=1
        
            ## RATES
            try:
                rate = str(trans.getElementsByTagName('rate')[0]\
                    .getElementsByTagName('value')[0].firstChild.data)
                rates.append(float(rate))
            except:
                pass
        
        # Get arcs
        arcd = {}
        stoich = None
        acount = 0
        for arc in dom.getElementsByTagName('arc'):
            tag = arc.toxml()
            try:
                atype = arc.getElementsByTagName('type')[0].firstChild.data
                print atype
            except IndexError:
                pass
            try:
                stoich = arc.getElementsByTagName('text')[0].firstChild.data
            except IndexError:
                pass
            try:
                stoich = arc.getElementsByTagName('value')[0]\
                    .firstChild.data
                stoich = arc.getElementsByTagName('inscription')[0]\
                    .getElementsByTagName('value')[0].firstChild.data
            except IndexError:
                pass
 
            if stoich == None:
                ### WARNING: MISSING STOICHIOMETRIES
                ### ASSUMED ONE
                print "Note: Missing stoichiometry, set to 1"
                stoich = 1

            # arc ID
            try:
                aid = str(re.search(getaid, tag).group(1))
            except:
                aid = acount
            
            afrom = str(re.search(getsource, tag).group(1))

            # find test and inhibitory arcs:
            try:
                atype = str(re.search(getatype, tag).group(1))
            except: 
                atype = None

            if atype == 'test':
                mat = 'test'
            elif atype == 'inhibitory':
                mat = 'inhib'
            else:
                if afrom in plist:
                    mat = 'pre'
                else:
                    mat = 'post'

            ato = str(re.search(gettarg, tag).group(1))
            # ARC d
            arcd[aid] = [int(stoich), afrom, ato, mat]
            acount +=1

        # if [1] in plist >> pre
        # if [1] in tlist >> post
        net = re.search(getnid, str(dom.getElementsByTagName('net')[0]\
                                        .toxml())).group(1)
        # format { arcid : \
        # [stoichiometry, from (place or trans), to (p or t)], 'pre' or 'post' }
        ## Pre and Post ##
        pre = np.zeros(shape=(len(tlist), len(plist)), dtype=int)
        post = pre.copy()
        
        # test and inhib may not be needed
        test = pre.copy()
        inhib = pre.copy()
        zeros = pre.copy().tolist()

        cols={}
        for i in range(len(plist)):
            # buils dict for matrices population purposes
            # columns of pre/post relate to places
            cols[plist[i]] = i

        rows={}
        for j in range(len(tlist)):
            # rows relate to transitions
            rows[tlist[j]] = j 

        try:
            for arc in arcd.values():
                if arc[3] == 'pre':
                    pre[rows[arc[2]], cols[arc[1]]] = int(arc[0])
                elif arc[3] == 'post':
                    post[rows[arc[1]], cols[arc[2]]] = int(arc[0])
                elif arc[3] == 'test':
                    test[rows[arc[2]], cols[arc[1]]] = int(arc[0])
                elif arc[3] == 'inhib':
                    inhib[rows[arc[2]], cols[arc[1]]] = int(arc[0])
        except KeyError:
            print "Error with place or transition identifiers"
            raise AttributeError

        ## Build token list
        TOK = []
        vectok = { 'p': plist, 't': tlist, 'r': rates, 'm' : mlist, 'c':clist }
        mattok = {'pre': pre, 'post': post, 'inhib':inhib, 'test':test}
 
        for key in vectok.keys():
            if len(vectok[key]) != 0:
                TOK.append(pat.Token(key, np.array(vectok[key])))
        
        for ky in mattok.keys():
            if mattok[ky].tolist() != zeros:
                TOK.append(pat.Token(ky, np.matrix(mattok[ky])))
        
        # run error handling
        self.check(TOK)

        # return unordered list of token objects
        return TOK
