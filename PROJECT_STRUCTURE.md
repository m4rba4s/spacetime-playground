# 📁 Project Structure Overview

**spacetime-playground v0.1.0**

---

## 🌳 Directory Tree

```
spacetime-playground/
│
├── 📄 README.md                          # Main project documentation & philosophy
├── 📄 QUICKSTART.md                      # 5-minute getting started guide
├── 📄 STATUS.md                          # Roadmap & development status
├── 📄 LICENSE                            # MIT License with disclaimer
├── 📄 CONTRIBUTING.md                    # Contributor guidelines
├── 📄 RELEASE_CHECKLIST.md               # Pre-release validation checklist
├── 📄 DEPLOYMENT_COMPLETE.md             # Project completion summary
├── 📄 PROJECT_STRUCTURE.md               # This file
├── 📄 ДЛЯ_МЕНЯ.md                        # Russian quick guide for author
│
├── 📄 requirements.txt                   # Python dependencies
├── 📄 .gitignore                         # Git ignore patterns
│
├── 🧪 test_installation.py               # Installation verification script
├── 🧪 test_before_release.py             # Comprehensive pre-release tests
├── 🧪 quick_test.py                      # Fast basic functionality test
├── 📜 test.bat                           # Windows test runner
├── 📜 test.sh                            # Linux/Mac test runner
│
├── 📂 metric/                            # 🌐 Geometric Background Module
│   ├── __init__.py                       # Module exports & version
│   └── gaussian_warp.py                  # Gaussian warp bubble generator
│                                         #   - Static & moving bubbles
│                                         #   - Christoffel symbols
│                                         #   - Metric diagnostics
│                                         #   [450 lines]
│
├── 📂 fields/                            # 🌊 Field Solver Module
│   ├── __init__.py                       # Module exports
│   └── scalar1d.py                       # 1D scalar wave equation solver
│                                         #   - RK4 time integration
│                                         #   - Energy conservation
│                                         #   - Multiple boundary conditions
│                                         #   - Initial condition templates
│                                         #   [509 lines]
│
├── 📂 sim/                               # 🎮 Experiment Orchestration
│   ├── __init__.py                       # Module exports
│   └── run_case.py                       # Experiment orchestrator
│                                         #   - JSON config loading
│                                         #   - Simulation execution
│                                         #   - Visualization generation
│                                         #   - Data export (CSV/PNG/GIF)
│                                         #   [462 lines]
│
├── 📂 experiments/                       # 🧪 Experiment Configurations
│   ├── exp_scalar_warp_static.json       # Example: Static warp bubble
│   └── results/                          # Output directory (git-ignored)
│       └── exp_scalar_warp_static/       # Created on first run
│           ├── summary.png               # Multi-panel visualization
│           ├── animation.gif             # Time evolution movie
│           ├── field_snapshots.csv       # Raw field data
│           ├── energy_history.csv        # Energy vs time
│           └── config.json               # Exact parameters used
│
├── 📂 tests/                             # ✅ Validation & Testing
│   ├── __init__.py                       # Test module
│   └── test_scalar1d.py                  # Comprehensive test suite
│                                         #   - Energy conservation tests
│                                         #   - Convergence validation
│                                         #   - Boundary condition checks
│                                         #   - Metric integration tests
│                                         #   [12 automated tests, 396 lines]
│
├── 📂 docs/                              # 📚 Documentation
│   └── FORMULAE.md                       # Mathematical derivations
│                                         #   - Wave equations on curved space
│                                         #   - Energy conservation proofs
│                                         #   - Numerical discretization
│                                         #   - Stability analysis
│                                         #   [530 lines]
│
└── 📂 viz/                               # 🎨 Visualization (future)
    └── [placeholder for React frontend]
```

---

## 📊 Statistics

| Category | Count | Lines of Code |
|----------|-------|---------------|
| **Core Python Modules** | 3 | ~1,400 |
| **Test Suites** | 3 | ~1,000 |
| **Documentation** | 10 | ~4,000 |
| **Configuration** | 2 | ~50 |
| **Total Files** | 26+ | ~6,500+ |

---

## 🔍 Component Details

### 📦 Core Modules

#### `metric/` - Geometric Backgrounds
**Purpose:** Generate spacetime geometries for field simulations

**Key Components:**
- `GaussianWarp` class — 1D/2D warp bubble generator
- `WarpParameters` dataclass — Configuration storage
- Christoffel symbol computation
- Effective wave speed calculation
- Metric diagnostics and validation

**Public API:**
```python
from metric import create_static_bubble_1d, create_moving_bubble_1d

warp = create_static_bubble_1d(amplitude=0.3, width=15.0)
g_xx, g_inv = warp.metric_1d(x)
```

---

#### `fields/` - Field Solvers
**Purpose:** Solve wave equations on curved backgrounds

**Key Components:**
- `ScalarWaveSolver1D` — Main solver class
- `SimulationParameters` — Simulation configuration
- `ScalarField1D` — Field state container
- Energy conservation monitoring
- Multiple boundary conditions (periodic, Dirichlet, Neumann)

**Public API:**
```python
from fields import ScalarWaveSolver1D, SimulationParameters

params = SimulationParameters(Nx=200, Lx=100.0, T=50.0, dt=0.05)
solver = ScalarWaveSolver1D(params)
results = solver.run()
```

---

#### `sim/` - Experiment Orchestration
**Purpose:** Run complete experiments from configuration files

**Key Components:**
- `ExperimentOrchestrator` — Main orchestrator class
- JSON configuration parser
- Metric setup and field initialization
- Automated visualization generation
- Data export in multiple formats

**Public API:**
```python
from sim import ExperimentOrchestrator

orchestrator = ExperimentOrchestrator("experiments/my_exp.json")
orchestrator.run_full_workflow()
```

---

### 🧪 Testing Infrastructure

#### Test Levels

**1. Quick Test (`quick_test.py`):**
- Basic imports
- Minimal simulation (10 steps)
- Fast validation (~5 seconds)

**2. Installation Test (`test_installation.py`):**
- Dependency verification
- Module import checks
- Short simulation run
- ~30 seconds

**3. Comprehensive Test (`test_before_release.py`):**
- Full validation suite
- Physics accuracy checks
- Documentation verification
- ~2 minutes

**4. Full Test Suite (`tests/test_scalar1d.py`):**
- 12 automated tests
- Numerical convergence
- Energy conservation
- Boundary conditions
- pytest compatible

---

### 📚 Documentation Hierarchy

**Level 1: User-Facing**
- `README.md` — Project overview & philosophy
- `QUICKSTART.md` — Get running in 5 minutes
- `ДЛЯ_МЕНЯ.md` — Author's personal guide (Russian)

**Level 2: Technical**
- `docs/FORMULAE.md` — Mathematical foundations
- `STATUS.md` — Development roadmap
- `PROJECT_STRUCTURE.md` — This file

**Level 3: Contributor**
- `CONTRIBUTING.md` — How to contribute
- `RELEASE_CHECKLIST.md` — Pre-release validation

**Level 4: Code Documentation**
- Inline docstrings (NumPy style)
- Function/class documentation
- Example usage in `__main__` blocks

---

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
           ┌──────────────────────┐
           │  JSON Configuration  │
           │  (experiments/*.json) │
           └──────────┬───────────┘
                      │
                      ▼
           ┌──────────────────────┐
           │ ExperimentOrchestrator│
           │     (sim/run_case)    │
           └──────┬───────┬────────┘
                  │       │
         ┌────────┘       └────────┐
         ▼                          ▼
┌────────────────┐        ┌────────────────┐
│ Metric Generator│        │  Field Solver  │
│(metric/gaussian)│        │(fields/scalar) │
└────────┬───────┘        └────────┬───────┘
         │                          │
         └──────────┬───────────────┘
                    ▼
         ┌──────────────────────┐
         │   Simulation Loop    │
         │  - Time stepping     │
         │  - Energy monitoring │
         │  - Data collection   │
         └──────────┬───────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
         ▼                     ▼
┌─────────────────┐   ┌─────────────────┐
│  Visualization  │   │   Data Export   │
│  - Plots        │   │  - CSV files    │
│  - Animations   │   │  - Metadata     │
└─────────────────┘   └─────────────────┘
```

---

## 🎯 Module Dependencies

```
metric/
  └─ numpy, scipy

fields/
  ├─ numpy, scipy
  └─ metric/ (optional, for curved space)

sim/
  ├─ numpy, matplotlib
  ├─ metric/
  ├─ fields/
  └─ json, pathlib

tests/
  ├─ pytest
  ├─ metric/
  └─ fields/
```

---

## 🚀 Execution Paths

### Path 1: Quick Test
```bash
python quick_test.py
```
**Flow:** Imports → Metric → Field → 10 steps → Success

### Path 2: Full Experiment
```bash
python sim/run_case.py experiments/exp_scalar_warp_static.json
```
**Flow:** Config → Setup → Simulate → Visualize → Export

### Path 3: Automated Testing
```bash
pytest tests/test_scalar1d.py -v
```
**Flow:** 12 tests → Validation → Report

### Path 4: Direct Module Usage
```python
from metric import create_static_bubble_1d
from fields import ScalarWaveSolver1D

# Custom workflow...
```

---

## 📂 File Naming Conventions

- **Modules:** `lowercase_with_underscores.py`
- **Classes:** `PascalCase`
- **Functions:** `snake_case()`
- **Constants:** `UPPER_SNAKE_CASE`
- **Documentation:** `UPPERCASE.md`
- **Configs:** `descriptive_name.json`

---

## 🔐 Git Ignored Items

Via `.gitignore`:
- `__pycache__/` and `*.pyc`
- `experiments/results/` (generated outputs)
- `*.png`, `*.gif` (except docs)
- Virtual environments
- IDE configs
- OS-specific files

---

## 🎨 Color Coding (for reference)

- 🌐 **Metric/Geometry** → Blue
- 🌊 **Fields/Physics** → Cyan
- 🎮 **Simulation** → Green
- 🧪 **Testing** → Yellow
- 📚 **Documentation** → Purple
- 🎨 **Visualization** → Red

---

## 📈 Growth Roadmap (Directory Evolution)

### v0.1.0 (Current)
```
metric/    ✓ 1D Gaussian
fields/    ✓ 1D scalar
sim/       ✓ Orchestrator
tests/     ✓ Basic suite
docs/      ✓ Foundation
```

### v0.2.0 (Planned)
```
metric/    + 2D/3D metrics
fields/    + 2D scalar, FDTD EM
emfield/   + NEW
sim/       + Parameter sweeps
tests/     + EM tests
```

### v0.3.0 (Future)
```
qinfo/     + NEW (quantum info)
fields/    + Spinor fields
viz/       + React frontend
```

---

## 🔗 Cross-References

**README.md** ↔ All files (overview)  
**QUICKSTART.md** → `experiments/`, `sim/`  
**FORMULAE.md** ↔ `metric/`, `fields/`  
**CONTRIBUTING.md** → `tests/`, all modules  
**STATUS.md** → Future structure

---

## 💡 Key Design Principles

1. **Modularity** — Each directory is self-contained
2. **Clarity** — Readable over clever
3. **Testability** — Every module has tests
4. **Documentation** — Everything explained
5. **Extensibility** — Easy to add new features

---

## 🎓 Learning Path Through Structure

**Beginner:**
1. `README.md` → Understand vision
2. `QUICKSTART.md` → Run first experiment
3. `experiments/` → Modify parameters

**Intermediate:**
4. `metric/gaussian_warp.py` → Study implementation
5. `fields/scalar1d.py` → Understand solver
6. `tests/test_scalar1d.py` → See validation

**Advanced:**
7. `docs/FORMULAE.md` → Mathematical details
8. `sim/run_case.py` → Orchestration
9. Create new module → Contribute!

---

## 📞 Where to Find Things

**"How do I...?"**

- **Run a simulation?** → `QUICKSTART.md`
- **Understand the math?** → `docs/FORMULAE.md`
- **Contribute code?** → `CONTRIBUTING.md`
- **Report a bug?** → GitHub Issues
- **Add a new metric?** → `metric/gaussian_warp.py` (template)
- **Change parameters?** → `experiments/*.json`
- **Run tests?** → `quick_test.py` or `pytest`

---

**Version:** 1.0  
**Last Updated:** 2024 v0.1.0  
**Maintained by:** Space-Playground Collective

*"A well-organized project is a joy to explore."* 🌌