import convert

class WConverterTxt(convert.WConvert):
    """
    Converter class takes a PetriNetData instance and
    write a file of given format, in this case: .txt
    """
    def save(self, outfile):
        """
        Save the current working SPN to a file of a given name
        in the current dir
        """
        import re
        import datetime
        
        # Produce and write txt file
        dt = re.compile(r"dtype")
        f = open(outfile, 'w') 
        f.write('## ~ File produced by SPNlib on %s ~ ##\n\n'\
                 % str(datetime.datetime.now().strftime("%d-%m-%Y at %H:%M")))
        for j in self.vdict.keys():
            # Only write attributes that exist
            if self.vdict[j] is not None:
                g = re.search(r"dtype", repr(self.vdict[j]))
                if g:
                    # Handle ndarray's habit of adding dtype
                    value = repr(self.vdict[j]).replace('\n','')
                    f.write(j + " = " + value[6:g.start()-9].replace(' ','')\
                                .replace('],',']') +'\n')
                else:
                    value = repr(self.vdict[j]).replace('\n','')
                    f.write(j + " = " + value[6:-1].replace(' ','') + '\n')
        for i in self.mdict.keys():
            if self.mdict[i] is not None:
                value = repr(self.mdict[i]).replace('\n','')
                if len(i) < 5:
                    i = i + ' '*(5 % len(i))
                f.write(i + " = " + value[7:-1].replace(' ','')\
                            .replace('],[','],\n\t [') + '\n')
        

