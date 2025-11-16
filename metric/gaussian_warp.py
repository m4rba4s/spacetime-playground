"""
Gaussian Warp Bubble Metric Generator

This module generates toy "warp bubble" metrics - localized Gaussian deformations
of flat spacetime geometry. These are NOT solutions to Einstein's equations and
do NOT represent physically realizable warp drives. They are pedagogical tools
for exploring how fields behave on variable geometric backgrounds.

Mathematical Foundation:
-----------------------
We start with flat Minkowski metric in (1+1)D or (2+1)D:
    ds² = -dt² + dx² (+ dy²)

And introduce a localized "shape function" f(x,y,t) that modifies spatial geometry:
    ds² = -dt² + [1 + f(x,y,t)]² dx² + dy²

where f is a Gaussian "bubble" that can be static or moving.

Physical Interpretation:
-----------------------
- f > 0: Space is "stretched" (expansion)
- f < 0: Space is "compressed" (contraction)
- Moving bubble: Center position changes with time
- These affect how waves propagate through the region

Author: Space-Playground Collective
License: MIT
"""

from dataclasses import dataclass
from typing import Callable, Optional, Tuple

import numpy as np


@dataclass
class WarpParameters:
    """
    Parameters defining a Gaussian warp bubble.

    Attributes:
        amplitude: Maximum metric deformation (dimensionless)
                   Typical range: [-0.5, 0.5] for numerical stability
        width: Spatial width of the bubble (in grid units)
        center_x: Initial x-position of bubble center
        center_y: Initial y-position (for 2D)
        velocity: Bubble velocity (for moving bubbles)
        time: Current time (for dynamic metrics)
    """

    amplitude: float = 0.2
    width: float = 10.0
    center_x: float = 0.0
    center_y: float = 0.0
    velocity: float = 0.0
    time: float = 0.0


class GaussianWarp:
    """
    Generator for Gaussian warp bubble metrics.

    This class creates localized geometric deformations that can be used
    to study field propagation on variable backgrounds.
    """

    def __init__(self, params: WarpParameters):
        """
        Initialize warp bubble generator.

        Parameters:
            params: WarpParameters object specifying bubble properties
        """
        self.params = params

    def shape_function_1d(self, x: np.ndarray) -> np.ndarray:
        """
        Compute 1D Gaussian shape function.

        Mathematical form:
            f(x,t) = A * exp(-((x - x₀(t))² / (2σ²)))
        where:
            x₀(t) = x₀ + v*t  (moving bubble)
            A = amplitude
            σ = width

        Parameters:
            x: Spatial coordinate array

        Returns:
            Shape function values f(x)
        """
        center = self.params.center_x + self.params.velocity * self.params.time
        sigma = self.params.width
        amplitude = self.params.amplitude

        f = amplitude * np.exp(-((x - center) ** 2) / (2 * sigma**2))
        return f

    def shape_function_2d(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Compute 2D Gaussian shape function.

        Mathematical form:
            f(x,y,t) = A * exp(-(r²/(2σ²)))
        where:
            r² = (x - x₀)² + (y - y₀)²

        Parameters:
            x: X-coordinate array (2D meshgrid)
            y: Y-coordinate array (2D meshgrid)

        Returns:
            Shape function values f(x,y)
        """
        center_x = self.params.center_x + self.params.velocity * self.params.time
        center_y = self.params.center_y
        sigma = self.params.width
        amplitude = self.params.amplitude

        r_squared = (x - center_x) ** 2 + (y - center_y) ** 2
        f = amplitude * np.exp(-r_squared / (2 * sigma**2))
        return f

    def conformal_factor_1d(self, x: np.ndarray) -> np.ndarray:
        """
        Compute conformal factor Ω(x) = 1 + f(x).

        The spatial metric is:
            g_xx = Ω²(x)

        Parameters:
            x: Spatial coordinate array

        Returns:
            Conformal factor Ω(x)
        """
        return 1.0 + self.shape_function_1d(x)

    def conformal_factor_2d(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Compute 2D conformal factor Ω(x,y) = 1 + f(x,y).

        Parameters:
            x: X-coordinate array
            y: Y-coordinate array

        Returns:
            Conformal factor Ω(x,y)
        """
        return 1.0 + self.shape_function_2d(x, y)

    def metric_1d(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute 1D spatial metric components.

        For (1+1)D spacetime:
            ds² = -dt² + g_xx dx²
        where:
            g_xx = [1 + f(x)]²

        Parameters:
            x: Spatial coordinate array

        Returns:
            g_xx: Spatial metric component
            g_xx_inv: Inverse spatial metric (1/g_xx)
        """
        omega = self.conformal_factor_1d(x)
        g_xx = omega**2
        g_xx_inv = 1.0 / g_xx

        return g_xx, g_xx_inv

    def metric_2d(self, x: np.ndarray, y: np.ndarray) -> dict:
        """
        Compute 2D spatial metric components.

        For (2+1)D spacetime with conformal deformation:
            ds² = -dt² + Ω²(dx² + dy²)

        This is a conformally flat metric where:
            g_xx = g_yy = Ω²(x,y)
            g_xy = 0

        Parameters:
            x: X-coordinate meshgrid
            y: Y-coordinate meshgrid

        Returns:
            Dictionary containing:
                'g_xx': Spatial metric g_xx
                'g_yy': Spatial metric g_yy
                'g_xy': Off-diagonal (zero for this metric)
                'conformal_factor': Ω(x,y)
                'det_g': Determinant of spatial metric
        """
        omega = self.conformal_factor_2d(x, y)
        omega_sq = omega**2

        return {
            "g_xx": omega_sq,
            "g_yy": omega_sq,
            "g_xy": np.zeros_like(omega),
            "conformal_factor": omega,
            "det_g": omega**4,  # det(g) = Ω⁴ for 2D conformal metric
            "sqrt_det_g": omega**2,
        }

    def christoffel_1d(self, x: np.ndarray, dx: float) -> np.ndarray:
        """
        Compute Christoffel symbols for 1D spatial metric.

        For metric g_xx = Ω², the non-zero component is:
            Γˣ_xx = ∂_x(ln Ω²) / 2 = (1/Ω) * ∂_x Ω

        Physical meaning: Describes how "straight lines" curve in this geometry.

        Parameters:
            x: Spatial coordinates
            dx: Grid spacing for numerical derivatives

        Returns:
            Gamma_xxx: Christoffel symbol Γˣ_xx
        """
        omega = self.conformal_factor_1d(x)

        # Compute ∂_x Ω using centered differences
        d_omega_dx = np.zeros_like(omega)
        d_omega_dx[1:-1] = (omega[2:] - omega[:-2]) / (2 * dx)
        # Boundary handling (one-sided differences)
        d_omega_dx[0] = (omega[1] - omega[0]) / dx
        d_omega_dx[-1] = (omega[-1] - omega[-2]) / dx

        gamma_xxx = d_omega_dx / omega

        return gamma_xxx

    def effective_wavespeed_1d(self, x: np.ndarray, c0: float = 1.0) -> np.ndarray:
        """
        Compute effective wave speed in deformed geometry.

        For a scalar wave on curved background, the effective speed is:
            v_eff(x) = c₀ / Ω(x)

        Physical interpretation:
        - Ω > 1 (expansion): waves slow down
        - Ω < 1 (compression): waves speed up

        Parameters:
            x: Spatial coordinates
            c0: Base wave speed in flat space (default: 1.0)

        Returns:
            Effective wave speed v_eff(x)
        """
        omega = self.conformal_factor_1d(x)
        return c0 / omega

    def update_time(self, new_time: float):
        """
        Update bubble time for dynamic simulations.

        Parameters:
            new_time: New time value
        """
        self.params.time = new_time


def create_static_bubble_1d(
    amplitude: float = 0.2, width: float = 10.0, center: float = 0.0
) -> GaussianWarp:
    """
    Convenience function: Create a static 1D warp bubble.

    Parameters:
        amplitude: Metric deformation strength
        width: Spatial extent of bubble
        center: Position of bubble center

    Returns:
        GaussianWarp object configured for static bubble

    Example:
        >>> warp = create_static_bubble_1d(amplitude=0.3, width=15.0)
        >>> x = np.linspace(-50, 50, 200)
        >>> g_xx, g_inv = warp.metric_1d(x)
    """
    params = WarpParameters(
        amplitude=amplitude, width=width, center_x=center, velocity=0.0, time=0.0
    )
    return GaussianWarp(params)


def create_moving_bubble_1d(
    amplitude: float = 0.2,
    width: float = 10.0,
    center: float = 0.0,
    velocity: float = 0.1,
) -> GaussianWarp:
    """
    Convenience function: Create a moving 1D warp bubble.

    Parameters:
        amplitude: Metric deformation strength
        width: Spatial extent of bubble
        center: Initial position
        velocity: Bubble velocity (in units of grid points per time unit)

    Returns:
        GaussianWarp object configured for moving bubble

    Example:
        >>> warp = create_moving_bubble_1d(velocity=0.5)
        >>> for t in range(100):
        >>>     warp.update_time(t * dt)
        >>>     g_xx, _ = warp.metric_1d(x)
    """
    params = WarpParameters(
        amplitude=amplitude, width=width, center_x=center, velocity=velocity, time=0.0
    )
    return GaussianWarp(params)


def create_static_bubble_2d(
    amplitude: float = 0.2,
    width: float = 10.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
) -> GaussianWarp:
    """
    Convenience function: Create a static 2D warp bubble.

    Parameters:
        amplitude: Metric deformation strength
        width: Spatial extent of bubble
        center_x: X-position of bubble center
        center_y: Y-position of bubble center

    Returns:
        GaussianWarp object configured for 2D static bubble

    Example:
        >>> warp = create_static_bubble_2d(amplitude=0.3, width=20.0)
        >>> x, y = np.meshgrid(np.linspace(-50, 50, 100),
        ...                     np.linspace(-50, 50, 100))
        >>> metric = warp.metric_2d(x, y)
    """
    params = WarpParameters(
        amplitude=amplitude,
        width=width,
        center_x=center_x,
        center_y=center_y,
        velocity=0.0,
    )
    return GaussianWarp(params)


# ============================================================================
# DIAGNOSTIC AND VISUALIZATION UTILITIES
# ============================================================================


def compute_metric_diagnostics(warp: GaussianWarp, x: np.ndarray) -> dict:
    """
    Compute diagnostic information about the metric.

    Useful for validation and visualization.

    Parameters:
        warp: GaussianWarp object
        x: Spatial coordinates

    Returns:
        Dictionary with diagnostic information:
            - max_deformation: Maximum metric deformation
            - min_wavespeed: Minimum effective wave speed
            - max_wavespeed: Maximum effective wave speed
            - bubble_center: Current bubble center position
    """
    g_xx, _ = warp.metric_1d(x)
    v_eff = warp.effective_wavespeed_1d(x)

    deformation = g_xx - 1.0  # Deviation from flat space

    return {
        "max_deformation": np.max(np.abs(deformation)),
        "min_wavespeed": np.min(v_eff),
        "max_wavespeed": np.max(v_eff),
        "bubble_center": warp.params.center_x + warp.params.velocity * warp.params.time,
        "amplitude": warp.params.amplitude,
        "width": warp.params.width,
    }


if __name__ == "__main__":
    # Quick visualization test
    import matplotlib.pyplot as plt

    print("=== Gaussian Warp Metric Generator Test ===\n")

    # Create test domain
    x = np.linspace(-50, 50, 500)

    # Test 1: Static bubble
    print("Test 1: Static warp bubble")
    warp_static = create_static_bubble_1d(amplitude=0.3, width=15.0, center=0.0)
    g_xx, g_inv = warp_static.metric_1d(x)

    diagnostics = compute_metric_diagnostics(warp_static, x)
    print(f"  Max deformation: {diagnostics['max_deformation']:.4f}")
    print(
        f"  Wave speed range: [{diagnostics['min_wavespeed']:.4f}, {diagnostics['max_wavespeed']:.4f}]"
    )

    # Test 2: Moving bubble at different times
    print("\nTest 2: Moving warp bubble")
    warp_moving = create_moving_bubble_1d(amplitude=0.3, width=15.0, velocity=0.5)

    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    # Plot metric
    axes[0].plot(x, g_xx, "b-", linewidth=2, label="Static bubble")

    for t in [0, 20, 40]:
        warp_moving.update_time(t)
        g_xx_moving, _ = warp_moving.metric_1d(x)
        axes[0].plot(x, g_xx_moving, "--", alpha=0.7, label=f"t = {t}")

    axes[0].axhline(y=1.0, color="k", linestyle=":", alpha=0.5, label="Flat space")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("g_xx")
    axes[0].set_title("Spatial Metric Component")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Plot effective wave speed
    warp_moving.update_time(0)
    v_eff = warp_moving.effective_wavespeed_1d(x)
    axes[1].plot(x, v_eff, "r-", linewidth=2)
    axes[1].axhline(y=1.0, color="k", linestyle=":", alpha=0.5)
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("v_eff / c")
    axes[1].set_title("Effective Wave Speed")
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("metric_test.png", dpi=150)
    print("\n✓ Plot saved as 'metric_test.png'")
    print("\n=== All tests passed ===")
