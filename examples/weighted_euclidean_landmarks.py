"""
This example demonstrates a *weighted* CLIPPER data-association pipeline.

We:
  1) Generate two synthetic sets of 2D/3D landmarks with partially overlapping
     "true" correspondences and associated landmark sizes.
  2) Construct a dense candidate association set between the two landmark sets.
  3) Filter and weight candidate associations based on landmark size consistency.
     (Associations with more similar sizes receive higher weights.)
  4) Run CLIPPER using a Euclidean distance invariant, injecting the per-association
     weights onto the diagonal of the CLIPPER affinity matrix.
  5) Solve for a consistent subset of associations using CLIPPER’s graph-theoretic
     optimization.
  6) Visualize the result by plotting the two landmark sets in x–y and drawing
     lines between the associations selected by CLIPPER.

This example is intentionally minimal and self-contained, and is meant to show
how CLIPPER can be extended to incorporate *weighted* association confidence
rather than relying on binary (inlier/outlier) decisions.
"""

from weighted_clipper.euclidean_landmark_matcher import EuclideanLandmarkMatcher
from weighted_clipper.plotting import plot_sets_with_selected_associations
from weighted_clipper.synthetic import make_synthetic_landmarks


def main():
    P1, Cov1, S1, P2, Cov2, S2, gt = make_synthetic_landmarks()
    true_idx1, true_idx2 = gt

    matcher = EuclideanLandmarkMatcher(epsilon=0.05, sizeLimit=0.40)
    Ain = matcher.findAssociations(P1, Cov1, S1, P2, Cov2, S2)

    print("Selected associations (idx1 -> idx2):")
    print(Ain)
    print(f"\nSelected: {len(Ain)} associations")

    # Quick sanity check: how many selected align with the planted correspondences?
    planted = set(zip(true_idx1.tolist(), true_idx2.tolist()))
    selected = set((int(a[0]), int(a[1])) for a in Ain)
    hits = len(planted.intersection(selected))
    print(f"Hits on planted correspondences: {hits}/{len(planted)}")

    plot_sets_with_selected_associations(P1, P2, Ain)


if __name__ == "__main__":
    main()
