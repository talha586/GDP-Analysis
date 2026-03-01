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

    def write(self, tag: str, records: List[dict]):
        title = self._TITLES.get(tag, tag.upper())
        sep   = "=" * 70
        print(f"\n{sep}")
        print(f"  {title}")
        print(sep)

        if not records:
            print("  (no data)")
            return

        keys  = list(records[0].keys())
        col_w = max(18, max(len(str(k)) for k in keys) + 2)

        header = "".join(f"{str(k):<{col_w}}" for k in keys)
        print(f"  {header}")
        print(f"  {'-' * len(header)}")

        for rec in records:
            def fmt(v):
                if isinstance(v, float):
                    return f"{v:,.2f}"
                return str(v)
            row = "".join(f"{fmt(rec.get(k, '')):<{col_w}}" for k in keys)
            print(f"  {row}")
