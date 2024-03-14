def ReverseKeyValue(dict1):
    """
    :param dict1: dict
    :return: dict
    """
    return {v: k for k, v in dict1.items()}


if __name__ == "__main__":

    import random
    import string
    dict1 = {"kobayashi" : "21312450"}
    for i in range(10):
        r_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        r_id = ''.join(random.sample(string.digits, 8))
        dict1[r_name] = r_id

    print(ReverseKeyValue(dict1))  # {'21312450': 'kobayashi'}