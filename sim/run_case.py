"""
Experiment Orchestrator for Space-Playground

This module loads experiment configurations, runs simulations, and generates
visualizations and data exports.

Experiment Configuration Format (JSON):
---------------------------------------
{
    "name": "exp_scalar_warp_static",
    "description": "Static warp bubble with Gaussian pulse",
    "type": "scalar_1d",
    "metric": {
        "type": "gaussian_warp",
        "amplitude": 0.3,
        "width": 15.0,
        "center": 0.0,
        "velocity": 0.0
    },
    "simulation": {
        "Nx": 200,
        "Lx": 100.0,
        "T": 100.0,
        "dt": 0.05,
        "c": 1.0,
        "boundary": "periodic"
    },
    "initial_conditions": {
        "type": "gaussian_pulse",
        "center": 25.0,
        "width": 5.0,
        "amplitude": 1.0
    },
    "output": {
        "save_interval": 10,
        "export_csv": true,
        "export_plots": true,
        "export_animation": true
    }
}

Author: Space-Playground Collective
License: MIT
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fields.scalar1d import (
    ScalarWaveSolver1D,
    SimulationParameters,
    gaussian_pulse,
    sine_wave,
    wave_packet,
)
from metric.gaussian_warp import (
    GaussianWarp,
    WarpParameters,
    create_moving_bubble_1d,
    create_static_bubble_1d,
)


class ExperimentOrchestrator:
    """
    Orchestrates simulation experiments from configuration files.
    """

    def __init__(self, config_path: str):
        """
        Initialize orchestrator with experiment configuration.

        Parameters:
            config_path: Path to JSON configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.results = None
        self.output_dir = self._setup_output_dir()

    def _load_config(self) -> Dict[str, Any]:
        """Load and validate experiment configuration."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            config = json.load(f)

        # Validate required fields
        required = ["name", "type", "metric", "simulation", "initial_conditions"]
        for field in required:
            if field not in config:
                raise ValueError(f"Missing required field in config: {field}")

        return config

    def _setup_output_dir(self) -> Path:
        """Create output directory for results."""
        output_dir = self.config_path.parent / "results" / self.config["name"]
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    def _create_metric(self) -> GaussianWarp:
        """Create metric generator from configuration."""
        metric_config = self.config["metric"]
        metric_type = metric_config.get("type", "gaussian_warp")

        if metric_type == "gaussian_warp":
            amplitude = metric_config.get("amplitude", 0.2)
            width = metric_config.get("width", 10.0)
            center = metric_config.get("center", 0.0)
            velocity = metric_config.get("velocity", 0.0)

            if velocity == 0.0:
                return create_static_bubble_1d(amplitude, width, center)
            else:
                return create_moving_bubble_1d(amplitude, width, center, velocity)
        else:
            raise ValueError(f"Unknown metric type: {metric_type}")

    def _create_initial_conditions(self, x: np.ndarray):
        """Create initial field configuration."""
        ic_config = self.config["initial_conditions"]
        ic_type = ic_config.get("type", "gaussian_pulse")

        if ic_type == "gaussian_pulse":
            center = ic_config.get("center", 50.0)
            width = ic_config.get("width", 5.0)
            amplitude = ic_config.get("amplitude", 1.0)
            return gaussian_pulse(x, center, width, amplitude)

        elif ic_type == "sine_wave":
            wavelength = ic_config.get("wavelength", 20.0)
            amplitude = ic_config.get("amplitude", 1.0)
            return sine_wave(x, wavelength, amplitude)

        elif ic_type == "wave_packet":
            center = ic_config.get("center", 50.0)
            width = ic_config.get("width", 5.0)
            k0 = ic_config.get("k0", 1.0)
            amplitude = ic_config.get("amplitude", 1.0)
            return wave_packet(x, center, width, k0, amplitude)

        else:
            raise ValueError(f"Unknown initial condition type: {ic_type}")

    def run_simulation(self):
        """Execute the simulation."""
        print(f"\n{'=' * 60}")
        print(f"Experiment: {self.config['name']}")
        print(f"{'=' * 60}")
        print(f"Description: {self.config.get('description', 'N/A')}")
        print(f"Type: {self.config['type']}\n")

        # Setup simulation parameters
        sim_config = self.config["simulation"]
        params = SimulationParameters(
            Nx=sim_config.get("Nx", 200),
            Lx=sim_config.get("Lx", 100.0),
            T=sim_config.get("T", 100.0),
            dt=sim_config.get("dt", 0.05),
            c=sim_config.get("c", 1.0),
            boundary=sim_config.get("boundary", "periodic"),
        )

        # Create solver
        solver = ScalarWaveSolver1D(params)

        # Setup metric
        print("Setting up metric...")
        warp = self._create_metric()
        g_xx, g_xx_inv = warp.metric_1d(solver.x)
        solver.set_metric(g_xx)

        # Setup initial conditions
        print("Setting initial conditions...")
        phi_initial = self._create_initial_conditions(solver.x)
        solver.set_initial_conditions(phi_func=lambda x: phi_initial)

        # Run simulation
        print("\nRunning simulation...")
        output_config = self.config.get("output", {})
        save_interval = output_config.get("save_interval", 10)

        self.results = solver.run(save_interval=save_interval)
        self.results["metric"] = {"g_xx": g_xx, "warp_params": warp.params}

        print(f"\n{'=' * 60}")
        print("Simulation complete!")
        print(f"{'=' * 60}\n")

        return self.results

    def generate_plots(self):
        """Generate visualization plots."""
        if self.results is None:
            raise RuntimeError("No results to plot. Run simulation first.")

        print("Generating plots...")

        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        # 1. Field evolution
        ax1 = fig.add_subplot(gs[0, :])
        x = self.results["x"]
        snapshots = self.results["field_snapshots"]
        times = self.results["time_snapshots"]

        # Plot subset of snapshots
        indices = np.linspace(0, len(times) - 1, 8, dtype=int)
        cmap = plt.cm.viridis
        for idx in indices:
            t = times[idx]
            field = snapshots[idx]
            color = cmap(idx / len(indices))
            ax1.plot(
                x, field, color=color, alpha=0.7, linewidth=1.5, label=f"t={t:.1f}"
            )

        ax1.set_xlabel("x", fontsize=12)
        ax1.set_ylabel("φ(x,t)", fontsize=12)
        ax1.set_title("Scalar Field Evolution", fontsize=14, fontweight="bold")
        ax1.legend(ncol=4, fontsize=9)
        ax1.grid(alpha=0.3)

        # 2. Metric profile
        ax2 = fig.add_subplot(gs[1, 0])
        g_xx = self.results["metric"]["g_xx"]
        ax2.plot(x, g_xx, "b-", linewidth=2)
        ax2.axhline(y=1.0, color="gray", linestyle="--", alpha=0.5, label="Flat space")
        ax2.set_xlabel("x", fontsize=12)
        ax2.set_ylabel("g_xx", fontsize=12)
        ax2.set_title("Spatial Metric", fontsize=13, fontweight="bold")
        ax2.legend()
        ax2.grid(alpha=0.3)

        # 3. Energy conservation
        ax3 = fig.add_subplot(gs[1, 1])
        time_hist = self.results["time_history"]
        energy_hist = self.results["energy_history"]
        E0 = energy_hist[0]
        E_normalized = energy_hist / E0

        ax3.plot(time_hist, E_normalized, "r-", linewidth=2)
        ax3.axhline(y=1.0, color="gray", linestyle="--", alpha=0.5, label="E₀")
        ax3.set_xlabel("Time", fontsize=12)
        ax3.set_ylabel("E(t) / E(0)", fontsize=12)
        ax3.set_title("Energy Conservation", fontsize=13, fontweight="bold")
        ax3.legend()
        ax3.grid(alpha=0.3)

        # Add energy drift annotation
        dE_final = abs(E_normalized[-1] - 1.0)
        ax3.text(
            0.98,
            0.02,
            f"Final drift: {dE_final:.2e}",
            transform=ax3.transAxes,
            ha="right",
            va="bottom",
            fontsize=10,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

        # 4. Spacetime diagram
        ax4 = fig.add_subplot(gs[2, :])
        T_grid, X_grid = np.meshgrid(times, x)
        field_grid = snapshots.T  # Transpose for proper orientation

        im = ax4.pcolormesh(
            X_grid, T_grid, field_grid, shading="auto", cmap="RdBu_r", vmin=-1, vmax=1
        )
        ax4.set_xlabel("x", fontsize=12)
        ax4.set_ylabel("Time", fontsize=12)
        ax4.set_title("Spacetime Diagram", fontsize=13, fontweight="bold")
        plt.colorbar(im, ax=ax4, label="φ(x,t)")

        # Overall title
        fig.suptitle(
            f"Experiment: {self.config['name']}",
            fontsize=16,
            fontweight="bold",
            y=0.995,
        )

        # Save plot
        plot_path = self.output_dir / "summary.png"
        plt.savefig(plot_path, dpi=300, bbox_inches="tight")
        print(f"  ✓ Saved summary plot: {plot_path}")

        plt.close()

    def generate_animation(self):
        """Generate animation of field evolution."""
        if self.results is None:
            raise RuntimeError("No results to animate. Run simulation first.")

        print("Generating animation...")

        x = self.results["x"]
        snapshots = self.results["field_snapshots"]
        times = self.results["time_snapshots"]
        g_xx = self.results["metric"]["g_xx"]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # Field plot
        (line1,) = ax1.plot([], [], "b-", linewidth=2, label="φ(x,t)")
        ax1.plot(x, g_xx - 1, "gray", alpha=0.3, linestyle="--", label="Metric (g-1)")
        ax1.set_xlim(x[0], x[-1])
        ax1.set_ylim(
            1.1 * np.min(snapshots), 1.1 * np.max(snapshots)
        )  # Auto-scale with buffer
        ax1.set_xlabel("x")
        ax1.set_ylabel("φ")
        ax1.legend()
        ax1.grid(alpha=0.3)
        title = ax1.text(
            0.5,
            0.95,
            "",
            transform=ax1.transAxes,
            ha="center",
            va="top",
            fontsize=12,
            fontweight="bold",
        )

        # Energy plot
        energy_hist = self.results["energy_history"]
        E0 = energy_hist[0]
        (line2,) = ax2.plot([], [], "r-", linewidth=2)
        ax2.axhline(y=1.0, color="gray", linestyle="--", alpha=0.5)
        ax2.set_xlim(0, times[-1])
        ax2.set_ylim(0.98 * np.min(energy_hist / E0), 1.02 * np.max(energy_hist / E0))
        ax2.set_xlabel("Time")
        ax2.set_ylabel("E(t) / E(0)")
        ax2.grid(alpha=0.3)

        def init():
            line1.set_data([], [])
            line2.set_data([], [])
            return line1, line2, title

        def animate(i):
            line1.set_data(x, snapshots[i])
            title.set_text(f"t = {times[i]:.2f}")

            # Energy up to current time
            current_idx = int(i * len(energy_hist) / len(snapshots))
            line2.set_data(
                self.results["time_history"][:current_idx],
                energy_hist[:current_idx] / E0,
            )

            return line1, line2, title

        anim = FuncAnimation(
            fig, animate, init_func=init, frames=len(snapshots), interval=50, blit=True
        )

        # Save animation
        anim_path = self.output_dir / "animation.gif"
        writer = PillowWriter(fps=20)
        anim.save(anim_path, writer=writer)
        print(f"  ✓ Saved animation: {anim_path}")

        plt.close()

    def export_data(self):
        """Export results as CSV files."""
        if self.results is None:
            raise RuntimeError("No results to export. Run simulation first.")

        print("Exporting data...")

        # Export field snapshots
        field_data = np.column_stack(
            [self.results["x"]] + [snap for snap in self.results["field_snapshots"]]
        )
        header = "x," + ",".join(
            [f"phi_t_{t:.2f}" for t in self.results["time_snapshots"]]
        )
        field_path = self.output_dir / "field_snapshots.csv"
        np.savetxt(field_path, field_data, delimiter=",", header=header, comments="")
        print(f"  ✓ Saved field data: {field_path}")

        # Export energy history
        energy_data = np.column_stack(
            [self.results["time_history"], self.results["energy_history"]]
        )
        energy_path = self.output_dir / "energy_history.csv"
        np.savetxt(
            energy_path,
            energy_data,
            delimiter=",",
            header="time,energy",
            comments="",
        )
        print(f"  ✓ Saved energy data: {energy_path}")

        # Export configuration
        config_path = self.output_dir / "config.json"
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=4)
        print(f"  ✓ Saved configuration: {config_path}")

    def run_full_workflow(self):
        """Execute complete workflow: simulate, visualize, export."""
        # Run simulation
        self.run_simulation()

        # Generate outputs
        output_config = self.config.get("output", {})

        if output_config.get("export_plots", True):
            self.generate_plots()

        if output_config.get("export_animation", True):
            self.generate_animation()

        if output_config.get("export_csv", True):
            self.export_data()

        print(f"\n{'=' * 60}")
        print(f"All outputs saved to: {self.output_dir}")
        print(f"{'=' * 60}\n")


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python run_case.py <experiment_config.json>")
        print("\nExample:")
        print("  python sim/run_case.py experiments/exp_scalar_warp_static.json")
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        orchestrator = ExperimentOrchestrator(config_path)
        orchestrator.run_full_workflow()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
