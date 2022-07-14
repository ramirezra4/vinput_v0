import unittest
import Platter
import pandas as pd

class SQLTestCase(unittest.TestCase):
    def setUp(self):
        self.platter = Platter('1GYS4HKJXHR376823', 'Month36')

    def test_hit_cula(self):
        match_vin = {'VIN': ['1GYS4HKJXHR376823'], 'Term: Month36': ['22650']}
        match_vin_df = pd.DataFrame(match_vin)
        self.assertEquals(self.platter.hit_cula(), match_vin_df)
