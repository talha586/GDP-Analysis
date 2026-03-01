from typing import List
import sys


class ConsoleWriter:

    _TITLES = {
        "top10":                     "Top 10 Countries by GDP",
        "bottom10":                  "Bottom 10 Countries by GDP",
        "growth_rate":               "GDP Growth Rate by Country",
        "avg_by_continent":          "Average GDP by Continent",
        "global_gdp_trend":          "Total Global GDP Trend",
        "fastest_growing_continent": "Fastest Growing Continent",
        "consistent_decline":        "Countries with Consistent GDP Decline",
        "continent_contribution":    "Continent Contribution to Global GDP (%)",
    }
