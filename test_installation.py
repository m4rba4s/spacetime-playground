#!/usr/bin/env python3
"""
Installation Test Script for Space-Playground

Quick verification that all components are working correctly.
Run this after installation to check your setup.

Usage:
    python test_installation.py
"""

import sys
from pathlib import Path

print("=" * 70)
print("SPACE-PLAYGROUND INSTALLATION TEST")
print("=" * 70)
print()

# Test 1: Check Python version
print("[1/6] Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 10:
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
else:
    print(f"  ✗ Python {version.major}.{version.minor} (Need 3.10+)")
    sys.exit(1)

# Test 2: Check dependencies
print("\n[2/6] Checking dependencies...")
required_packages = {
    "numpy": "numpy",
    "scipy": "scipy",
    "matplotlib": "matplotlib.pyplot",
}

missing = []
for name, import_path in required_packages.items():
    try:
        __import__(import_path)
        print(f"  ✓ {name}")
    except ImportError:
        print(f"  ✗ {name} (missing)")
        missing.append(name)

if missing:
    print(f"\n  Install missing packages: pip install {' '.join(missing)}")
    sys.exit(1)

# Test 3: Import Space-Playground modules
print("\n[3/6] Importing Space-Playground modules...")
try:
    from metric.gaussian_warp import create_static_bubble_1d

    print("  ✓ metric.gaussian_warp")
except ImportError as e:
    print(f"  ✗ metric.gaussian_warp: {e}")
    sys.exit(1)

try:
    from fields.scalar1d import ScalarWaveSolver1D, SimulationParameters

    print("  ✓ fields.scalar1d")
except ImportError as e:
    print(f"  ✗ fields.scalar1d: {e}")
    sys.exit(1)

# Test 4: Generate a metric
print("\n[4/6] Testing metric generation...")
try:
    import numpy as np

    warp = create_static_bubble_1d(amplitude=0.3, width=15.0, center=0.0)
    x = np.linspace(-50, 50, 200)
    g_xx, g_inv = warp.metric_1d(x)

    # Verify metric properties
    assert np.all(g_xx > 0), "Metric not positive!"
    assert np.all(np.isfinite(g_xx)), "Metric has NaN/Inf!"
    assert np.abs(g_xx[0] - 1.0) < 0.1, "Metric not asymptotically flat!"

    print(f"  ✓ Generated metric (max g_xx = {np.max(g_xx):.3f})")
except Exception as e:
    print(f"  ✗ Metric generation failed: {e}")
    sys.exit(1)

# Test 5: Run a short simulation
print("\n[5/6] Running short simulation...")
try:
    params = SimulationParameters(
        Nx=100, Lx=50.0, T=5.0, dt=0.05, c=1.0, boundary="periodic"
    )

    solver = ScalarWaveSolver1D(params)

    # Gaussian pulse
    from fields.scalar1d import gaussian_pulse

    solver.set_initial_conditions(
        phi_func=lambda x: gaussian_pulse(x, center=25.0, width=5.0, amplitude=1.0)
    )

    # Run for a few steps
    for _ in range(10):
        solver.step()

    # Check energy
    E = solver.compute_energy()
    assert E > 0, "Energy not positive!"
    assert np.isfinite(E), "Energy is NaN/Inf!"

    print(f"  ✓ Simulation ran successfully (E = {E:.6f})")
except Exception as e:
    print(f"  ✗ Simulation failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

# Test 6: Check experiment configuration exists
print("\n[6/6] Checking experiment files...")
exp_file = Path("experiments/exp_scalar_warp_static.json")
if exp_file.exists():
    print(f"  ✓ Found {exp_file}")
else:
    print(f"  ⚠ Missing {exp_file} (optional)")

print("\n" + "=" * 70)
print("ALL TESTS PASSED ✓")
print("=" * 70)
print("\nYour Space-Playground installation is ready!")
print("\nNext steps:")
print("  1. Run an experiment:")
print("     python sim/run_case.py experiments/exp_scalar_warp_static.json")
print("\n  2. Run full test suite:")
print("     pytest tests/test_scalar1d.py -v")
print("\n  3. Read the documentation:")
print("     QUICKSTART.md, README.md, docs/FORMULAE.md")
print("\n🌌 Happy exploring!")
