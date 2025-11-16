# 🚀 Quick Start Guide

**Get your first simulation running in 5 minutes.**

---

## Prerequisites

- Python 3.10 or higher
- 5 minutes of your time

---

## Step 1: Install Dependencies

```bash
cd space-playground
pip install numpy scipy matplotlib imageio Pillow numba pytest
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

---

## Step 2: Run Your First Experiment

```bash
python sim/run_case.py experiments/exp_scalar_warp_static.json
```

**What happens:**
- A Gaussian wave pulse launches from x=20
- It encounters a static warp bubble at x=50
- The wave slows down, partially reflects, and accumulates phase shifts
- Simulation runs for 80 time units
- Results saved to `experiments/results/exp_scalar_warp_static/`

**Expected output:**
```
==============================================================
Experiment: exp_scalar_warp_static
==============================================================
Description: Static warp bubble with Gaussian pulse
Type: scalar_1d

Setting up metric...
Setting initial conditions...

Running simulation...
Starting simulation: T=80.0, dt=0.04, Nx=400
Total steps: 2000
  Progress: 10% | t=8.00 | E/E₀=1.000032 | ΔE/E₀=3.18e-05
  Progress: 20% | t=16.00 | E/E₀=0.999967 | ΔE/E₀=3.32e-05
  Progress: 30% | t=24.00 | E/E₀=1.000015 | ΔE/E₀=1.51e-05
  ...
✓ Simulation complete

Generating plots...
  ✓ Saved summary plot: experiments/results/.../summary.png
Generating animation...
  ✓ Saved animation: experiments/results/.../animation.gif
Exporting data...
  ✓ Saved field data: experiments/results/.../field_snapshots.csv
  ✓ Saved energy data: experiments/results/.../energy_history.csv
  ✓ Saved configuration: experiments/results/.../config.json

==============================================================
All outputs saved to: experiments/results/exp_scalar_warp_static
==============================================================
```

**Time:** ~30-60 seconds depending on your CPU.

---

## Step 3: View Results

### Summary Plot
Open `experiments/results/exp_scalar_warp_static/summary.png`

You'll see:
- **Top:** Field evolution over time (colored lines)
- **Middle left:** Spatial metric profile (the warp bubble)
- **Middle right:** Energy conservation plot (should be flat!)
- **Bottom:** Spacetime diagram (field as heatmap)

### Animation
Open `experiments/results/exp_scalar_warp_static/animation.gif`

Watch the wave propagate through curved space in real-time.

### Data Files
- `field_snapshots.csv` - Raw field values for further analysis
- `energy_history.csv` - Energy vs. time
- `config.json` - Exact parameters used (for reproducibility)

---

## Step 4: Run Numerical Tests

Verify everything works correctly:

```bash
pytest tests/test_scalar1d.py -v
```

**Expected:**
```
tests/test_scalar1d.py::TestScalarWaveSolver1D::test_energy_conservation_flat_space PASSED
tests/test_scalar1d.py::TestScalarWaveSolver1D::test_flat_space_sine_wave_stability PASSED
tests/test_scalar1d.py::TestScalarWaveSolver1D::test_wave_propagation_speed PASSED
...

==================== 12 passed in 45.23s ====================
```

**If tests fail:** Check your Python version and dependencies.

---

## Step 5: Create Your Own Experiment

Copy the template:

```bash
cp experiments/exp_scalar_warp_static.json experiments/my_experiment.json
```

Edit `my_experiment.json`:

```json
{
    "name": "my_experiment",
    "description": "My first custom experiment!",
    "type": "scalar_1d",
    "metric": {
        "type": "gaussian_warp",
        "amplitude": 0.4,        ← Change this!
        "width": 20.0,           ← And this!
        "center": 60.0,
        "velocity": 0.0
    },
    "simulation": {
        "Nx": 400,
        "Lx": 100.0,
        "T": 100.0,              ← Longer simulation
        "dt": 0.04,
        "c": 1.0,
        "boundary": "periodic"
    },
    "initial_conditions": {
        "type": "gaussian_pulse",
        "center": 20.0,
        "width": 3.0,            ← Narrower pulse
        "amplitude": 1.0
    },
    "output": {
        "save_interval": 10,
        "export_csv": true,
        "export_plots": true,
        "export_animation": true
    }
}
```

Run it:

```bash
python sim/run_case.py experiments/my_experiment.json
```

---

## What Can You Tweak?

### Metric Parameters
- **amplitude** (0.0 - 0.5): Strength of space deformation
  - 0.0 = flat space
  - 0.3 = moderate warp
  - 0.5 = strong warp (may cause instability)
- **width** (5.0 - 30.0): Size of the bubble
- **center**: Where the bubble sits
- **velocity** (0.0 - 0.3): Moving bubble speed

### Simulation Parameters
- **Nx** (200-800): Grid resolution (more = slower but more accurate)
- **T** (50-200): Total simulation time
- **dt** (0.01-0.1): Time step (smaller = more stable, must satisfy CFL < 1)
- **boundary**: 'periodic', 'dirichlet', or 'neumann'

### Initial Conditions
- **type**: 'gaussian_pulse', 'sine_wave', 'wave_packet'
- **center**: Starting position
- **width**: Pulse width
- **amplitude**: Initial field strength

---

## Troubleshooting

### "CFL > 1.0 - simulation may be unstable!"
**Solution:** Reduce `dt` or increase `Nx`:
```json
"dt": 0.02    ← Make smaller
```

### "Energy not conserved: relative error = 0.05"
**Solution:** 
1. Check CFL condition
2. Reduce metric amplitude
3. Use finer grid (increase Nx)

### "NaN/Inf detected"
**Solution:**
1. Reduce time step `dt`
2. Reduce metric amplitude
3. Ensure amplitude < 0.8

### Simulation takes too long
**Solution:**
- Reduce `Nx` to 200
- Reduce `T` to 50
- Increase `dt` to 0.08 (but watch CFL!)

### Import errors
**Solution:**
```bash
# Make sure you're in the right directory
cd space-playground

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

---

## Next Steps

### Learn More
- Read `docs/FORMULAE.md` for mathematical details
- Explore `fields/scalar1d.py` source code
- Check `tests/` for validation examples

### Experiment Ideas
1. **Wave packet dispersion:** Use 'wave_packet' initial condition
2. **Moving bubble:** Set `velocity: 0.2` in metric
3. **Multiple reflections:** Set `boundary: "dirichlet"`
4. **Strong field:** Increase `amplitude` to 2.0 (nonlinear regime)

### Contribute
- Found a bug? Open an issue on GitHub
- Improved the code? Submit a pull request
- Have an idea? Start a discussion

---

## Performance Tips

### Fast iteration (for testing)
```json
"Nx": 100,
"T": 20.0,
"save_interval": 50,
"export_animation": false  ← Skip slow animation
```

### Publication quality (for final results)
```json
"Nx": 800,
"T": 150.0,
"dt": 0.02,
"save_interval": 5
```

---

## Command Cheat Sheet

```bash
# Run experiment
python sim/run_case.py experiments/<name>.json

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_scalar1d.py::TestScalarWaveSolver1D::test_energy_conservation_flat_space

# Test with coverage
pytest tests/ --cov=fields --cov=metric

# Quick metric visualization
python metric/gaussian_warp.py

# Quick field solver test
python fields/scalar1d.py
```

---

## Understanding the Physics (30-second version)

1. **Metric = geometry of space**
   - `g_xx > 1`: Space is stretched (waves slow down)
   - `g_xx < 1`: Space is compressed (waves speed up)

2. **Wave equation:** `∂²φ/∂t² = □_g φ`
   - Waves follow curved paths in curved space
   - Energy is conserved (approximately)

3. **What you're seeing:**
   - Wave propagation through variable geometry
   - Phase accumulation in curved regions
   - Reflection/transmission at metric gradients

**This is NOT a real warp drive** — just a numerical playground for understanding field-geometry interactions.

---

## Success Checklist

- [ ] Dependencies installed
- [ ] First experiment runs successfully
- [ ] Results files generated
- [ ] Tests pass (at least 10/12)
- [ ] Custom experiment created
- [ ] Energy conserved to < 5%

**All checked?** You're ready to explore! 🌌

---

**Questions?** Check `README.md` for detailed documentation.

**Stuck?** The code is heavily commented — read the source!

**Excited?** Star the repository and share your results! ⭐