import unittest
import numpy as np

from src.module_1.p2_lp_filtering import *

class TestGenerate(unittest.TestCase):
    """
    @meta
    """
    def test_no_error(self):
        """
        @meta
        """
        config = ConfigParser()
        assignment422(config)
        assignment423(config)
