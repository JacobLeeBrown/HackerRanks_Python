
def my_atoi(s):
    """Convert string to 32-bit signed integer following algorithm of C's atoi
    function.

    Parameters
    ----------
    s : str
        String to parse

    Returns
    -------
    int
        32-bit signed integer value of parsed `s`
    """

    # Trim leading spaces
    s = s.lstrip(' ')

    if len(s) == 0:
        return 0

    # Read first character if it is a sign
    sign_multiplier = 1
    if s[0] in {'-', '+'}:
        if s[0] == '-':
            sign_multiplier = -1
        s = s[1:]
        if len(s) == 0:
            return 0

    # Read characters until first non-digit
    for i, char in enumerate(s):
        if char not in "1234567890":
            s = s[:i]
            break

    if len(s) == 0:
        return 0

    # Can now parse string to int (can only be positive)
    s_int = int(s)

    # Clamp to signed 32-bit bounds
    max_int = 2**31
    max_int = max_int if (sign_multiplier == -1) else (max_int - 1)
    s_int = min(s_int, max_int)

    # Return signed result
    return s_int * sign_multiplier
