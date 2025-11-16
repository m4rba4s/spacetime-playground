"""
Numerical Validation Tests for 1D Scalar Wave Solver

This test suite verifies:
1. Energy conservation in flat and curved space
2. Wave propagation accuracy against analytical solutions
3. Convergence under grid refinement
4. Boundary condition implementation
5. Metric integration correctness

Author: Space-Playground Collective
License: MIT
"""

import sys
from pathlib import Path

import numpy as np
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fields.scalar1d import (
    ScalarWaveSolver1D,
    SimulationParameters,
    gaussian_pulse,
    sine_wave,
)
from metric.gaussian_warp import create_static_bubble_1d


class TestScalarWaveSolver1D:
    """Test suite for 1D scalar wave solver."""

    def test_energy_conservation_flat_space(self):
        """Test that energy is conserved in flat spacetime."""
        params = SimulationParameters(
            Nx=200, Lx=100.0, T=50.0, dt=0.05, c=1.0, boundary="periodic"
        )

        solver = ScalarWaveSolver1D(params)
        solver.set_initial_conditions(
            phi_func=lambda x: gaussian_pulse(x, center=50.0, width=5.0, amplitude=1.0)
        )

        # Run simulation
        results = solver.run(save_interval=50)

        # Check energy conservation
        E0 = results["energy_history"][0]
        E_final = results["energy_history"][-1]
        relative_error = abs(E_final - E0) / E0

        assert relative_error < 0.01, (
            f"Energy not conserved: relative error = {relative_error:.4e}"
        )

    def test_flat_space_sine_wave_stability(self):
        """Test that sine wave remains stable in flat space."""
        params = SimulationParameters(
            Nx=100, Lx=50.0, T=25.0, dt=0.05, c=1.0, boundary="periodic"
        )

        solver = ScalarWaveSolver1D(params)

        # Initial sine wave (eigenmode for periodic BC)
        wavelength = params.Lx / 2.0  # n=2 mode
        solver.set_initial_conditions(
            phi_func=lambda x: sine_wave(x, wavelength=wavelength, amplitude=1.0)
        )

        # Run simulation
        results = solver.run(save_interval=10)

        # Check that field amplitude doesn't explode
        max_amplitude = np.max(np.abs(results["field_snapshots"]))
        assert max_amplitude < 2.0, (
            f"Field amplitude exploded: max = {max_amplitude:.4f}"
        )

        # Check energy conservation
        E0 = results["energy_history"][0]
        E_final = results["energy_history"][-1]
        relative_error = abs(E_final - E0) / E0

        assert relative_error < 0.02, f"Energy drift too large: {relative_error:.4e}"

    def test_wave_propagation_speed(self):
        """Test that waves propagate at correct speed in flat space."""
        c = 1.0
        params = SimulationParameters(
            Nx=400, Lx=200.0, T=40.0, dt=0.02, c=c, boundary="periodic"
        )

        solver = ScalarWaveSolver1D(params)

        # Narrow Gaussian pulse
        x0 = 50.0
        width = 2.0
        solver.set_initial_conditions(
            phi_func=lambda x: gaussian_pulse(x, center=x0, width=width, amplitude=1.0)
        )

        # Run for known time
        results = solver.run(save_interval=5)

        # Find pulse center at final time
        final_field = results["field_snapshots"][-1]
        final_time = results["time_snapshots"][-1]

        # Find center as maximum location
        center_idx = np.argmax(np.abs(final_field))
        x_final = results["x"][center_idx]

        # Expected displacement (accounting for periodic boundary)
        Lx = params.Lx
        expected_displacement = c * final_time
        actual_displacement = (x_final - x0) % Lx

        # Allow for numerical dispersion
        error = min(
            abs(actual_displacement - expected_displacement),
            abs(actual_displacement - expected_displacement + Lx),
            abs(actual_displacement - expected_displacement - Lx),
        )

        assert error < 5.0, f"Wave speed incorrect: error = {error:.2f}"

    def test_dirichlet_boundary_conditions(self):
        """Test that Dirichlet boundary conditions are properly enforced."""
        params = SimulationParameters(
            Nx=100, Lx=50.0, T=10.0, dt=0.05, c=1.0, boundary="dirichlet"
        )

        solver = ScalarWaveSolver1D(params)
        solver.set_initial_conditions(
            phi_func=lambda x: gaussian_pulse(x, center=25.0, width=5.0, amplitude=1.0)
        )

        # Run simulation
        results = solver.run(save_interval=5)

        # Check that boundaries remain zero
        for snapshot in results["field_snapshots"]:
            assert abs(snapshot[0]) < 1e-10, (
                f"Left boundary not zero: {snapshot[0]:.4e}"
            )
            assert abs(snapshot[-1]) < 1e-10, (
                f"Right boundary not zero: {snapshot[-1]:.4e}"
            )

    def test_convergence_under_refinement(self):
        """Test that solution converges as grid is refined."""
        # Coarse simulation
        params_coarse = SimulationParameters(
            Nx=100, Lx=50.0, T=10.0, dt=0.05, c=1.0, boundary="periodic"
        )

        solver_coarse = ScalarWaveSolver1D(params_coarse)
        solver_coarse.set_initial_conditions(
            phi_func=lambda x: gaussian_pulse(x, center=25.0, width=5.0, amplitude=1.0)
        )
        results_coarse = solver_coarse.run(save_interval=200)

        # Fine simulation
        params_fine = SimulationParameters(
            Nx=200, Lx=50.0, T=10.0, dt=0.025, c=1.0, boundary="periodic"
        )

        solver_fine = ScalarWaveSolver1D(params_fine)
        solver_fine.set_initial_conditions(
            phi_func=lambda x: gaussian_pulse(x, center=25.0, width=5.0, amplitude=1.0)
        )
        results_fine = solver_fine.run(save_interval=400)

        # Compare final energies
        E_coarse = results_coarse["energy_history"][-1]
        E_fine = results_fine["energy_history"][-1]
        E0_coarse = results_coarse["energy_history"][0]

        # Fine simulation should conserve energy better
        drift_coarse = abs(E_coarse - E0_coarse) / E0_coarse
        drift_fine = abs(E_fine - E0_coarse) / E0_coarse

        assert drift_fine <= drift_coarse, (
            "Fine grid should have better energy conservation"
        )

    def test_metric_integration(self):
        """Test that curved metric is properly integrated."""
        params = SimulationParameters(
            Nx=200, Lx=100.0, T=50.0, dt=0.05, c=1.0, boundary="periodic"
        )

        solver = ScalarWaveSolver1D(params)

        # Set up warp metric
        warp = create_static_bubble_1d(amplitude=0.3, width=15.0, center=50.0)
        g_xx, g_xx_inv = warp.metric_1d(solver.x)
        solver.set_metric(g_xx)

        # Verify metric was set correctly
        assert np.allclose(solver.g_xx, g_xx), "Metric not set correctly in solver"
        assert np.allclose(solver.g_xx_inv, g_xx_inv), (
            "Inverse metric not set correctly"
        )

        # Run simulation
        solver.set_initial_conditions(
            phi_func=lambda x: gaussian_pulse(x, center=20.0, width=5.0, amplitude=1.0)
        )

        results = solver.run(save_interval=50)

        # Check that simulation completes without errors
        assert len(results["field_snapshots"]) > 0, "No field snapshots generated"

        # Check energy is positive and finite
        for E in results["energy_history"]:
            assert E > 0, "Energy became negative"
            assert np.isfinite(E), "Energy became infinite or NaN"

    def test_energy_conservation_curved_space(self):
        """Test energy conservation in curved space."""
        params = SimulationParameters(
            Nx=200, Lx=100.0, T=40.0, dt=0.04, c=1.0, boundary="periodic"
        )

        solver = ScalarWaveSolver1D(params)

        # Set up warp metric
        warp = create_static_bubble_1d(amplitude=0.2, width=10.0, center=50.0)
        g_xx, _ = warp.metric_1d(solver.x)
        solver.set_metric(g_xx)

        # Initial pulse away from warp bubble
        solver.set_initial_conditions(
            phi_func=lambda x: gaussian_pulse(x, center=20.0, width=5.0, amplitude=1.0)
        )

        # Run simulation
        results = solver.run(save_interval=50)

        # Check energy conservation (should be slightly worse than flat space)
        E0 = results["energy_history"][0]
        E_final = results["energy_history"][-1]
        relative_error = abs(E_final - E0) / E0

        assert relative_error < 0.05, (
            f"Energy not conserved in curved space: error = {relative_error:.4e}"
        )

    def test_no_nan_or_inf(self):
        """Test that simulation never produces NaN or Inf values."""
        params = SimulationParameters(
            Nx=200, Lx=100.0, T=30.0, dt=0.05, c=1.0, boundary="periodic"
        )

        solver = ScalarWaveSolver1D(params)

        # Large amplitude to stress-test
        solver.set_initial_conditions(
            phi_func=lambda x: gaussian_pulse(x, center=50.0, width=5.0, amplitude=5.0)
        )

        results = solver.run(save_interval=20)

        # Check all snapshots for NaN/Inf
        for i, snapshot in enumerate(results["field_snapshots"]):
            assert np.all(np.isfinite(snapshot)), f"NaN/Inf detected at snapshot {i}"

        # Check energy history
        assert np.all(np.isfinite(results["energy_history"])), (
            "NaN/Inf in energy history"
        )

    def test_small_metric_deformation_limit(self):
        """Test that small metric deformations give nearly flat-space results."""
        params = SimulationParameters(
            Nx=200, Lx=100.0, T=40.0, dt=0.05, c=1.0, boundary="periodic"
        )

        # Flat space simulation
        solver_flat = ScalarWaveSolver1D(params)
        solver_flat.set_initial_conditions(
            phi_func=lambda x: gaussian_pulse(x, center=50.0, width=5.0, amplitude=1.0)
        )
        results_flat = solver_flat.run(save_interval=40)

        # Very small metric deformation
        solver_curved = ScalarWaveSolver1D(params)
        warp = create_static_bubble_1d(
            amplitude=0.01, width=15.0, center=50.0
        )  # 1% deformation
        g_xx, _ = warp.metric_1d(solver_curved.x)
        solver_curved.set_metric(g_xx)
        solver_curved.set_initial_conditions(
            phi_func=lambda x: gaussian_pulse(x, center=50.0, width=5.0, amplitude=1.0)
        )
        results_curved = solver_curved.run(save_interval=40)

        # Final fields should be very similar
        field_flat = results_flat["field_snapshots"][-1]
        field_curved = results_curved["field_snapshots"][-1]

        max_difference = np.max(np.abs(field_flat - field_curved))
        relative_difference = max_difference / np.max(np.abs(field_flat))

        assert relative_difference < 0.1, (
            f"Small metric should give similar results: diff = {relative_difference:.4e}"
        )


class TestInitialConditions:
    """Test initial condition generators."""

    def test_gaussian_pulse_properties(self):
        """Test that Gaussian pulse has correct properties."""
        x = np.linspace(0, 100, 200)
        center = 50.0
        width = 5.0
        amplitude = 1.0

        pulse = gaussian_pulse(x, center, width, amplitude)

        # Check maximum is at center
        max_idx = np.argmax(pulse)
        assert abs(x[max_idx] - center) < 1.0, "Gaussian not centered correctly"

        # Check amplitude
        assert abs(np.max(pulse) - amplitude) < 1e-10, "Gaussian amplitude incorrect"

        # Check decay to nearly zero far from center
        far_indices = np.where(np.abs(x - center) > 5 * width)[0]
        if len(far_indices) > 0:
            assert np.max(np.abs(pulse[far_indices])) < 0.01 * amplitude, (
                "Gaussian doesn't decay properly"
            )

    def test_sine_wave_periodicity(self):
        """Test that sine wave is periodic."""
        wavelength = 20.0
        x = np.linspace(0, 100, 200)

        wave = sine_wave(x, wavelength, amplitude=1.0)

        # Check approximate periodicity
        Lx = x[-1] - x[0]
        n_periods = int(Lx / wavelength)

        if n_periods >= 2:
            # Sample at one wavelength apart
            idx1 = 50
            idx2 = idx1 + int(len(x) * wavelength / Lx)

            if idx2 < len(x):
                assert abs(wave[idx1] - wave[idx2]) < 0.1, "Sine wave not periodic"


class TestMetricValidation:
    """Test metric generator integration."""

    def test_metric_positivity(self):
        """Test that metric remains positive."""
        warp = create_static_bubble_1d(amplitude=0.3, width=15.0, center=50.0)
        x = np.linspace(0, 100, 200)

        g_xx, g_xx_inv = warp.metric_1d(x)

        assert np.all(g_xx > 0), "Metric must be positive everywhere"
        assert np.all(g_xx_inv > 0), "Inverse metric must be positive"

    def test_metric_flatness_at_infinity(self):
        """Test that metric approaches flat space far from bubble."""
        warp = create_static_bubble_1d(amplitude=0.3, width=15.0, center=50.0)
        x = np.linspace(-100, 200, 600)

        g_xx, _ = warp.metric_1d(x)

        # Check edges are nearly flat
        edge_tolerance = 0.01
        assert abs(g_xx[0] - 1.0) < edge_tolerance, "Metric not flat at left boundary"
        assert abs(g_xx[-1] - 1.0) < edge_tolerance, "Metric not flat at right boundary"


def run_all_tests():
    """Run all tests and print summary."""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    print("=" * 70)
    print("SPACE-PLAYGROUND NUMERICAL VALIDATION TESTS")
    print("=" * 70)
    run_all_tests()
