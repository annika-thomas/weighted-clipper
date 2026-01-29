import clipperpy
import numpy as np
from AssociationWeighting import weightAssociation

def generateAssociationList(N1, N2):
    assocList = np.zeros((N1*N2,2),np.int32)

    i = 0

    for n1 in range(N1):
        for n2 in range(N2):
            assocList[i,0] = n1
            assocList[i,1] = n2
            i += 1

    return assocList

def dropBySize():
    return

class EuclideanLandmarkMatcher:
    def __init__(self, epsilon, sizeLimit):
        self.epsilon = epsilon
        self.sizeLimit = sizeLimit
        return
    
    def findAssociations(self, landmarkPositions1, landmarkPositionCovariances1, landmarkSizes1, landmarkPositions2, landmarkPositionCovariances2, landmarkSizes2):
        iparams = clipperpy.invariants.EuclideanDistanceParams()
        iparams.epsilon = self.epsilon
        iparams.sigma = 0.5 * iparams.epsilon
        invariant = clipperpy.invariants.EuclideanDistance(iparams)

        params = clipperpy.Params()
        params.rounding = clipperpy.Rounding.DSD_HEU
        clipper = clipperpy.CLIPPER(invariant, params)

        numLandmarks1, _ = landmarkPositions1.shape
        numLandmarks2, _ = landmarkPositions2.shape

        assocList = generateAssociationList(numLandmarks1, numLandmarks2)

        # Loop through association list and drop out associations where size is vastly different
        numAssocRows, _ = assocList.shape

        inliers = np.zeros(numAssocRows,dtype=bool)
        weights = np.zeros(numAssocRows,dtype=float)

        for assocRow in range(numAssocRows):
            idx1 = assocList[assocRow,0]
            idx2 = assocList[assocRow,1]
            
            lm1_size = landmarkSizes1[idx1]
            lm2_size = landmarkSizes2[idx2]

            # Compute arithmetic mean change
            arithMeanChange = 2*np.abs(lm1_size-lm2_size)/(lm1_size+lm2_size)

            # Consider an association a possible inlier only if size difference is below limit
            inliers[assocRow] = arithMeanChange < self.sizeLimit

            # Compute weight for association using an arbitrarily chosen function
            weights[assocRow] = weightAssociation(arithMeanChange, self.sizeLimit)
        
        # drop associations that are clearly not inliers, also update weights similarly
        assocList = assocList[inliers,:]
        weights = weights[inliers]

        clipper.score_pairwise_consistency(landmarkPositions1.T, landmarkPositions2.T, assocList)

        A = clipper.get_affinity_matrix()
        C = clipper.get_constraint_matrix()

        # put weights on A matrix diagonal
        numInliers = len(weights)
        for i in range(numInliers):
            A[i,i] = weights[i]

        # feed updated matrix back to Clipper and find associations
        clipper.set_matrix_data(A,C)
        clipper.solve()
        Ain = clipper.get_selected_associations()

        return Ain
