import matplotlib.pyplot as plt

def plot_sets_with_selected_associations(
    P1, P2, Ain, title="Weighted CLIPPER: selected associations"
):
    """
    Two side-by-side XY plots + lines connecting selected associations.
    Uses figure-coordinate transforms without offset.
    """
    X1, Y1 = P1[:, 0], P1[:, 1]
    X2, Y2 = P2[:, 0], P2[:, 1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle(title)

    ax1.scatter(X1, Y1)
    ax1.set_title("Set 1 (x-y)")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_aspect("equal", adjustable="box")

    ax2.scatter(X2, Y2)
    ax2.set_title("Set 2 (x-y)")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_aspect("equal", adjustable="box")

    # --- IMPORTANT: finalize layout BEFORE drawing lines ---
    plt.tight_layout()
    fig.canvas.draw()

    for a in Ain:
        i1 = int(a[0])
        i2 = int(a[1])

        # data → display → figure coordinates
        p1_disp = ax1.transData.transform((X1[i1], Y1[i1]))
        p2_disp = ax2.transData.transform((X2[i2], Y2[i2]))

        p1_fig = fig.transFigure.inverted().transform(p1_disp)
        p2_fig = fig.transFigure.inverted().transform(p2_disp)

        fig.add_artist(
            plt.Line2D(
                [p1_fig[0], p2_fig[0]],
                [p1_fig[1], p2_fig[1]],
                transform=fig.transFigure,
                alpha=0.35,
            )
        )

    plt.show()
