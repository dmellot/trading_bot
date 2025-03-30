import unittest
from utils.api_utils import fetch_real_time_data

class TestApiUtils(unittest.TestCase):
    def test_fetch_real_time_data(self):
        """Vérifie que fetch_real_time_data retourne un DataFrame non vide."""
        df = fetch_real_time_data('BTC/USD', timeframe='1d', limit=10)
        self.assertFalse(df.empty, "Le DataFrame retourné est vide.")

    def test_invalid_symbol(self):
        """Vérifie que fetch_real_time_data gère les symboles invalides."""
        with self.assertRaises(Exception):
            fetch_real_time_data('INVALID/USD', timeframe='1d', limit=10)

if __name__ == '__main__':
    unittest.main()