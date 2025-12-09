import unittest
import numpy as np

from src.module_1.p2_lp_filtering import *

class TestGenerate(unittest.TestCase):
    def test_no_error(self):
        config = ConfigParser()
        assignment422(config)
        assignment423(config)