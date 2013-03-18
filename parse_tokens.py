class Token(object):
    """
    A token class which is populated by a lexer, converting raw input
    into tokens with a label (defining the token name/reference) and a
    corresponding value. An example token instantiaition is:
    token('p', numpy.array(['X1', X2']))
    Tokens are further processed by a Parser, converting these tokens 
    into useful data classes used elsewhere in the program.
    """
    def __init__(self, label, value):
        self.value = value
        self.label = str(label)

    def get_value(self):
	return self.value

    def get_label(self):
	return self.label

    def get_type(self):
	return type(self.value)
