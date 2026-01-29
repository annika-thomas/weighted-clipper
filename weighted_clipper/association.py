import numpy as np

def generateAssociationList(N1: int, N2: int) -> np.ndarray:
    """
    Generate dense association list (cartesian product):
      assocList[k] = [idx_in_set1, idx_in_set2]
    Shape: (N1*N2, 2), dtype=int32
    """
    assocList = np.zeros((N1 * N2, 2), np.int32)

    i = 0
    for n1 in range(N1):
        for n2 in range(N2):
            assocList[i, 0] = n1
            assocList[i, 1] = n2
            i += 1

    return assocList
