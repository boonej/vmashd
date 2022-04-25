# output.py
# Provides methods to format output.

def list_cols(t_list, cols, padding):
    """Outputs

    :param t_list: list of text to break up into columns
    :type t_list: List
    :param cols: desired number of columns
    :type cols: int
    :param padding: number of spaces between columns (at widest)
    :type padding: int
    :return: list of strings delimited to columns
    :rtype: List

    """
    longest = max(t_list, key=len)
    width = len(longest) + padding
    output = [''.join([f'{str:{width}}'
                       for str in t_list[i:i+cols]]) for i in range(
                           0,
                           len(t_list),
                           cols)]
    return output
