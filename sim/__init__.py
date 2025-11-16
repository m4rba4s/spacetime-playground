"""
Simulation Orchestration Module

This module provides experiment orchestrators for running, visualizing,
and exporting Space-Playground simulations.

Main components:
- ExperimentOrchestrator: Runs experiments from JSON configurations
- Result exporters: CSV, plots, animations
- Batch execution utilities

Usage:
    from sim import ExperimentOrchestrator

    orchestrator = ExperimentOrchestrator("experiments/my_exp.json")
    orchestrator.run_full_workflow()
"""

from .run_case import ExperimentOrchestrator

__all__ = ["ExperimentOrchestrator"]
__version__ = "0.1.0"
