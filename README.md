# 🪐 Space-Playground  
_A digital laboratory for exploring geometry, fields, and information._

---

## 🌌 Preface — Manifest

This project was born out of two things: **fatigue and curiosity**.  
Fatigue — because humanity keeps running in loops of fear, power, and noise.  
Curiosity — because somewhere inside us the question still burns:  
**how is the space that holds us built?**

We are not building a real warp engine, and we promise no miracles.  
We are building an **environment for observation** — a playground for hypotheses where you can touch mathematics, watch fields distort geometry, and see how information survives deformation.  
This project is about **understanding**, not escape.

We don't stand against science; we extend it — openly, experimentally, collectively.  
Code here is not just a tool but a **language of dialogue with nature**.  
Every simulation is a question whispered into the universe, and every visualization is a partial answer — shimmering, imperfect, but honest.

There are no heroes here, only participants: engineers, artists, researchers, skeptics.  
Together we build a **bridge between computation and wonder** — between precise numbers and the quiet feeling that something vast hides behind them.

If, through these lines, someone again finds the urge to look deep into matter not for profit but for truth — then the project worked.

---

## 🧩 About

**Space-Playground** is an open scientific playground for:
- simulating local geometric deformations (toy *warp-bubbles*);
- studying scalar and electromagnetic fields on dynamic metrics;
- experimenting with toy quantum information encoders;
- visualizing the interactions between information, energy, and geometry.

It is written in **Python** and designed to be accessible to scientists, students, and curious minds alike.

---

## ⚙️ Architecture Overview

```
space-playground/
├── metric/         → metric generators (1D/2D warp profiles)
├── fields/         → scalar field solvers on variable geometry
├── emfield/        → electromagnetic field (FDTD) module [planned]
├── qinfo/          → information encoding & compression [planned]
├── sim/            → experiment orchestrators, sweeps
├── viz/            → visualization interface [planned]
├── experiments/    → configs and result archives
├── tests/          → automated numerical verification
└── docs/           → formulas, theory notes, ethics statement
```

---

## 🧠 Core Modules (Current Status)

### ✅ `metric/`
Generates background metrics — static or moving Gaussian "bubbles" that shape how space behaves for other modules.

**Implemented:**
- 1D Gaussian warp bubbles (static and moving)
- 2D conformal metrics
- Christoffel symbol computation
- Effective wave speed calculations

### ✅ `fields/`
Solves wave equations for scalar fields within those geometries.  
Demonstrates stability, energy conservation, and information preservation.

**Implemented:**
- 1D scalar wave equation solver on curved backgrounds
- RK4 time integration with energy monitoring
- Multiple boundary conditions (periodic, Dirichlet, Neumann)
- Energy conservation tracking

### 🚧 `emfield/` [Planned]
Implements 2D Maxwell equations (FDTD).  
Lets you see how electromagnetic fields *paint* geometry — how variable permittivity and permeability affect energy flow and focus.

### 🚧 `qinfo/` [Planned]
Encodes classical data in redundancy or simple tensor structures to study how information behaves under deformation.  
Optional quantum libraries (e.g., `quimb`) may be used for extended experiments.

---

## 🚀 Getting Started

### Requirements
- **Python 3.10+**  
- Standard scientific stack: `numpy`, `scipy`, `matplotlib`
- Optional: `numba` for performance, `pytest` for testing

### Quick Install

```bash
# Clone repository
git clone https://github.com/<yourname>/space-playground.git
cd space-playground

# Install dependencies
pip install -r requirements.txt
```

### Run Your First Simulation

```bash
# Run the static warp bubble experiment
python sim/run_case.py experiments/exp_scalar_warp_static.json
```

This will:
1. Create a static Gaussian warp bubble at x=50
2. Launch a Gaussian wave pulse from x=20
3. Simulate wave propagation through curved space
4. Generate visualizations and export data to `experiments/results/`

### Expected Output

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
  ...
✓ Simulation complete

Generating plots...
  ✓ Saved summary plot: experiments/results/.../summary.png
Generating animation...
  ✓ Saved animation: experiments/results/.../animation.gif
Exporting data...
  ✓ Saved field data: experiments/results/.../field_snapshots.csv
  ✓ Saved energy data: experiments/results/.../energy_history.csv
```

---

## 🧪 Example Experiments

### Experiment 1: Static Warp Bubble
**File:** `experiments/exp_scalar_warp_static.json`

Observe how a wave pulse interacts with a localized metric deformation:
- Wave slows down inside the bubble (where space is "stretched")
- Partial reflection at the bubble boundary
- Energy redistribution but conservation
- Phase shifts accumulate through curved region

### Create Your Own Experiment

Create a new JSON configuration file:

```json
{
    "name": "my_experiment",
    "description": "Your custom experiment description",
    "type": "scalar_1d",
    "metric": {
        "type": "gaussian_warp",
        "amplitude": 0.2,
        "width": 10.0,
        "center": 50.0,
        "velocity": 0.0
    },
    "simulation": {
        "Nx": 200,
        "Lx": 100.0,
        "T": 50.0,
        "dt": 0.05,
        "c": 1.0,
        "boundary": "periodic"
    },
    "initial_conditions": {
        "type": "gaussian_pulse",
        "center": 20.0,
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
```

Run it:
```bash
python sim/run_case.py experiments/my_experiment.json
```

---

## 🔬 Mathematical Foundation (Brief)

We use simplified forms of:

### Scalar Wave Equation on Curved Background
For a metric with spatial component g_xx(x), the wave equation becomes:

```
∂²φ/∂t² = c² □_g φ
```

where □_g is the covariant Laplacian:

```
□_g φ = (1/√g) ∂_x(√g g^xx ∂_x φ)
```

### Energy Conservation
The conserved energy is:

```
E = ∫ [φ_t² + c² g^xx (∂φ/∂x)²] √g dx
```

The metric is **prescribed**, not solved from Einstein equations.  
No claims of physical warp or exotic matter are made — this is **a numerical analogy**, not propulsion physics.

**See `docs/FORMULAE.md` for detailed derivations.**

---

## 📊 Understanding the Output

Each experiment produces:

1. **summary.png** - Multi-panel visualization showing:
   - Field evolution over time
   - Spatial metric profile
   - Energy conservation plot
   - Spacetime diagram

2. **animation.gif** - Time evolution of the field with live energy monitoring

3. **field_snapshots.csv** - Raw field data at saved time points

4. **energy_history.csv** - Total energy vs. time for validation

5. **config.json** - Complete experiment parameters for reproducibility

---

## 🧪 Running Tests

Validate the numerical accuracy:

```bash
# Run all tests
pytest tests/test_scalar1d.py -v

# Run specific test
pytest tests/test_scalar1d.py::TestScalarWaveSolver1D::test_energy_conservation_flat_space -v
```

Tests verify:
- Energy conservation (< 1% drift)
- Convergence under grid refinement
- Boundary condition correctness
- Metric integration accuracy
- Numerical stability

---

## 📚 Documentation

- **`docs/FORMULAE.md`** — Simplified derivations and assumptions [planned]
- **`docs/ETHICS.md`** — Statement of limitations and intent [planned]
- **`docs/TUTORIALS.md`** — Step-by-step guides to create new experiments [planned]

---

## 🛠️ Development Roadmap

### Phase 1: Core Physics ✅ (Current)
- [x] 1D scalar wave solver
- [x] Gaussian warp metrics
- [x] Energy conservation monitoring
- [x] Experiment orchestrator
- [x] Numerical validation tests

### Phase 2: Extended Field Theory 🚧 (Next)
- [ ] 2D scalar wave solver
- [ ] FDTD electromagnetic solver
- [ ] Variable permittivity/permeability
- [ ] Multi-field interactions

### Phase 3: Information Theory 🔮 (Future)
- [ ] Classical information encoding
- [ ] Fidelity measures under deformation
- [ ] Simple quantum state evolution
- [ ] Entanglement in curved space

### Phase 4: Interactive Visualization 🔮 (Future)
- [ ] React web interface
- [ ] Real-time parameter control
- [ ] 3D visualization with WebGL
- [ ] Collaborative experiments

---

## 🤝 Contributing

Pull requests and discussions are welcome!

We encourage additions in:
- **Numerical methods** - Better integrators, adaptive grids
- **Physical systems** - New field types, metric profiles
- **Visualization** - Better plots, interactive tools
- **Documentation** - Tutorials, explanations, examples

**Guidelines:**
- Keep code clear and well-documented
- Add tests for new numerical methods
- Maintain physical accuracy over performance (initially)
- Update documentation with your changes

---

## 🪞 Philosophy

This repository exists to remind us that knowledge is a collective act.  
We don't compete with nature; we collaborate with it.  
Every dataset, every simulation, every insight is a conversation — between human curiosity and the deep structure of reality.

> *"We are not separate minds scattered through space — we are one species, learning to think together."*

---

## 🧾 License

Open-source under **MIT License**.  
Use freely, cite fairly, and share improvements.

---

## 🪐 Contact & Community

**Project initiated by the 0utspoken & metal gear** and collaborators — engineers, physicists, and artists who believe that the best kind of science is the one anyone can touch.

- **GitHub Issues:** Bug reports and feature requests
- **Discussions:** Ideas, questions, and collaborations
- **Pull Requests:** Code contributions welcome

> **Space-Playground** is a laboratory for those who dream in equations.  
> Where computation meets wonder. 🌌

---

## 🔗 Quick Links

- [Getting Started](#-getting-started)
- [Example Experiments](#-example-experiments)
- [Running Tests](#-running-tests)
- [Contributing](#-contributing)

---

**Star ⭐ this repository if you believe science should be beautiful, accessible, and collaborative.**