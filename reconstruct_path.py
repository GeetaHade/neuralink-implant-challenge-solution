import argparse, pandas as pd, numpy as np, matplotlib.pyplot as plt

def reconstruct_positions(df, dt: float = 0.015):
    x = np.cumsum(df["velocity_x"].values * dt)
    y = np.cumsum(df["velocity_y"].values * dt)
    x = x - x.min()
    y = y - y.min()
    return x, y

def save_plot(xs, ys, fname, title):
    fig = plt.figure(figsize=(8, 4.5), dpi=150)
    plt.plot(xs, ys, linewidth=1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    fig.savefig(fname, bbox_inches="tight", pad_inches=0.0)
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser(description="Integrate mouse velocities to positions and plot.")
    ap.add_argument("--csv", default="mouse_velocities.csv")
    ap.add_argument("--dt", type=float, default=0.015)
    ap.add_argument("--out", default="positions.csv")
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    x, y = reconstruct_positions(df, args.dt)

    pd.DataFrame({"x": x, "y": y}).to_csv(args.out, index=False)
    save_plot(x, y, "trajectory_y_down.png", "Reconstructed (Y Down)")
    save_plot(x, y.max() - y, "trajectory_y_up.png", "Reconstructed (Y Up)")
    print("Wrote positions.csv, trajectory_y_down.png, trajectory_y_up.png")

if __name__ == "__main__":
    main()

