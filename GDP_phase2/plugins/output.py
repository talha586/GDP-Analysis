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


class GraphicsChartWriter:

    def __init__(self):
        import matplotlib.pyplot as plt
        import matplotlib.ticker as mticker
        self._plt     = plt
        self._mticker = mticker

    def write(self, tag: str, records: List[dict]):
        if not records:
            print(f"No data for '{tag}', skipping chart.")
            return

        dispatch = {
            "top10":                     self._bar_horizontal,
            "bottom10":                  self._bar_horizontal,
            "growth_rate":               self._bar_growth_rate,
            "avg_by_continent":          self._pie_chart,
            "global_gdp_trend":          self._line_trend,
            "fastest_growing_continent": self._bar_continent_growth,
            "consistent_decline":        self._text_table,
            "continent_contribution":    self._donut_chart,
        }

        handler = dispatch.get(tag)
        if handler:
            handler(tag, records)

    def _save_and_close(self, filename: str):
        self._plt.tight_layout()
        self._plt.show()
        self._plt.close()

    def _fmt_billions(self, val: float) -> str:
        if val >= 1e12:
            return f"${val/1e12:.1f}T"
        if val >= 1e9:
            return f"${val/1e9:.1f}B"
        if val >= 1e6:
            return f"${val/1e6:.1f}M"
        return f"${val:.0f}"

    def _bar_horizontal(self, tag: str, records: List[dict]):
        plt       = self._plt
        countries = [r.get("country", "") for r in records]
        gdps      = [r.get("gdp", 0) for r in records]
        year      = records[0].get("year", "")
        title_map = {"top10": f"Top 10 Countries by GDP ({year})",
                     "bottom10": f"Bottom 10 Countries by GDP ({year})"}
        color_map = {"top10": "#2ecc71", "bottom10": "#e74c3c"}

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(countries[::-1], gdps[::-1], color=color_map.get(tag, "#4c72b0"))
        ax.set_xlabel("GDP (current US$)", fontsize=11)
        ax.set_title(title_map.get(tag, tag), fontsize=13, fontweight="bold")
        ax.xaxis.set_major_formatter(self._mticker.FuncFormatter(lambda x, _: self._fmt_billions(x)))
        for bar, val in zip(bars, gdps[::-1]):
            ax.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height()/2,
                    self._fmt_billions(val), va="center", fontsize=8)
        ax.grid(axis="x", linestyle="--", alpha=0.5)
        self._save_and_close(f"{tag}.png")

    def _bar_growth_rate(self, tag: str, records: List[dict]):
        plt       = self._plt
        top       = records[:15]
        countries = [r.get("country", "") for r in top]
        rates     = [r.get("growth_pct", 0) for r in top]
        colors    = ["#2ecc71" if r >= 0 else "#e74c3c" for r in rates]
        s_year    = records[0].get("start_year", "")
        e_year    = records[0].get("end_year", "")

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(countries, rates, color=colors)
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_ylabel("Growth Rate (%)", fontsize=11)
        ax.set_title(f"GDP Growth Rate by Country ({s_year}–{e_year})", fontsize=13, fontweight="bold")
        plt.xticks(rotation=45, ha="right", fontsize=8)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        self._save_and_close(f"{tag}.png")

    def _pie_chart(self, tag: str, records: List[dict]):
        plt    = self._plt
        labels = [r.get("continent", "") for r in records]
        values = [r.get("average_gdp", 0) for r in records]

        fig, ax = plt.subplots(figsize=(8, 8))
        _, _, autotexts = ax.pie(values, labels=labels, autopct="%1.1f%%",
                                 startangle=140, pctdistance=0.82)
        for at in autotexts:
            at.set_fontsize(9)
        ax.set_title("Average GDP by Continent", fontsize=13, fontweight="bold")
        self._save_and_close(f"{tag}.png")

    def _line_trend(self, tag: str, records: List[dict]):
        plt    = self._plt
        years  = [r.get("year", "") for r in records]
        totals = [r.get("total_gdp", 0) for r in records]

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(years, totals, color="#2980b9", linewidth=2.5, marker="o", markersize=4)
        ax.fill_between(range(len(years)), totals, alpha=0.15, color="#2980b9")
        ax.set_xlabel("Year", fontsize=11)
        ax.set_ylabel("Total Global GDP (US$)", fontsize=11)
        ax.set_title("Total Global GDP Trend", fontsize=13, fontweight="bold")
        step = max(1, len(years) // 10)
        ax.set_xticks(range(0, len(years), step))
        ax.set_xticklabels(years[::step], rotation=45, fontsize=8)
        ax.yaxis.set_major_formatter(self._mticker.FuncFormatter(lambda x, _: self._fmt_billions(x)))
        ax.grid(linestyle="--", alpha=0.5)
        self._save_and_close(f"{tag}.png")

    def _bar_continent_growth(self, tag: str, records: List[dict]):
        plt        = self._plt
        continents = [r.get("continent", "") for r in records]
        rates      = [r.get("growth_pct", 0) for r in records]
        colors     = ["#f39c12" if i == 0 else "#bdc3c7" for i in range(len(records))]

        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(continents, rates, color=colors)
        ax.set_ylabel("GDP Growth (%)", fontsize=11)
        ax.set_title("GDP Growth Rate by Continent", fontsize=13, fontweight="bold")
        for bar, val in zip(bars, rates):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f"{val:.1f}%", ha="center", fontsize=9)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        plt.xticks(rotation=30, ha="right")
        self._save_and_close(f"{tag}.png")

    def _text_table(self, tag: str, records: List[dict]):
        plt = self._plt
        fig, ax = plt.subplots(figsize=(8, max(3, len(records) * 0.4 + 1)))
        ax.axis("off")

        if not records:
            ax.text(0.5, 0.5, "No countries with consistent GDP decline found.",
                    ha="center", va="center", fontsize=12)
        else:
            col_labels = ["Country", "Continent", "Years of Decline", "Up To Year"]
            table_data = [[r.get("country",""), r.get("continent",""),
                           str(r.get("years","")), str(r.get("end_year",""))]
                          for r in records]
            table = ax.table(cellText=table_data, colLabels=col_labels,
                             loc="center", cellLoc="left")
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1.2, 1.4)

        ax.set_title("Countries with Consistent GDP Decline", fontsize=12, fontweight="bold", pad=10)
        self._save_and_close(f"{tag}.png")

    def _donut_chart(self, tag: str, records: List[dict]):
        plt    = self._plt
        labels = [r.get("continent", "") for r in records]
        values = [r.get("contribution_pct", 0) for r in records]

        fig, ax = plt.subplots(figsize=(8, 8))
        _, _, autotexts = ax.pie(values, labels=labels, autopct="%1.1f%%",
                                 startangle=140, pctdistance=0.82,
                                 wedgeprops={"width": 0.5})
        for at in autotexts:
            at.set_fontsize(9)
        ax.set_title("Continent Contribution to Global GDP (%)", fontsize=13, fontweight="bold")
        self._save_and_close(f"{tag}.png")