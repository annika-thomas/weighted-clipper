import numpy as np
import clipperpy

from .weight_association import weightAssociation
from .association import generateAssociationList


class EuclideanLandmarkMatcher:
    """
    Demonstrates a weighted CLIPPER solve by:
      1) Building an association list (dense cartesian product)
      2) Filtering associations using a size mismatch threshold
      3) Computing CLIPPER affinity/constraint
      4) Injecting per-association weights onto the diagonal of A
      5) Solving and returning selected associations
    """

    def __init__(self, epsilon: float, sizeLimit: float):
        self.epsilon = float(epsilon)
        self.sizeLimit = float(sizeLimit)

    def findAssociations(
        self,
        landmarkPositions1: np.ndarray,            # shape (N1, 3)
        landmarkPositionCovariances1: np.ndarray,  # unused (kept for API compatibility)
        landmarkSizes1: np.ndarray,                # shape (N1,)
        landmarkPositions2: np.ndarray,            # shape (N2, 3)
        landmarkPositionCovariances2: np.ndarray,  # unused
        landmarkSizes2: np.ndarray                 # shape (N2,)
    ) -> np.ndarray:
        # --- CLIPPER invariant / params ---
        iparams = clipperpy.invariants.EuclideanDistanceParams()
        iparams.epsilon = self.epsilon
        iparams.sigma = 0.5 * iparams.epsilon
        invariant = clipperpy.invariants.EuclideanDistance(iparams)

        params = clipperpy.Params()
        params.rounding = clipperpy.Rounding.DSD_HEU
        clipper = clipperpy.CLIPPER(invariant, params)

        # --- Association list (dense) ---
        numLandmarks1, _ = landmarkPositions1.shape
        numLandmarks2, _ = landmarkPositions2.shape
        assocList = generateAssociationList(numLandmarks1, numLandmarks2)

        # --- Pre-filter by size mismatch, compute per-association weights ---
        numAssocRows, _ = assocList.shape
        inliers = np.zeros(numAssocRows, dtype=bool)
        weights = np.zeros(numAssocRows, dtype=float)

        for assocRow in range(numAssocRows):
            idx1 = assocList[assocRow, 0]
            idx2 = assocList[assocRow, 1]

            lm1_size = float(landmarkSizes1[idx1])
            lm2_size = float(landmarkSizes2[idx2])

            # arithmetic mean change (normalized absolute difference)
            denom = (lm1_size + lm2_size)
            if denom <= 1e-12:
                arithMeanChange = np.inf
            else:
                arithMeanChange = 2.0 * abs(lm1_size - lm2_size) / denom

            # candidate inlier if below limit
            inliers[assocRow] = (arithMeanChange < self.sizeLimit)

            # weight using arbitrary function
            weights[assocRow] = weightAssociation(arithMeanChange, self.sizeLimit)

        # Drop obvious non-inliers and keep corresponding weights
        assocList = assocList[inliers, :]
        weights = weights[inliers]

        # --- CLIPPER scoring ---
        # NOTE: CLIPPER expects inputs as 3xN (column-major points),
        # while our API stores them as Nx3. So transpose here.
        clipper.score_pairwise_consistency(landmarkPositions1.T, landmarkPositions2.T, assocList)

        A = clipper.get_affinity_matrix()
        C = clipper.get_constraint_matrix()

        # --- Inject weights: put weights on A diagonal ---
        numInliers = len(weights)
        for i in range(numInliers):
            A[i, i] = weights[i]

        # Feed updated matrices back and solve
        clipper.set_matrix_data(A, C)
        clipper.solve()

        Ain = clipper.get_selected_associations()
        return Ain
