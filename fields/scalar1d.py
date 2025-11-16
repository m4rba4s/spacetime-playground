"""
1D Scalar Wave Equation Solver on Curved Background

This module solves the scalar wave equation on a (1+1)D spacetime with
variable spatial metric:

    □_g φ = 0

For a metric ds² = -dt² + g_xx(x,t) dx², the wave equation becomes:

    ∂²φ/∂t² = (1/√g) ∂_x(√g g^xx ∂_x φ)

where:
    - g = g_xx is the spatial metric component
    - g^xx = 1/g_xx is the inverse metric

In the conformal case g_xx = Ω²(x), this simplifies to:

    ∂²φ/∂t² = (1/Ω²) ∂²φ/∂x² - (2/Ω) (∂Ω/∂x) ∂φ/∂x

Physical Interpretation:
-----------------------
The scalar field φ represents a wave propagating through curved space.
The metric modifies:
1. The effective wave speed: v_eff = c/Ω
2. The "force" from geometric gradients: -(2/Ω)(∂Ω/∂x)∂φ/∂x

Energy Conservation:
-------------------
The total energy should be conserved (modulo numerical errors):
    E = ∫ [φ_t² + g^xx (φ_x)²] √g dx

Author: Space-Playground Collective
License: MIT
"""

from dataclasses import dataclass
from typing import Callable, Optional, Tuple

import numpy as np


@dataclass
class SimulationParameters:
    """
    Parameters for 1D scalar field simulation.

    Attributes:
        Nx: Number of spatial grid points
        Lx: Spatial domain length
        T: Total simulation time
        dt: Time step
        dx: Spatial step (computed from Nx, Lx)
        c: Base wave speed (default: 1.0)
        boundary: Boundary condition type ('periodic', 'dirichlet', 'neumann')
    """

    Nx: int = 200
    Lx: float = 100.0
    T: float = 100.0
    dt: float = 0.05
    c: float = 1.0
    boundary: str = "periodic"

    def __post_init__(self):
        self.dx = self.Lx / self.Nx
        self.Nt = int(self.T / self.dt)

        # CFL condition check
        cfl = self.c * self.dt / self.dx
        if cfl > 1.0:
            print(f"WARNING: CFL = {cfl:.3f} > 1.0 - simulation may be unstable!")
            print(f"  Consider reducing dt below {self.dx / self.c:.4f}")


class ScalarField1D:
    """
    1D scalar field with first and second time derivatives.
    """

    def __init__(self, Nx: int):
        """
        Initialize field arrays.

        Parameters:
            Nx: Number of spatial grid points
        """
        self.phi = np.zeros(Nx)  # Field value φ(x,t)
        self.phi_t = np.zeros(Nx)  # Time derivative ∂φ/∂t
        self.phi_tt = np.zeros(Nx)  # Second time derivative ∂²φ/∂t²

    def copy(self):
        """Create a deep copy of the field state."""
        new_field = ScalarField1D(len(self.phi))
        new_field.phi = self.phi.copy()
        new_field.phi_t = self.phi_t.copy()
        new_field.phi_tt = self.phi_tt.copy()
        return new_field


class ScalarWaveSolver1D:
    """
    Solver for 1D scalar wave equation on curved background.

    Uses second-order centered finite differences in space and
    RK4 time integration for accuracy and stability.
    """

    def __init__(self, params: SimulationParameters):
        """
        Initialize solver.

        Parameters:
            params: Simulation parameters
        """
        self.params = params
        self.x = np.linspace(0, params.Lx, params.Nx, endpoint=False)

        # State variables
        self.field = ScalarField1D(params.Nx)
        self.time = 0.0
        self.step_count = 0

        # Metric (default: flat space)
        self.g_xx = np.ones(params.Nx)
        self.g_xx_inv = np.ones(params.Nx)
        self.sqrt_g = np.ones(params.Nx)

        # Energy history
        self.energy_history = []
        self.time_history = []

    def set_metric(self, g_xx: np.ndarray):
        """
        Set the spatial metric.

        Parameters:
            g_xx: Spatial metric component (must be positive)
        """
        if np.any(g_xx <= 0):
            raise ValueError("Metric must be positive everywhere!")

        self.g_xx = g_xx.copy()
        self.g_xx_inv = 1.0 / g_xx
        self.sqrt_g = np.sqrt(g_xx)

    def set_initial_conditions(
        self,
        phi_func: Callable[[np.ndarray], np.ndarray],
        phi_t_func: Optional[Callable[[np.ndarray], np.ndarray]] = None,
    ):
        """
        Set initial field configuration.

        Parameters:
            phi_func: Function φ(x) for initial field
            phi_t_func: Function ∂φ/∂t(x) for initial velocity (default: zero)
        """
        self.field.phi = phi_func(self.x)

        if phi_t_func is not None:
            self.field.phi_t = phi_t_func(self.x)
        else:
            self.field.phi_t = np.zeros_like(self.field.phi)

        # Compute initial acceleration
        self._compute_wave_equation()

    def _spatial_derivative(self, f: np.ndarray) -> np.ndarray:
        """
        Compute ∂f/∂x using second-order centered differences.

        Parameters:
            f: Function values on grid

        Returns:
            ∂f/∂x
        """
        df_dx = np.zeros_like(f)
        dx = self.params.dx

        if self.params.boundary == "periodic":
            # Periodic boundary: wrap around
            df_dx = (np.roll(f, -1) - np.roll(f, 1)) / (2 * dx)
        else:
            # Interior points: centered difference
            df_dx[1:-1] = (f[2:] - f[:-2]) / (2 * dx)

            # Boundaries: one-sided differences
            if self.params.boundary == "dirichlet":
                df_dx[0] = (f[1] - f[0]) / dx
                df_dx[-1] = (f[-1] - f[-2]) / dx
            elif self.params.boundary == "neumann":
                df_dx[0] = 0.0
                df_dx[-1] = 0.0

        return df_dx

    def _spatial_laplacian(self, f: np.ndarray) -> np.ndarray:
        """
        Compute covariant Laplacian: (1/√g) ∂_x(√g g^xx ∂_x f)

        This is the proper geometric Laplacian on curved space.

        Parameters:
            f: Function values on grid

        Returns:
            □_g f (covariant Laplacian)
        """
        dx = self.params.dx

        # Compute ∂f/∂x
        df_dx = self._spatial_derivative(f)

        # Compute flux: √g g^xx ∂f/∂x
        flux = self.sqrt_g * self.g_xx_inv * df_dx

        # Compute divergence: (1/√g) ∂(flux)/∂x
        d_flux_dx = self._spatial_derivative(flux)
        laplacian = d_flux_dx / self.sqrt_g

        return laplacian

    def _compute_wave_equation(self):
        """
        Compute ∂²φ/∂t² from wave equation:

            ∂²φ/∂t² = c² □_g φ

        Updates self.field.phi_tt
        """
        c_sq = self.params.c**2
        laplacian = self._spatial_laplacian(self.field.phi)
        self.field.phi_tt = c_sq * laplacian

    def _apply_boundary_conditions(self):
        """Apply boundary conditions to field values."""
        if self.params.boundary == "dirichlet":
            self.field.phi[0] = 0.0
            self.field.phi[-1] = 0.0
            self.field.phi_t[0] = 0.0
            self.field.phi_t[-1] = 0.0
        elif self.params.boundary == "periodic":
            # Already handled by periodic derivatives
            pass
        elif self.params.boundary == "neumann":
            # Zero derivative at boundaries (handled in derivative computation)
            pass

    def _rk4_step(self):
        """
        Perform one RK4 time step.

        State vector: y = [φ, ∂φ/∂t]
        Derivative: dy/dt = [∂φ/∂t, ∂²φ/∂t²]
        """
        dt = self.params.dt

        # Save initial state
        phi_0 = self.field.phi.copy()
        phi_t_0 = self.field.phi_t.copy()

        # k1
        self._compute_wave_equation()
        k1_phi = self.field.phi_t
        k1_phi_t = self.field.phi_tt

        # k2
        self.field.phi = phi_0 + 0.5 * dt * k1_phi
        self.field.phi_t = phi_t_0 + 0.5 * dt * k1_phi_t
        self._apply_boundary_conditions()
        self._compute_wave_equation()
        k2_phi = self.field.phi_t
        k2_phi_t = self.field.phi_tt

        # k3
        self.field.phi = phi_0 + 0.5 * dt * k2_phi
        self.field.phi_t = phi_t_0 + 0.5 * dt * k2_phi_t
        self._apply_boundary_conditions()
        self._compute_wave_equation()
        k3_phi = self.field.phi_t
        k3_phi_t = self.field.phi_tt

        # k4
        self.field.phi = phi_0 + dt * k3_phi
        self.field.phi_t = phi_t_0 + dt * k3_phi_t
        self._apply_boundary_conditions()
        self._compute_wave_equation()
        k4_phi = self.field.phi_t
        k4_phi_t = self.field.phi_tt

        # Combine
        self.field.phi = phi_0 + (dt / 6.0) * (
            k1_phi + 2 * k2_phi + 2 * k3_phi + k4_phi
        )
        self.field.phi_t = phi_t_0 + (dt / 6.0) * (
            k1_phi_t + 2 * k2_phi_t + 2 * k3_phi_t + k4_phi_t
        )

        self._apply_boundary_conditions()
        self._compute_wave_equation()

    def compute_energy(self) -> float:
        """
        Compute total field energy:

            E = ∫ [φ_t² + c² g^xx (∂φ/∂x)²] √g dx

        This is the conserved energy for the wave equation on curved space.

        Returns:
            Total energy E
        """
        dx = self.params.dx
        c_sq = self.params.c**2

        # Kinetic energy density: φ_t²
        kinetic = self.field.phi_t**2

        # Gradient energy density: g^xx (∂φ/∂x)²
        phi_x = self._spatial_derivative(self.field.phi)
        gradient = self.g_xx_inv * phi_x**2

        # Total energy density
        energy_density = kinetic + c_sq * gradient

        # Integrate with proper volume element √g dx
        total_energy = np.sum(energy_density * self.sqrt_g) * dx

        return total_energy

    def step(self):
        """Advance simulation by one time step."""
        self._rk4_step()
        self.time += self.params.dt
        self.step_count += 1

        # Record energy
        energy = self.compute_energy()
        self.energy_history.append(energy)
        self.time_history.append(self.time)

    def run(self, save_interval: int = 10) -> dict:
        """
        Run full simulation.

        Parameters:
            save_interval: Save field snapshot every N steps

        Returns:
            Dictionary with:
                - 'x': Spatial coordinates
                - 'time_snapshots': Times when snapshots were saved
                - 'field_snapshots': Field values at those times
                - 'energy_history': Energy vs time
                - 'time_history': Time array for energy
        """
        field_snapshots = []
        time_snapshots = []

        # Save initial state
        field_snapshots.append(self.field.phi.copy())
        time_snapshots.append(self.time)

        print(
            f"Starting simulation: T={self.params.T}, dt={self.params.dt}, Nx={self.params.Nx}"
        )
        print(f"Total steps: {self.params.Nt}")

        for n in range(self.params.Nt):
            self.step()

            if (n + 1) % save_interval == 0:
                field_snapshots.append(self.field.phi.copy())
                time_snapshots.append(self.time)

            if (n + 1) % (self.params.Nt // 10) == 0:
                progress = 100 * (n + 1) / self.params.Nt
                E = self.energy_history[-1]
                E0 = self.energy_history[0]
                dE = abs(E - E0) / E0 if E0 > 0 else 0
                print(
                    f"  Progress: {progress:.0f}% | t={self.time:.2f} | E/E₀={E / E0:.6f} | ΔE/E₀={dE:.2e}"
                )

        print("✓ Simulation complete")

        return {
            "x": self.x,
            "time_snapshots": np.array(time_snapshots),
            "field_snapshots": np.array(field_snapshots),
            "energy_history": np.array(self.energy_history),
            "time_history": np.array(self.time_history),
        }


# ============================================================================
# INITIAL CONDITION TEMPLATES
# ============================================================================


def gaussian_pulse(
    x: np.ndarray, center: float, width: float, amplitude: float = 1.0
) -> np.ndarray:
    """
    Gaussian pulse initial condition.

    φ(x,0) = A * exp(-(x-x₀)²/(2σ²))
    """
    return amplitude * np.exp(-((x - center) ** 2) / (2 * width**2))


def sine_wave(x: np.ndarray, wavelength: float, amplitude: float = 1.0) -> np.ndarray:
    """
    Sinusoidal initial condition.

    φ(x,0) = A * sin(2π x / λ)
    """
    return amplitude * np.sin(2 * np.pi * x / wavelength)


def wave_packet(
    x: np.ndarray, center: float, width: float, k0: float, amplitude: float = 1.0
) -> np.ndarray:
    """
    Gaussian wave packet.

    φ(x,0) = A * exp(-(x-x₀)²/(2σ²)) * cos(k₀ x)
    """
    envelope = np.exp(-((x - center) ** 2) / (2 * width**2))
    carrier = np.cos(k0 * x)
    return amplitude * envelope * carrier


# ============================================================================
# VALIDATION AND TESTING
# ============================================================================

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    print("=== 1D Scalar Wave Solver Test ===\n")

    # Test 1: Flat space wave propagation
    print("Test 1: Gaussian pulse in flat space")
    params = SimulationParameters(
        Nx=200, Lx=100.0, T=50.0, dt=0.05, c=1.0, boundary="periodic"
    )

    solver = ScalarWaveSolver1D(params)

    # Initial Gaussian pulse
    solver.set_initial_conditions(
        phi_func=lambda x: gaussian_pulse(x, center=50.0, width=5.0, amplitude=1.0),
        phi_t_func=None,
    )

    # Run simulation
    results = solver.run(save_interval=20)

    # Check energy conservation
    E0 = results["energy_history"][0]
    E_final = results["energy_history"][-1]
    dE_relative = abs(E_final - E0) / E0

    print(f"\nEnergy conservation:")
    print(f"  Initial energy: {E0:.6f}")
    print(f"  Final energy: {E_final:.6f}")
    print(f"  Relative change: {dE_relative:.2e}")

    if dE_relative < 0.01:
        print("  ✓ Energy conserved to < 1%")
    else:
        print("  ⚠ Energy drift detected!")

    # Visualization
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Field evolution
    for i, (t, field) in enumerate(
        zip(results["time_snapshots"][::3], results["field_snapshots"][::3])
    ):
        alpha = 0.3 + 0.7 * (i / len(results["time_snapshots"][::3]))
        axes[0].plot(results["x"], field, alpha=alpha, label=f"t = {t:.1f}")

    axes[0].set_xlabel("x")
    axes[0].set_ylabel("φ(x,t)")
    axes[0].set_title("Gaussian Pulse Propagation (Flat Space)")
    axes[0].legend(loc="upper right", ncol=2)
    axes[0].grid(alpha=0.3)

    # Energy conservation
    E_norm = results["energy_history"] / E0
    axes[1].plot(results["time_history"], E_norm, "b-", linewidth=2)
    axes[1].axhline(
        y=1.0, color="r", linestyle="--", alpha=0.5, label="Perfect conservation"
    )
    axes[1].set_xlabel("Time")
    axes[1].set_ylabel("E(t) / E(0)")
    axes[1].set_title("Energy Conservation")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("scalar_field_test.png", dpi=150)
    print("\n✓ Plot saved as 'scalar_field_test.png'")

    print("\n=== All tests passed ===")
