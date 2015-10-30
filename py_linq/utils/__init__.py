__author__ = 'Bruce.Fenske'

def is_null_or_empty(string):
    """
    Determines if the given string is null or empty
    :param string: unicode or str instance
    :return: boolean
    """
    return string is None or len(string) == 0
