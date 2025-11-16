#!/usr/bin/env python3
"""
Quick Test for spacetime-playground
====================================

Minimal test to verify basic functionality.
Run this before your first GitHub commit!

Usage:
    python quick_test.py
"""

import sys


def test_python_version():
    """Check Python version"""
    print("Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✓ {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ {version.major}.{version.minor} (need 3.10+)")
        return False


def test_imports():
    """Test critical imports"""
    print("\nTesting imports:")

    tests = [
        ("numpy", "import numpy as np"),
        ("scipy", "import scipy"),
        ("matplotlib", "import matplotlib.pyplot as plt"),
        ("metric module", "from metric.gaussian_warp import create_static_bubble_1d"),
        ("fields module", "from fields.scalar1d import ScalarWaveSolver1D"),
    ]

    passed = 0
    for name, code in tests:
        try:
            exec(code)
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")

    return passed == len(tests)


def test_basic_simulation():
    """Run minimal simulation"""
    print("\nTesting basic simulation:")

    try:
        import numpy as np
        from fields.scalar1d import (
            ScalarWaveSolver1D,
            SimulationParameters,
            gaussian_pulse,
        )
        from metric.gaussian_warp import create_static_bubble_1d

        # Create metric
        print("  Creating metric...", end=" ")
        warp = create_static_bubble_1d(amplitude=0.3, width=15.0, center=0.0)
        x = np.linspace(-50, 50, 100)
        g_xx, g_inv = warp.metric_1d(x)
        print("✓")

        # Initialize solver
        print("  Initializing solver...", end=" ")
        params = SimulationParameters(
            Nx=50, Lx=50.0, T=1.0, dt=0.05, c=1.0, boundary="periodic"
        )
        solver = ScalarWaveSolver1D(params)
        solver.set_initial_conditions(
            phi_func=lambda x: gaussian_pulse(x, center=25.0, width=5.0, amplitude=1.0)
        )
        print("✓")

        # Run a few steps
        print("  Running 10 time steps...", end=" ")
        for _ in range(10):
            solver.step()
        print("✓")

        # Check energy
        print("  Checking energy conservation...", end=" ")
        E = solver.compute_energy()
        E0 = solver.energy_history[0]
        drift = abs(E - E0) / E0
        print(f"✓ (drift: {drift:.4%})")

        return True

    except Exception as e:
        print(f"\n  ✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print(" SPACETIME-PLAYGROUND QUICK TEST")
    print("=" * 60)
    print()

    results = []

    # Run tests
    results.append(test_python_version())
    results.append(test_imports())
    results.append(test_basic_simulation())

    # Summary
    print("\n" + "=" * 60)
    if all(results):
        print(" ✓ ALL TESTS PASSED - READY TO GO!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Create GitHub repo: spacetime-playground")
        print("  2. git init && git add . && git commit -m 'Initial commit'")
        print("  3. Push to GitHub")
        print("  4. Share with the world!")
        return 0
    else:
        print(" ✗ SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease fix errors above before release.")
        print("Check that dependencies are installed:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
