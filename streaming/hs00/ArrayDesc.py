# namespace:

import numpy as np

class ArrayDesc(object):
    """Defines the properties of an array detector result.

    An array type consists of these attributes:

    * name, a name for the array
    * shape, a tuple of lengths in 1 to N dimensions arranged as for C order
      arrays, i.e. (..., t, y, x), which is also the numpy shape
    * dtype, the data type of a single value, in numpy format
    * dimnames, a list of names for each dimension

    The class can try to determine if a given image-type can be converted
    to another.
    """

    def __init__(self, name, shape, dtype, dimnames=None):
        """Creates a datatype with given (numpy) shape and (numpy) data format.

        Also stores the 'names' of the used dimensions as a list called
        dimnames.  Defaults to 'X', 'Y' for 2D data and 'X', 'Y', 'Z' for 3D
        data.
        """
        self.name = name
        self.shape = shape
        self.dtype = np.dtype(dtype)
        if dimnames is None:
            dimnames = ['X', 'Y', 'Z', 'T', 'E', 'U', 'V', 'W'][:len(shape)]
        self.dimnames = dimnames

    def __repr__(self):
        return 'ArrayDesc(%r, %r, %r, %r)' % (self.name, self.shape,
                                              self.dtype, self.dimnames)

    def copy(self):
        return ArrayDesc(self.name, self.shape, self.dtype, self.dimnames)
