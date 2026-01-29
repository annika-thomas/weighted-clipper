import numpy as np

def make_synthetic_landmarks(N1=30, N2=35, noise=0.01, seed=7):
    """
    Generate two synthetic landmark sets with partially overlapping correspondences.

    Parameters
    ----------
    N1 : int
        Number of landmarks in set 1.
    N2 : int
        Number of landmarks in set 2.
    noise : float
        Standard deviation of Gaussian noise added to the positions of
        corresponding landmarks in set 2.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    P1 : (N1, 3) ndarray
        3D positions of landmarks in set 1.
    Cov1 : (N1, 3, 3) ndarray
        Per-landmark position covariances for set 1 (unused in this example,
        but included for API compatibility).
    S1 : (N1,) ndarray
        Scalar "size" attribute for each landmark in set 1.

    P2 : (N2, 3) ndarray
        3D positions of landmarks in set 2.
    Cov2 : (N2, 3, 3) ndarray
        Per-landmark position covariances for set 2 (unused).
    S2 : (N2,) ndarray
        Scalar "size" attribute for each landmark in set 2.

    (true_idx1, true_idx2) : tuple of ndarrays
        Indices of the planted ground-truth correspondences such that
        P1[true_idx1[k]] corresponds to P2[true_idx2[k]].
    """
    rng = np.random.default_rng(seed)

    # --- Landmark set 1 ---
    # P1: landmark positions (3D)
    P1 = rng.uniform(-1.0, 1.0, size=(N1, 3))

    # S1: per-landmark size attribute (used for association weighting)
    S1 = rng.uniform(0.05, 0.20, size=(N1,))

    # --- Ground-truth correspondences (subset) ---
    # Number of true correspondences we will plant between the two sets
    num_true = min(N1, N2, 20)

    # Indices of corresponding landmarks in set 1 and set 2
    true_idx1 = rng.choice(N1, size=num_true, replace=False)
    true_idx2 = rng.choice(N2, size=num_true, replace=False)

    # --- Landmark set 2 ---
    # P2: initial random landmark positions
    P2 = rng.uniform(-1.0, 1.0, size=(N2, 3))

    # S2: initial random landmark sizes
    S2 = rng.uniform(0.05, 0.20, size=(N2,))

    # Overwrite a subset of landmarks in set 2 to create true correspondences:
    # positions are copied from set 1 with added Gaussian noise
    P2[true_idx2] = P1[true_idx1] + rng.normal(
        scale=noise, size=(num_true, 3)
    )

    # Make sizes mostly consistent for true matches (small multiplicative noise)
    S2[true_idx2] = S1[true_idx1] * (
        1.0 + rng.normal(scale=0.05, size=num_true)
    )

    # --- Covariances ---
    # Placeholder covariances (not used by the matcher in this example)
    Cov1 = np.zeros((N1, 3, 3))
    Cov2 = np.zeros((N2, 3, 3))

    return P1, Cov1, S1, P2, Cov2, S2, (true_idx1, true_idx2)
