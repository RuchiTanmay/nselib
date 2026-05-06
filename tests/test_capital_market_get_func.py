import unittest
from unittest.mock import Mock, patch

from nselib.capital_market.get_func import get_index_data
from nselib.constants import index_data_columns


class TestGetIndexData(unittest.TestCase):
    def test_get_index_data_drops_hi_timestamp_when_present(self):
        response = Mock()
        response.json.return_value = {
            "data": [
                {
                    "CH_INDEX_NAME": "NIFTY 50",
                    "OPEN": 25000.0,
                    "HIGH": 25100.0,
                    "CLOSE": 25075.0,
                    "LOW": 24950.0,
                    "TURNOVER": 12345.0,
                    "VOLUME": 67890,
                    "TIMESTAMP": "06-May-2026",
                    "HI_TIMESTAMP": "2026-05-06T00:00:00",
                }
            ]
        }

        with patch("nselib.capital_market.get_func.nse_urlfetch", return_value=response):
            data_df = get_index_data("NIFTY 50", "30-04-2026", "06-05-2026")

        self.assertEqual(list(data_df.columns), index_data_columns)
        self.assertNotIn("HI_TIMESTAMP", data_df.columns)

    def test_get_index_data_accepts_response_without_hi_timestamp(self):
        response = Mock()
        response.json.return_value = {
            "data": [
                {
                    "CH_INDEX_NAME": "NIFTY 50",
                    "OPEN": 25000.0,
                    "HIGH": 25100.0,
                    "CLOSE": 25075.0,
                    "LOW": 24950.0,
                    "TURNOVER": 12345.0,
                    "VOLUME": 67890,
                    "TIMESTAMP": "06-May-2026",
                }
            ]
        }

        with patch("nselib.capital_market.get_func.nse_urlfetch", return_value=response):
            data_df = get_index_data("NIFTY 50", "30-04-2026", "06-05-2026")

        self.assertEqual(list(data_df.columns), index_data_columns)
        self.assertEqual(data_df.loc[0, "INDEX_NAME"], "NIFTY 50")


if __name__ == "__main__":
    unittest.main()
