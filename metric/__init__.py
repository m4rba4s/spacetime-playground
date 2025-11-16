"""
Metric Generation Module

This module provides tools for generating geometric backgrounds (metrics)
for field simulations in Space-Playground.

Available Metrics:
    - Gaussian warp bubbles (1D/2D, static/moving)
    - Conformal deformations
    - Custom metric profiles

Main Classes:
    GaussianWarp: Generator for Gaussian warp bubble metrics
    WarpParameters: Configuration dataclass for warp parameters

Convenience Functions:
    create_static_bubble_1d: Quick 1D static bubble
    create_moving_bubble_1d: Quick 1D moving bubble
    create_static_bubble_2d: Quick 2D static bubble

Example:
    >>> from metric import create_static_bubble_1d
    >>> import numpy as np
    >>>
    >>> warp = create_static_bubble_1d(amplitude=0.3, width=15.0)
    >>> x = np.linspace(-50, 50, 200)
    >>> g_xx, g_inv = warp.metric_1d(x)

Author: Space-Playground Collective
License: MIT
"""

from .gaussian_warp import (
    GaussianWarp,
    WarpParameters,
    compute_metric_diagnostics,
    create_moving_bubble_1d,
    create_static_bubble_1d,
    create_static_bubble_2d,
)

__all__ = [
    "GaussianWarp",
    "WarpParameters",
    "create_static_bubble_1d",
    "create_moving_bubble_1d",
    "create_static_bubble_2d",
    "compute_metric_diagnostics",
]

__version__ = "0.1.0"
