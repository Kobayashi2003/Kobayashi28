def ReverseKeyValue(dict1):
    """
    :param dict1: dict
    :return: dict
    """

    return {v: k for k, v in dict1.items()}


if __name__ == "__main__":

    dict1 = {"kobayashi" : "21312450"}

    print(ReverseKeyValue(dict1))  # {'21312450': 'kobayashi'}