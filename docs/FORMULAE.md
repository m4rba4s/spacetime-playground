# 📐 Mathematical Formulae & Derivations

**Space-Playground Mathematical Foundation**

This document provides detailed mathematical derivations for the physics implemented in Space-Playground. All equations are presented in a pedagogical manner, bridging theoretical foundations with numerical implementation.

---

## Table of Contents

1. [Metric Geometry Basics](#1-metric-geometry-basics)
2. [Scalar Wave Equation on Curved Backgrounds](#2-scalar-wave-equation-on-curved-backgrounds)
3. [Energy Conservation](#3-energy-conservation)
4. [Gaussian Warp Bubble Metrics](#4-gaussian-warp-bubble-metrics)
5. [Numerical Discretization](#5-numerical-discretization)
6. [Stability Analysis](#6-stability-analysis)
7. [References](#references)

---

## 1. Metric Geometry Basics

### 1.1 Spacetime Metric

In general relativity, the geometry of spacetime is described by a metric tensor **g<sub>μν</sub>**. The spacetime interval is:

```
ds² = g_μν dx^μ dx^ν
```

For our (1+1)D simulations, we use:

```
ds² = -dt² + g_xx(x,t) dx²
```

where:
- Time is not deformed (remains Minkowski-like)
- Spatial metric **g<sub>xx</sub>(x,t)** can vary
- Signature is (-,+) following particle physics convention

### 1.2 Inverse Metric

The inverse metric satisfies:

```
g^μν g_νλ = δ^μ_λ
```

For our diagonal metric:

```
g^tt = -1
g^xx = 1/g_xx
```

### 1.3 Metric Determinant

The determinant of the spatial metric:

```
g = det(g_ij) = g_xx  (in 1D)
```

The volume element becomes:

```
dV = √g dx
```

This is crucial for energy integrals and conservation laws.

---

## 2. Scalar Wave Equation on Curved Backgrounds

### 2.1 Covariant Wave Equation

The covariant wave equation for a massless scalar field φ is:

```
□_g φ = 0
```

where **□<sub>g</sub>** is the d'Alembertian operator:

```
□_g φ = (1/√(-g)) ∂_μ(√(-g) g^μν ∂_ν φ)
```

### 2.2 Explicit Form for (1+1)D

For our metric **ds² = -dt² + g<sub>xx</sub> dx²**, this becomes:

```
∂²φ/∂t² = (1/√g_xx) ∂_x(√g_xx g^xx ∂_x φ)
```

Expanding the right side:

```
∂²φ/∂t² = (1/√g_xx) ∂_x(√g_xx · (1/g_xx) · ∂φ/∂x)
```

```
∂²φ/∂t² = (1/√g_xx) ∂_x((1/√g_xx) ∂φ/∂x)
```

This is the **covariant Laplacian** acting on φ.

### 2.3 Conformal Metrics

For a conformally flat metric:

```
g_xx = Ω²(x,t)
```

The wave equation simplifies to:

```
∂²φ/∂t² = (1/Ω²) ∂²φ/∂x² - (2/Ω³)(∂Ω/∂x) ∂φ/∂x
```

**Physical interpretation:**
- First term: Modified wave operator with effective speed **c<sub>eff</sub> = c/Ω**
- Second term: "Geometric force" from spatial metric gradients

### 2.4 Wave Speed in Curved Space

In regions where **Ω > 1** (space is "stretched"):
- Waves propagate **slower** than in flat space
- Wavelength appears **longer**

In regions where **Ω < 1** (space is "compressed"):
- Waves propagate **faster**
- Wavelength appears **shorter**

This is analogous to light propagating through variable refractive index media.

---

## 3. Energy Conservation

### 3.1 Energy-Momentum Tensor

For a scalar field, the energy-momentum tensor is:

```
T_μν = ∂_μ φ ∂_ν φ - (1/2) g_μν g^αβ ∂_α φ ∂_β φ
```

### 3.2 Total Energy

The conserved energy for the scalar field on our background is:

```
E = ∫ T_tt √g dx
```

For our (1+1)D metric:

```
E = ∫ [(∂φ/∂t)² + g^xx (∂φ/∂x)²] √g_xx dx
```

Breaking this down:
- **Kinetic energy density:** (∂φ/∂t)²
- **Gradient energy density:** g^xx (∂φ/∂x)² = (1/g_xx)(∂φ/∂x)²
- **Volume element:** √g_xx dx

### 3.3 Energy Conservation Theorem

For a **static** metric (∂g/∂t = 0), energy is conserved:

```
dE/dt = 0
```

**Proof sketch:**
Using the wave equation and integration by parts:

```
dE/dt = 2∫ [φ_t φ_tt + g^xx φ_x φ_xt] √g dx
```

Substituting φ_tt from the wave equation and applying integration by parts shows this vanishes (with appropriate boundary conditions).

### 3.4 Numerical Energy Conservation

In numerical simulations, we monitor:

```
ΔE/E₀ = |E(t) - E(0)| / E(0)
```

Good simulations should maintain **ΔE/E₀ < 0.01** (1% drift) over long times.

---

## 4. Gaussian Warp Bubble Metrics

### 4.1 Shape Function

We define a localized Gaussian deformation:

```
f(x,t) = A exp(-(x - x₀(t))²/(2σ²))
```

where:
- **A**: Amplitude (dimensionless)
- **σ**: Width of the bubble
- **x₀(t) = x₀ + vt**: Bubble center position

### 4.2 Conformal Factor

The conformal factor is:

```
Ω(x,t) = 1 + f(x,t)
```

And the spatial metric:

```
g_xx(x,t) = Ω²(x,t) = [1 + f(x,t)]²
```

### 4.3 Physical Constraints

For the metric to remain physical:

1. **Positivity:** g_xx > 0 everywhere
   - Requires: **|A| < 1**

2. **Asymptotic flatness:** Ω → 1 as |x| → ∞
   - Guaranteed by Gaussian decay

3. **Smoothness:** Ω should be at least C² (twice differentiable)
   - Gaussian is C^∞

### 4.4 Energy Condition Considerations

In full general relativity, this metric would require:

```
T_μν = (8πG)^(-1) G_μν
```

For our toy metrics, the implied stress-energy would violate energy conditions (requiring "exotic matter"). This is **pedagogical fiction** — we prescribe the metric without claiming physical realizability.

### 4.5 Connection Coefficients (Christoffel Symbols)

For the conformal metric, the non-zero Christoffel symbols are:

```
Γ^x_xx = (∂_x Ω) / Ω = (∂_x g_xx) / (2 g_xx)
```

This describes how "straight lines" (geodesics) curve in this geometry.

### 4.6 2D Extension

For 2D, we use:

```
f(x,y,t) = A exp(-[(x-x₀)² + (y-y₀)²]/(2σ²))
```

With metric:

```
ds² = -dt² + Ω²(x,y) (dx² + dy²)
```

This is a **conformally flat** metric in 2D.

---

## 5. Numerical Discretization

### 5.1 Spatial Grid

Discretize space on a uniform grid:

```
x_i = i·Δx,  i = 0, 1, ..., N-1
Δx = L/N
```

Field values: **φ_i(t) ≈ φ(x_i, t)**

### 5.2 Spatial Derivatives

**First derivative** (centered difference):

```
∂φ/∂x|_i ≈ (φ_{i+1} - φ_{i-1})/(2Δx) + O(Δx²)
```

**Second derivative:**

```
∂²φ/∂x²|_i ≈ (φ_{i+1} - 2φ_i + φ_{i-1})/(Δx²) + O(Δx²)
```

### 5.3 Covariant Laplacian Discretization

For **□<sub>g</sub> φ = (1/√g) ∂<sub>x</sub>(√g g<sup>xx</sup> ∂<sub>x</sub> φ)**:

Define flux at cell interfaces:

```
F_{i+1/2} = √g_{i+1/2} · g^xx_{i+1/2} · (φ_{i+1} - φ_i)/Δx
```

Then:

```
(□_g φ)_i ≈ (F_{i+1/2} - F_{i-1/2}) / (Δx · √g_i)
```

This maintains **conservation properties** in discrete form.

### 5.4 Time Integration: RK4

We use 4th-order Runge-Kutta for time evolution.

State vector: **y = [φ, ∂φ/∂t]**

Time derivative: **dy/dt = [∂φ/∂t, ∂²φ/∂t²]**

RK4 update:

```
k₁ = f(y_n)
k₂ = f(y_n + Δt·k₁/2)
k₃ = f(y_n + Δt·k₂/2)
k₄ = f(y_n + Δt·k₃)

y_{n+1} = y_n + (Δt/6)(k₁ + 2k₂ + 2k₃ + k₄)
```

This is **4th-order accurate** in time: error ~ O(Δt⁴)

### 5.5 CFL Condition

For stability, the Courant-Friedrichs-Lewy condition must be satisfied:

```
CFL = c · Δt / Δx ≤ 1
```

More conservatively:

```
c · Δt / Δx ≤ 0.5
```

In curved space, use the **maximum effective wave speed**:

```
CFL = (c/Ω_min) · Δt / Δx ≤ 1
```

---

## 6. Stability Analysis

### 6.1 Von Neumann Stability

For flat space wave equation, Fourier mode analysis:

```
φ(x,t) = exp(i(kx - ωt))
```

Dispersion relation:

```
ω = ±c|k|
```

For our numerical scheme (RK4 + centered differences), all modes remain bounded if CFL < 1.

### 6.2 Energy Dissipation

Ideal discrete energy:

```
E_discrete = Σ_i [(φ_t,i)² + g^xx_i ((φ_{i+1} - φ_i)/Δx)²] √g_i Δx
```

Properly discretized, this should remain constant (up to round-off error).

### 6.3 Numerical Dispersion

Discrete wave equation has modified dispersion:

```
ω_numerical ≈ ω_exact [1 - (kΔx)²/6 + O(Δx⁴)]
```

This causes:
- **Phase errors** accumulate over time
- High-k modes propagate slower
- Wave packets "spread" (numerical dispersion)

### 6.4 Grid Resolution Guidelines

For accurate wave propagation:

**Minimum points per wavelength:**
```
N_λ = λ/Δx ≥ 10
```

For a wavelength λ, need at least 10 grid points to resolve it accurately.

**Bubble resolution:**
For a Gaussian bubble of width σ:
```
N_bubble = 2σ/Δx ≥ 20
```

---

## 7. Physical Units and Dimensionless Form

### 7.1 Natural Units

We work in units where:
- **c = 1** (speed of light)
- Length scale set by bubble width σ
- Time scale: **T ~ σ/c = σ**

### 7.2 Dimensionless Parameters

All simulations use dimensionless quantities:

- **x̃ = x/σ**: Position in bubble widths
- **t̃ = tc/σ**: Time in light-crossing times
- **Ã = A**: Dimensionless amplitude

### 7.3 Conversion to Physical Units

To relate to real physics (hypothetically):

If σ = 1 meter:
- Grid spacing Δx = 0.25 m (for Nx=400, Lx=100)
- Time step Δt = 0.04 light-meters ≈ 0.13 ns
- Simulation time T = 80 light-meters ≈ 267 ns

**Note:** These are toy models, not claims of physical realizability!

---

## Appendix A: Metric Signature Conventions

We use the **particle physics signature** (-,+,+,+):

```
η_μν = diag(-1, +1, +1, +1)
```

Some texts use (+,-,-,-). Conversion:

```
g_μν^{our} = -g_μν^{GR texts}
```

---

## Appendix B: Key Assumptions & Limitations

1. **Prescribed metric:** We do not solve Einstein's equations
2. **Test field approximation:** φ does not backreact on geometry
3. **Classical fields:** No quantum field theory effects
4. **Weak deformations:** |A| << 1 for numerical stability
5. **Pedagogical intent:** These are exploration tools, not engineering designs

---

## References

### Textbooks
1. **Misner, Thorne, Wheeler** - *Gravitation* (1973)
   - Chapter 21: Variational principle and energy-momentum tensor
2. **Carroll, Sean** - *Spacetime and Geometry* (2004)
   - Chapter 4: Covariant derivatives and geodesics
3. **Alcubierre, Miguel** - *Introduction to 3+1 Numerical Relativity* (2008)
   - Chapter 3: Numerical methods for wave equations

### Papers
1. **Alcubierre, M.** (1994). "The warp drive: hyper-fast travel within general relativity"
   - *Classical and Quantum Gravity*, 11(5), L73
   - Inspiration for warp bubble metrics
2. **Wald, Robert M.** (1984). *General Relativity*
   - Appendix E: Energy conditions and causality

### Numerical Methods
1. **LeVeque, R.J.** (2002). *Finite Volume Methods for Hyperbolic Problems*
   - Chapter 10: Wave propagation algorithms
2. **Butcher, J.C.** (2016). *Numerical Methods for Ordinary Differential Equations*
   - Chapter 3: Runge-Kutta methods

---

## Notation Summary

| Symbol | Meaning |
|--------|---------|
| g<sub>μν</sub> | Metric tensor |
| g<sup>μν</sup> | Inverse metric |
| φ | Scalar field |
| □<sub>g</sub> | Covariant d'Alembertian |
| Ω | Conformal factor |
| σ | Gaussian bubble width |
| A | Bubble amplitude |
| Γ<sup>λ</sup><sub>μν</sub> | Christoffel symbols |
| T<sub>μν</sub> | Energy-momentum tensor |

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Contributors:** Space-Playground Collective

*"Mathematics is the language in which the universe writes its autobiography."*