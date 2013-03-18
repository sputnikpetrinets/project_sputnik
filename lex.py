class RLexer(object):
    """Abstract class for lexers"""

    def lex(self, filename):
        """Takes list of files, returns list of tokens"""
        pass
    
    @staticmethod
    def check(tlist):
        """
        Error checking prior to returning token list after lexing.
        Tests validity and existence of the vital parameters, raises
        errors if the petri net isn't fully specified.
        """
        import parse_tokens as pat
        import numpy as np

        def check_uniqueness(ref):
            """
            Checks a list of given identifier to ensure unique
            identifiers have been assigned. If there are duplicates,
            appends an index to the end, e.g. is p = [ gA , gA , pA ]
            this method would ceonvert it to [gA , gA_1 , pA ]
            """
            for token in tlist:
                if token.label == ref:
                    test_list = token.value
            
            u_out = []
            co = 1
            if len(test_list) > len(set(test_list)):
                for p in test_list:
                    if p not in u_out:
                        u_out.append(p)
                    else:
                        u_out.append(p+'_'+str(co))
                        co+=1
                for item in tlist:
                    if item.label == ref:
                        item.value = u_out
                #raise AttributeError
                
        ## ERROR handling ##
        count = {}
        rates = []
        flags = []
        for token in tlist:
            count[token.label] = len(token.value)
            if token.label == 'r':
                 rates = token.value
            if token.label == 'c':
                 caps = token.value
            if token.label == 'pre':
                 pre = token.value
            if token.label == 'post':
                 post = token.value
            if token.label == 'test':
                 test = token.value
                 flags.append('t')
            if token.label == 'inhib':
                 inhib = token.value
                 flags.append('i')

        # Required parameters for Petri Net
        req = ['p', 't', 'r', 'm', 'pre', 'post']
        ## Current setup: ##
        # If rates are missing: set all to 0
        # If initial markings are missing: set all to 0
        # If p, t, pre or post are missing: Error
        for item in req:
            if item not in count.keys():
                if item == 'r':
                    tlist.append(pat.Token('r', np.zeros(count['t'])))
                    count['r'] = count['t']
                else:
                    if item == 'm':
                        tlist.append(pat.Token('m', np.zeros(count['p'])))
                        count['m'] = count['p']
                    else:
                        # Net not fully specified
                        # Params missing
                        # pass item to error handler
                        raise AttributeError
        
        check_uniqueness('p')
        check_uniqueness('t')

        missingno = 0
        if count['r'] < count['t']:
            # MISSING RATES!
            missingno = count['t'] - count['r']
            nrate = np.append(rates, np.zeros(missingno))
            tlist.append(pat.Token('r', nrate))
        
        try:
            miss = 0
            if count['c'] != 0:
                if count['c'] < count['p']:
                    miss = count['p'] - count['c']
                    ncap = np.append(caps, np.zeros(miss, dtype=int))
                    tlist.append(pat.Token('c', ncap))
        except KeyError:
            # if no capacities, don't worry
            pass

        # Check dimensions of pre and post matrices
        matdim = count['t'] * count['p']
        if matdim != pre.size or matdim != post.size:
            raise AttributeError
        
        if 't' in flags:
            if matdim != test.size:
                raise AttributeError
        if 'i' in flags:
            if matdim != inhib.size:
                raise AttributeError

        if count['pre'] != count['post'] or count['pre'] != count['t']:
            # Matrices error
            raise AttributeError

        # Test for negative rates
        for value in rates:
            if value < 0:
                raise AttributeError

        # Test for negative pre/post
        l = np.ravel(pre)
        ll = np.ravel(post)
        for vals in l:
            if vals < 0:
                raise AttributeError
        for va in ll:
            if va < 0:
                raise AttributeError
