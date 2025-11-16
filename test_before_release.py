#!/usr/bin/env python3
"""
Pre-Release Test Suite for spacetime-playground
================================================

Comprehensive validation before pushing to GitHub.
Tests all critical components and ensures everything works.

Run this BEFORE your first release!

Usage:
    python test_before_release.py
"""

import os
import sys
import traceback
from pathlib import Path


# Color codes for pretty output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")


def print_test(test_name):
    print(f"{Colors.BOLD}[TEST]{Colors.END} {test_name}...", end=" ")
    sys.stdout.flush()


def print_pass():
    print(f"{Colors.GREEN}✓ PASS{Colors.END}")


def print_fail(error=""):
    print(f"{Colors.RED}✗ FAIL{Colors.END}")
    if error:
        print(f"{Colors.RED}  Error: {error}{Colors.END}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠ WARNING: {text}{Colors.END}")


def print_info(text):
    print(f"  {Colors.BLUE}ℹ{Colors.END} {text}")


# Test counter
tests_passed = 0
tests_failed = 0
tests_total = 0


def run_test(test_name, test_func):
    """Run a single test and track results."""
    global tests_passed, tests_failed, tests_total
    tests_total += 1

    print_test(test_name)

    try:
        result = test_func()
        if result:
            print_pass()
            tests_passed += 1
            return True
        else:
            print_fail()
            tests_failed += 1
            return False
    except Exception as e:
        print_fail(str(e))
        if "--verbose" in sys.argv:
            traceback.print_exc()
        tests_failed += 1
        return False


# ============================================================================
# TEST FUNCTIONS
# ============================================================================


def test_python_version():
    """Check Python version is 3.10+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_info(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    print_warning(f"Python {version.major}.{version.minor} (need 3.10+)")
    return False


def test_numpy_import():
    """Check numpy can be imported"""
    import numpy as np

    print_info(f"numpy {np.__version__}")
    return True


def test_scipy_import():
    """Check scipy can be imported"""
    import scipy

    print_info(f"scipy {scipy.__version__}")
    return True


def test_matplotlib_import():
    """Check matplotlib can be imported"""
    import matplotlib

    print_info(f"matplotlib {matplotlib.__version__}")
    return True


def test_metric_module_import():
    """Import metric.gaussian_warp module"""
    from metric.gaussian_warp import create_static_bubble_1d

    return True


def test_fields_module_import():
    """Import fields.scalar1d module"""
    from fields.scalar1d import ScalarWaveSolver1D, SimulationParameters

    return True


def test_sim_module_import():
    """Import sim.run_case module"""
    from sim.run_case import ExperimentOrchestrator

    return True


def test_metric_generation():
    """Generate and validate a metric"""
    import numpy as np
    from metric.gaussian_warp import create_static_bubble_1d

    warp = create_static_bubble_1d(amplitude=0.3, width=15.0, center=0.0)
    x = np.linspace(-50, 50, 200)
    g_xx, g_inv = warp.metric_1d(x)

    # Validate properties
    assert np.all(g_xx > 0), "Metric not positive!"
    assert np.all(np.isfinite(g_xx)), "Metric has NaN/Inf!"
    assert np.abs(g_xx[0] - 1.0) < 0.1, "Not asymptotically flat!"

    print_info(f"g_xx range: [{np.min(g_xx):.4f}, {np.max(g_xx):.4f}]")
    return True


def test_christoffel_symbols():
    """Compute Christoffel symbols"""
    import numpy as np
    from metric.gaussian_warp import create_static_bubble_1d

    warp = create_static_bubble_1d(amplitude=0.2, width=10.0, center=0.0)
    x = np.linspace(-50, 50, 200)
    dx = x[1] - x[0]

    gamma = warp.christoffel_1d(x, dx)

    assert np.all(np.isfinite(gamma)), "Christoffel has NaN/Inf!"
    print_info(f"Max |Γ|: {np.max(np.abs(gamma)):.4f}")
    return True


def test_field_initialization():
    """Initialize scalar field solver"""
    from fields.scalar1d import ScalarWaveSolver1D, SimulationParameters, gaussian_pulse

    params = SimulationParameters(
        Nx=100, Lx=50.0, T=10.0, dt=0.05, c=1.0, boundary="periodic"
    )

    solver = ScalarWaveSolver1D(params)
    solver.set_initial_conditions(
        phi_func=lambda x: gaussian_pulse(x, center=25.0, width=5.0, amplitude=1.0)
    )

    E0 = solver.compute_energy()
    assert E0 > 0, "Initial energy not positive!"
    assert np.isfinite(E0), "Initial energy is NaN/Inf!"

    print_info(f"Initial energy: {E0:.6f}")
    return True


def test_short_simulation():
    """Run a very short simulation"""
    import numpy as np
    from fields.scalar1d import ScalarWaveSolver1D, SimulationParameters, gaussian_pulse

    params = SimulationParameters(
        Nx=100, Lx=50.0, T=1.0, dt=0.05, c=1.0, boundary="periodic"
    )

    solver = ScalarWaveSolver1D(params)
    solver.set_initial_conditions(
        phi_func=lambda x: gaussian_pulse(x, center=25.0, width=5.0, amplitude=1.0)
    )

    E0 = solver.compute_energy()

    # Run 10 steps
    for _ in range(10):
        solver.step()

    E_final = solver.compute_energy()
    drift = abs(E_final - E0) / E0

    assert np.all(np.isfinite(solver.field.phi)), "Field has NaN/Inf!"
    assert drift < 0.1, f"Energy drift too large: {drift:.2%}"

    print_info(f"Energy drift: {drift:.4%}")
    return True


def test_curved_space_simulation():
    """Simulate field in curved space"""
    import numpy as np
    from fields.scalar1d import ScalarWaveSolver1D, SimulationParameters, gaussian_pulse
    from metric.gaussian_warp import create_static_bubble_1d

    params = SimulationParameters(
        Nx=100, Lx=50.0, T=1.0, dt=0.05, c=1.0, boundary="periodic"
    )

    solver = ScalarWaveSolver1D(params)

    # Set metric
    warp = create_static_bubble_1d(amplitude=0.3, width=10.0, center=25.0)
    g_xx, _ = warp.metric_1d(solver.x)
    solver.set_metric(g_xx)

    # Initialize field away from bubble
    solver.set_initial_conditions(
        phi_func=lambda x: gaussian_pulse(x, center=10.0, width=3.0, amplitude=1.0)
    )

    E0 = solver.compute_energy()

    # Run 10 steps
    for _ in range(10):
        solver.step()

    E_final = solver.compute_energy()
    drift = abs(E_final - E0) / E0

    assert drift < 0.15, f"Energy drift in curved space too large: {drift:.2%}"
    print_info(f"Curved space energy drift: {drift:.4%}")
    return True


def test_experiment_config_exists():
    """Check experiment configuration file exists"""
    config_path = Path("experiments/exp_scalar_warp_static.json")
    assert config_path.exists(), "Config file not found!"

    import json

    with open(config_path) as f:
        config = json.load(f)

    required_fields = ["name", "type", "metric", "simulation", "initial_conditions"]
    for field in required_fields:
        assert field in config, f"Missing field: {field}"

    print_info(f"Config: {config['name']}")
    return True


def test_experiment_orchestrator():
    """Test experiment orchestrator initialization"""
    from sim.run_case import ExperimentOrchestrator

    config_path = "experiments/exp_scalar_warp_static.json"
    orchestrator = ExperimentOrchestrator(config_path)

    assert orchestrator.config is not None, "Config not loaded!"
    print_info(f"Loaded: {orchestrator.config['name']}")
    return True


def test_documentation_files():
    """Check all documentation files exist"""
    docs = [
        "README.md",
        "QUICKSTART.md",
        "STATUS.md",
        "LICENSE",
        "requirements.txt",
        "docs/FORMULAE.md",
    ]

    missing = []
    for doc in docs:
        if not Path(doc).exists():
            missing.append(doc)

    if missing:
        print_warning(f"Missing: {', '.join(missing)}")
        return False

    print_info("All documentation present")
    return True


def test_module_structure():
    """Verify module structure is correct"""
    modules = [
        "metric/__init__.py",
        "fields/__init__.py",
        "sim/__init__.py",
        "tests/__init__.py",
    ]

    for module in modules:
        assert Path(module).exists(), f"Missing: {module}"

    print_info("Module structure correct")
    return True


def test_readme_content():
    """Check README has essential sections"""
    with open("README.md") as f:
        content = f.read().lower()

    sections = ["quick start", "install", "example", "license"]
    missing = [s for s in sections if s not in content]

    if missing:
        print_warning(f"README missing sections: {', '.join(missing)}")
        return False

    print_info("README complete")
    return True


def test_license_exists():
    """Check LICENSE file exists and is MIT"""
    with open("LICENSE") as f:
        content = f.read()

    assert "MIT License" in content, "Not MIT License!"
    print_info("MIT License confirmed")
    return True


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================


def main():
    print_header("SPACETIME-PLAYGROUND PRE-RELEASE TEST SUITE")

    print(
        f"{Colors.BOLD}This will validate all components before GitHub release.{Colors.END}"
    )
    print(f"{Colors.BOLD}Run with --verbose for detailed error messages.{Colors.END}\n")

    # Category: Dependencies
    print(f"\n{Colors.BOLD}[1/5] CHECKING DEPENDENCIES{Colors.END}")
    print("-" * 70)
    run_test("Python version 3.10+", test_python_version)
    run_test("numpy import", test_numpy_import)
    run_test("scipy import", test_scipy_import)
    run_test("matplotlib import", test_matplotlib_import)

    # Category: Module Imports
    print(f"\n{Colors.BOLD}[2/5] TESTING MODULE IMPORTS{Colors.END}")
    print("-" * 70)
    run_test("Import metric.gaussian_warp", test_metric_module_import)
    run_test("Import fields.scalar1d", test_fields_module_import)
    run_test("Import sim.run_case", test_sim_module_import)

    # Category: Core Functionality
    print(f"\n{Colors.BOLD}[3/5] VALIDATING CORE PHYSICS{Colors.END}")
    print("-" * 70)
    run_test("Generate metric", test_metric_generation)
    run_test("Compute Christoffel symbols", test_christoffel_symbols)
    run_test("Initialize field solver", test_field_initialization)
    run_test("Short flat-space simulation", test_short_simulation)
    run_test("Curved-space simulation", test_curved_space_simulation)

    # Category: Experiment System
    print(f"\n{Colors.BOLD}[4/5] TESTING EXPERIMENT SYSTEM{Colors.END}")
    print("-" * 70)
    run_test("Experiment config exists", test_experiment_config_exists)
    run_test("Orchestrator initialization", test_experiment_orchestrator)

    # Category: Documentation
    print(f"\n{Colors.BOLD}[5/5] VERIFYING DOCUMENTATION{Colors.END}")
    print("-" * 70)
    run_test("Module structure", test_module_structure)
    run_test("Documentation files", test_documentation_files)
    run_test("README content", test_readme_content)
    run_test("LICENSE file", test_license_exists)

    # Final Report
    print_header("TEST RESULTS")

    print(f"Total tests: {Colors.BOLD}{tests_total}{Colors.END}")
    print(f"Passed:      {Colors.GREEN}{tests_passed}{Colors.END}")
    print(f"Failed:      {Colors.RED}{tests_failed}{Colors.END}")

    success_rate = (tests_passed / tests_total) * 100 if tests_total > 0 else 0
    print(f"Success rate: {Colors.BOLD}{success_rate:.1f}%{Colors.END}")

    print()

    if tests_failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}{'=' * 70}{Colors.END}")
        print(
            f"{Colors.GREEN}{Colors.BOLD}{'✓ ALL TESTS PASSED - READY FOR RELEASE':^70}{Colors.END}"
        )
        print(f"{Colors.GREEN}{Colors.BOLD}{'=' * 70}{Colors.END}\n")

        print(f"{Colors.BOLD}Next steps:{Colors.END}")
        print(
            f"  1. Create GitHub repository: {Colors.BLUE}spacetime-playground{Colors.END}"
        )
        print(f"  2. Initialize git:")
        print(f"     {Colors.YELLOW}git init{Colors.END}")
        print(f"     {Colors.YELLOW}git add .{Colors.END}")
        print(
            f"     {Colors.YELLOW}git commit -m 'Initial commit: v0.1.0 Foundation'{Colors.END}"
        )
        print(f"  3. Push to GitHub:")
        print(
            f"     {Colors.YELLOW}git remote add origin git@github.com:m4rba4s/spacetime-playground.git{Colors.END}"
        )
        print(f"     {Colors.YELLOW}git branch -M main{Colors.END}")
        print(f"     {Colors.YELLOW}git push -u origin main{Colors.END}")
        print(f"  4. Share on Reddit: r/Physics, r/Python")
        print(f"\n{Colors.GREEN}Good luck with the release! 🚀{Colors.END}\n")

        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}{'=' * 70}{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}{'✗ SOME TESTS FAILED':^70}{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}{'=' * 70}{Colors.END}\n")

        print(f"{Colors.YELLOW}Please fix failing tests before release.{Colors.END}")
        print(
            f"Run with {Colors.BOLD}--verbose{Colors.END} flag for detailed errors.\n"
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())
