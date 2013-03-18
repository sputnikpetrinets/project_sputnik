#!/usr/bin/python

class MementoContainer(object):
    """
    This class acts as container for Memento objects. It is also possible to set a storage limit to prevent the application to use to much memory.
    """

    _limit = 100
    _list_data = []
    _index = 0

    def __init__(self):
        """ Constructor of MementoContainer and default values will be initialised. """

        # call constructor of parent class
        super(MementoContainer, self).__init__()

        self._limit = 100
        self._list_data = []
        self._index = 0

    @property
    def storage_limit(self):
        """ Return storage limit of the container. """
        return self._limit
    
    @storage_limit.setter
    def storage_limit(self, limit):
        """ Set storage limit of the container. """
        self._limit = limit

    def undo(self):
        """ Return the last stored memento but does not delete the any mementos. If it is not possible to go any further back None will be returned. """
        # reduce index by 1
        self._index -= 1
        # check if index is valid
        if len(self._list_data) > self._index and self._index >= 0:
            # return memento
            return self._list_data[self._index]
        # check if index is invalid
        if self._index < 0:
            self._index = 0
        # no memento available
        return None

    def add(self, item):
        """ Add a new memento to the container. If the storage limit is exceeded the first memento will be deleted. """
        # check if the storage limit is reached
        if len(self._list_data) == self._limit:
            # delete oldest memento
            del self._list_data[0]
        # attach new memento
        self._list_data.append(item)
        # adapt index
        self._index = len(self._list_data)

    def remove(self, index):
        """ Remove a memento defined by its index. TRUE will be returned if the memento could be removed. """

        # check if the index is valid
        if index < len(self._list_data):
            # remove memento
            del self._list_data[index]
            # check if the current index needs to be adapted
            if index <= self._index:
                # adapt current index
                self._index -= 1
                if self._index < 0:
                    self._index = 0
            return True
        return False

    def remove_last_memento(self):
        """ Remove the last memento. """

        if len(self._list_data) > 0:
            del self._list_data[len(self._list_data) - 1]
