import spectral_a

class LSLayout(object):
    """
    Loads/saves Petri net layout from a .layout file.
    """
    def __init__(self):
        self._pos = dict()

    @property
    def positions(self):
        return self._pos

    @positions.setter
    def positions(self, pos):
        self._pos = pos

    def load(self, loadfile):
        """
        Loads (if present) a $.layout file, where $ = the filename of
        the open file (minus its extension). Uses this dictionary of
        co-ordinates to lay out the net.
        """
        import ast
        import os

        self.base = os.path.splitext(loadfile)[0]
        infile = self.base + '.layout'
        try:
            cfile = str(open(infile, "r").readlines(8192))
            self._pos=ast.literal_eval(cfile[2:-2])
        except IOError:
            # if no infile, layout afresh
            # e.g. spectral_a.calculate (??)
            pass
    
    def save(self, savefile):
        """
        Saves the co-ordinates of places and transitions to a $.layout 
        file, where $ = the filename of the open file (minus its extension).
        Writes a raw dictionary as a string.
        """
        import os

        print self._pos
        self.base = os.path.splitext(savefile)[0]
        outfile = self.base + '.layout'
        out = open(outfile, "w")
        out.write(str(self._pos))
        out.close()
