def replace_none_values(d):

    """
    Replaces dict values that are None with 0

    Parameters
    ----------
    d : dict

    Returns
    -------
    dict

    Example
    -------
    >>> replace_none_values({'amount': None})
    {'amount': 0}
    """
    for key, value in d.items():
        if value is None:
            d['key'] = 0
    return d


test = {'amount__sum': None}


print(replace_none_values(test))
