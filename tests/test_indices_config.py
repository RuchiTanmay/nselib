import unittest

from nselib import indices
from nselib.indices import nse_config


class TestIndicesConfig(unittest.TestCase):
    def test_broad_market_index_list_uses_nse_midcap_150_name(self):
        broad_market_indices = indices.index_list("BroadMarketIndices")

        self.assertIn("Nifty Midcap 150", broad_market_indices)
        self.assertNotIn("Nifty Midcap150", broad_market_indices)

    def test_midcap_150_config_urls_match_public_index_name(self):
        broad_market_config = nse_config.NiftyBroadMarketIndices

        self.assertIn("Nifty Midcap 150", broad_market_config.index_constituent_list_urls)
        self.assertIn("Nifty Midcap 150", broad_market_config.index_factsheet_urls)


if __name__ == "__main__":
    unittest.main()
