import math
import mmh3


class BloomFilter(object):

    """ Class for Bloom filter, using murmur3 hash function. Modified from
    https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/
        - Replaced usage of bitarray as to not require C compiler
        - Modified/fixed comments for understanding and convention
        - Changed class methods to static since they did not alter class state
    """

    def __init__(self, items_count, fp_prob):
        """
        Parameters
        ----------
        items_count : int
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False positive probability in decimal
        """
        # False positive probability in decimal
        self.fp_prob = fp_prob

        # Size of bit array to use
        self.size = self.get_size(items_count, fp_prob)

        # Number of hash functions to use
        self.hash_count = self.get_hash_count(self.size, items_count)

        # Initialize "bit" array of given size
        self.bit_array = [False] * self.size

    def add(self, item):
        """Add an item in the filter"""
        for i in range(self.hash_count):

            # Create digest for given item
            # i works as seed to mmh3.hash() function, giving us a new digest
            # with each iteration
            digest = mmh3.hash(item, i) % self.size

            # Set the bit to True in bit_array
            self.bit_array[digest] = True

    def check(self, item):
        """Check for existence of an item in filter"""
        for i in range(self.hash_count):

            # Recalculate digest for item to determine corresponding bit
            digest = mmh3.hash(item, i) % self.size

            if not self.bit_array[digest]:
                # If any bit is False then the item is not present in the filter
                # else there is probability that it exists
                return False

        return True

    @staticmethod
    def get_size(n, p):
        """ Calculate the size of the bit array (m) to be used using formula:
        m = -(n * lg(p)) / (lg(2)^2)

        Parameters
        ----------
        n : int
            Number of items expected to be stored in filter
        p : float
            False positive probability in decimal

        Returns
        -------
        int
            Size of bit array to be used
        """
        m = -(n * math.log(p)) / (math.log(2)**2)
        return int(m)

    @staticmethod
    def get_hash_count(m, n):
        """ Calculate the number of hash functions (k) to be used using formula:
        k = (m/n) * lg(2)

        Parameters
        ----------
        m : int
            size of bit array
        n : int
            number of items expected to be stored in filter

        Returns
        -------
        int
            Number of hash functions to be used
        """
        k = (m/n) * math.log(2)
        return int(k)
