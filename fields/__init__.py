"""
Fields Module - Wave Equation Solvers on Curved Backgrounds

This module contains solvers for various field equations on variable
geometric backgrounds:

- scalar1d: 1D scalar wave equation solver
- scalar2d: 2D scalar wave equation solver (planned)

Author: Space-Playground Collective
License: MIT
"""

from .scalar1d import (
    ScalarField1D,
    ScalarWaveSolver1D,
    SimulationParameters,
    gaussian_pulse,
    sine_wave,
    wave_packet,
)

__version__ = "0.1.0"

__all__ = [
    "ScalarField1D",
    "ScalarWaveSolver1D",
    "SimulationParameters",
    "gaussian_pulse",
    "sine_wave",
    "wave_packet",
]
