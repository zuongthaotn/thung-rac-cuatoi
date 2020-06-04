


def peak(Data):
    return (Data[-3] < Data[-2]) and (Data[-2] > Data[-1])


def valley(Data):
    return (Data[-3] > Data[-2]) and (Data[-2] < Data[-1])
