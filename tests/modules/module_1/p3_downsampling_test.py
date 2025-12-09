import unittest
import numpy as np

from src.module_1.p3_downsampling import *

class TestGenerate(unittest.TestCase):
    def test_no_error(self):
        config = ConfigParser()
        assignment431(config)
        assignment432(config)