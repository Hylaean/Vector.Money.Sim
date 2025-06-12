"""Data loading and normalisation utilities."""

from .io import read_inventory, read_io_table
from .normalise import normalise_per_capita

__all__ = ["read_io_table", "read_inventory", "normalise_per_capita"]
