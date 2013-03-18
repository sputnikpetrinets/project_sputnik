class ModelState(object):
    """
    The ModelState class is used to compress the data of the model to a single object which is needed to integrate the undo mechanism.
    """    

    # initialises default paramter
    _data = None
    _position = None
    _output_data = None
    _output_args = []

    @property
    def data(self):
        """ Return data (PetriNetData-Object). """
        return self._data

    @property
    def position(self):
        """ Return positions (dictionary with position information for each place and transition; dictionary key is the component key). """
        return self._position

    @property
    def output(self):
        """ Return output data (simulation data). """
        return self._output_data

    @property
    def output_args(self):
        """ Return output arguments. """
        return self._output_args

    @data.setter
    def data(self, data):
        """ Set data (PetriNetData-Object). """
        self._data = data

    @position.setter
    def position(self, pos):
        """ Set positions (dictionary with position information for each place and transition; dictionary key is the component key). """
        self._position = pos

    @output.setter
    def output(self, data):
        """ Set output data (simulation data). """
        self._output_data = data

    @output_args.setter
    def output_args(self, args):
        """ Set output arguments. """
        self._output_args = args
