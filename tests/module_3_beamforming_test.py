import unittest
import sys
import os
import importlib.util
from pathlib import Path

# Load beamforming.py directly from the project src/module 3 folder to avoid import resolution issues
bf_path = Path(__file__).resolve().parent.parent / 'src' / 'module_3' / 'beamforming.py'
spec = importlib.util.spec_from_file_location("beamforming", str(bf_path))
beamforming = importlib.util.module_from_spec(spec)
spec.loader.exec_module(beamforming)
a_lin = beamforming.a_lin

class TestBeamforming(unittest.TestCase):
    def setUp(self):
        return super().setUp()