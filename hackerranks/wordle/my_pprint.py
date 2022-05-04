

def pprint_alpha_dict(d):
    """ Prints key-value pairs in two columns. The 1st column sorted by key,
    ascending. The 2nd column is sorted by value, descending.

    Parameters
    ----------
    d : dict
        Dictionary to be printed.
        Assumes:
         - keys are exactly 1 character long
         - values are at most 6 characters long
         - there are less than 1000 entries
    """
    d_sorted_key = sorted(d.items(), key=lambda x: x[0])
    d_sorted_val = sorted(d.items(), key=lambda x: x[1], reverse=True)
    for i, key_item in enumerate(d_sorted_key):
        val_item = d_sorted_val[i]
        print("{} = {} {}: {} = {}".format(
            key_item[0], str(key_item[1]).ljust(6), str(i).rjust(3), val_item[0], val_item[1]))


def pprint_2d_alpha_dict(dd):
    """ Prints the given dictionary as a grid, each row representing a key-value
    pair, assuming the value is a list of ints. Emphasizes the highest value per
    column (same index of int-list value across all keys) with a preceding '*'.

    Parameters
    ----------
    dd : dict
        Dictionary to be printed.
        Assumes:
         - keys are exactly 1 character long
         - each value is a list of ints
         - all values are the same length
         - ints within the values are less than 1000000 (should be less
            than 6 digits for readable print out)
    """
    pad_count = 6
    index_count = len(list(dd.values())[0])
    max_counts = get_max_counts(dd)
    header = '  '
    for i in range(index_count):
        header += str(i+1).rjust(pad_count)
    print(header)

    dd_sorted_key = sorted(dd.items(), key=lambda x: x[0])
    for c, index_counts in dd_sorted_key:
        row = f'{c}:'
        for i, count in enumerate(index_counts):
            val_str = str(count)
            if count == max_counts[i]:
                val_str = '*' + val_str
            row += val_str.rjust(pad_count)
        print(row)


def get_max_counts(dd):
    """ Determines the max values per-index of the given dictionary's values,
    assumed to be list of ints.
        Ex:
            dd = {'a': [0, 1, 3],
                  'b': [1, -1, 0],
                  'c': [-1, 2, 1]}
            ->
            max_counts = [1, 2, 3]

    Parameters
    ----------
    dd : dict
        Dictionary to calculate statistics for.
        Assumes:
         - values are lists of ints
         - all values are the same length

    Returns
    -------
    max_counts : list of int
        Max values of each index of the passed parameter's values.
    """
    index_count = len(list(dd.values())[0])
    max_counts = [0] * index_count
    for i in range(index_count):
        max_counts[i] = sorted(dd.values(), key=lambda x: x[i], reverse=True)[0][i]
    return max_counts
