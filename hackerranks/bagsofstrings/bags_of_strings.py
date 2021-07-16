import random
import string
from bloomfilter import BloomFilter


def get_bloom_filters_for_bags(bags, n=1000, fp_prob=0.5):
    """
    Parameters
    ----------
    bags : list of list of str
        The sets of strings to generate bloom filters for
    n : int
        Number of items expected to be in each bag
    fp_prob : float
        False positive probability for bloom filter in decimal

    Returns
    -------
    list of BloomFilter
        Array of BloomFilters populated by the corresponding bag in bags
    """
    bloom_filters = []
    for bag in bags:
        assert(len(bag) == n)
        bf = BloomFilter(n, fp_prob)
        for item in bag:
            bf.add(item)
        bloom_filters.append(bf)

    return bloom_filters


def get_bags_that_might_contain(bags, bloom_filters, target):
    """
    Parameters
    ----------
    bags : list of list of str
        The sets of strings to be searched
    bloom_filters : list of BloomFilter
        BloomFilters pre-populated by the corresponding bag in bags
    target : str
        The string to search for

    Returns
    -------
    list of list of str
        The set of bags that may contain the target string. False positive rate
        depends on the initialization of the bloom filters.
    """
    assert(len(bags) == len(bloom_filters))
    potential_bags = []
    for i, bf in enumerate(bloom_filters):
        if bf.check(target):
            potential_bags.append(bags[i])

    return potential_bags


def generate_random_bags(bag_count=1000,
                         item_count=1000,
                         char_set=string.ascii_letters,
                         max_length=10):
    """
    Parameters
    ----------
    bag_count : int
        Number of sets of strings to generate
    item_count : int
        Number of strings per set
    char_set : str
        Characters to be used for random string generation
    max_length : int
        Maximum length of each random string

    Returns
    -------
    list of list of str
        Set of "bags" with random strings
    """
    bags = []
    for i in range(bag_count):
        bag = []
        for j in range(item_count):
            rand_len = random.randint(1, max_length)
            bag.append(''.join(random.choice(char_set) for _ in range(rand_len)))
        bags.append(bag)

    return bags

