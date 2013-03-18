import lex

class RLexerTxt(lex.RLexer):
    """
    Lexer for SPNlib .txt file format
    """    
    def lex(self, infile):
        """
        Takes a (correctly) formatted .txt file as input, and returns
        an unordered list of token objects, with properties 'label'
        and 'value'; for example, a .txt file with the line:
        p = ['X1', 'X2']
        Will be processed by lex to return a list containing a token object
        with label 'p' and value numpy.array(['X1', X2'])
        """
        
        import re
        import numpy as np
        import parse_tokens as pat
        import array

        TOKLIST = []
        # REs used to pick out SPN variables
        ptok = re.compile("(?ism)^\W*p(?:laces)?\W*=\W*(\[.*?\])")
	ttok = re.compile("(?ism)^\W*t(?:ransitions)?\W*=\W*(\[.*?\])")
	rtok = re.compile("(?ism)^\W*r(?:ates?)?\W*=\W*(\[.*?\])")
        # optional rates?
	mtok = re.compile("(?ism)^\W*m(?:arkings?)?\W*=\W*(\[.*?\])")
	ctok = re.compile("(?ism)^\W*c(?:apacities)?\W*=\W*(\[.*?\])")
	pretok = re.\
            compile("(?ism)^\W*pre(?:[_| ]arcs?)?\W*=\W*(\[(?:\W)*\[.*?\]{2})")
	posttok = re.\
            compile("(?ism)^\W*post(?:[_| ]arcs?)?\W*=\W*(\[(?:\W)*\[.*?\]{2})")
	testtok = re.\
            compile("(?ism)^\W*test(?:[_| ]arcs?)?\W*=\W*(\[(?:\W)*\[.*?\]{2})")
	inhibtok = re.compile\
        ("(?ism)^\W*I(?:nhib(?:itory[_| ]arcs?)?)?\W*=\W*(\[(?:\W)*\[.*?\]{2})")
        # optional i?
        # s = DOTALL, m = MULTILINE, i = IGNORECASE
        # Relate above REs to their standard labels used for simulation
        v_tok = {ptok : 'p', ttok : 't', rtok : 'r', mtok : 'm', ctok : 'c' }
        m_tok = {pretok : 'pre', posttok : 'post', \
                     testtok :'test', inhibtok :'inhib'}
        
        testfile = infile.readlines()
        infile.seek(0)
        # set max size of input file
        finput = infile.read(4096)
        
        # Only adds what it can find, parent class handles defaults and errors
        ## Build token list
        for i in v_tok.keys():
            if i.search(finput):
                try:
                    vval = np.array(eval(i.findall(finput)[0]),ndmin=1)
                    if i == ctok:
                        # don't add zero capacities
                        nonzero = False
                        for num in vval:
                            if num != 0:
                                nonzero = True
                        if nonzero == True:
                            TOKLIST.append(pat.Token(v_tok[i], vval))
                    else:
                        TOKLIST.append(pat.Token(v_tok[i], vval))
                except:# NameError, SyntaxError:
                    # If no quotes...
                    # OR if single quote: i.e. 'place1, place2 etc.
                    abc = i.findall(finput)[0].strip()
                    it = re.findall('[a-zA-Z0-9_]+', abc)
                    TOKLIST.append(pat.Token(v_tok[i], np.array(it,ndmin=1)))
        for j in m_tok.keys():
            if j.search(finput):
            # Same for matrices
                mval = np.matrix(eval(j.findall(finput)[0].replace('\n',''))\
                                     , dtype = int)
                TOKLIST.append(pat.Token(m_tok[j], mval))
        
        # error handling using parent method
        self.check(TOKLIST)

        # return ordered list of tokens
        return TOKLIST
