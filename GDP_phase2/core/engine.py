from typing import List, Any
from core.contracts import DataSink


def _to_float(val):
    try:
        v = float(val)
        return 0.0 if v != v else v
    except (TypeError, ValueError):
        return 0.0


class TransformationEngine:

    def __init__(self, sink: DataSink, config: dict):
        self.sink = sink
        self.config = config

    def execute(self, raw_data: List[Any]):
        continent     = self.config.get("continent", "Asia")
        start_year    = str(self.config.get("start_year", 1990))
        end_year      = str(self.config.get("end_year", 2020))
        decline_years = int(self.config.get("decline_years", 5))

        cleaned = self._clean(raw_data)

        all_years   = [str(y) for y in range(1960, 2025)]
        range_years = [y for y in all_years if int(start_year) <= int(y) <= int(end_year)]

        continent_rows = list(filter(
            lambda r: str(r.get("Continent", "")).strip() == continent,
            cleaned
        ))

        self.sink.write("top10",                    self._top_n_by_gdp(continent_rows, end_year, 10))
        self.sink.write("bottom10",                 self._bottom_n_by_gdp(continent_rows, end_year, 10))
        self.sink.write("growth_rate",              self._gdp_growth_rate(continent_rows, start_year, end_year))
        self.sink.write("avg_by_continent",         self._avg_gdp_by_continent(cleaned, range_years))
        self.sink.write("global_gdp_trend",         self._global_gdp_trend(cleaned, range_years))
        self.sink.write("fastest_growing_continent",self._fastest_growing_continent(cleaned, start_year, end_year))
        self.sink.write("consistent_decline",       self._consistent_decline(continent_rows, end_year, decline_years))
        self.sink.write("continent_contribution",   self._continent_contribution(cleaned, range_years))

    def _clean(self, raw_data):
        year_keys = [str(y) for y in range(1960, 2025)]

        def clean_row(row):
            cleaned = dict(row)
            for k in year_keys:
                if k in cleaned:
                    cleaned[k] = _to_float(cleaned[k])
            return cleaned

        return list(map(clean_row, raw_data))

    def _top_n_by_gdp(self, rows, year, n, ascending=False):
        valid = [r for r in rows if _to_float(r.get(str(year), 0)) > 0]
        sorted_rows = sorted(valid, key=lambda r: _to_float(r.get(str(year), 0)), reverse=not ascending)
        return [{"country": r["Country Name"], "continent": r.get("Continent", ""),
                 "gdp": _to_float(r.get(str(year), 0)), "year": year}
                for r in sorted_rows[:n]]

    def _bottom_n_by_gdp(self, rows, year, n):
        return self._top_n_by_gdp(rows, year, n, ascending=True)

    def _gdp_growth_rate(self, rows, start_year, end_year):
        def growth(r):
            g_start = _to_float(r.get(start_year, 0))
            g_end   = _to_float(r.get(end_year, 0))
            rate    = ((g_end - g_start) / g_start * 100) if g_start > 0 else 0.0
            return {
                "country":    r["Country Name"],
                "continent":  r.get("Continent", ""),
                "start_gdp":  g_start,
                "end_gdp":    g_end,
                "growth_pct": round(rate, 2),
                "start_year": start_year,
                "end_year":   end_year,
            }

        results = list(map(growth, rows))
        return sorted(results, key=lambda x: x["growth_pct"], reverse=True)

    def _avg_gdp_by_continent(self, rows, years):
        continents = list({r.get("Continent", "") for r in rows})

        def continent_avg(cont):
            cont_rows = [r for r in rows if r.get("Continent", "") == cont]
            all_vals  = [_to_float(r.get(y, 0)) for r in cont_rows for y in years if _to_float(r.get(y, 0)) > 0]
            avg       = sum(all_vals) / len(all_vals) if all_vals else 0.0
            return {"continent": cont, "average_gdp": round(avg, 2)}

        return sorted(list(map(continent_avg, continents)), key=lambda x: x["average_gdp"], reverse=True)

    def _global_gdp_trend(self, rows, years):
        def year_total(year):
            total = sum(_to_float(r.get(year, 0)) for r in rows)
            return {"year": year, "total_gdp": round(total, 2)}

        return list(map(year_total, years))

    def _fastest_growing_continent(self, rows, start_year, end_year):
        continents = list({r.get("Continent", "") for r in rows})

        def continent_growth():
            c_rows  = [r for r in rows if r.get("Continent", "") == cont]
            s_total = sum(_to_float(r.get(start_year, 0)) for r in c_rows)
            e_total = sum(_to_float(r.get(end_year, 0)) for r in c_rows)
            rate    = ((e_total - s_total) / s_total * 100) if s_total > 0 else 0.0
            return {"continent": cont, "growth_pct": round(rate, 2),
                    "start_gdp": round(s_total, 2), "end_gdp": round(e_total, 2)}

        return sorted(list(map(continent_growth, continents)), key=lambda x: x["growth_pct"], reverse=True)

    def _consistent_decline(self, rows, end_year, n_years):
        end_int   = int(end_year)
        check_yrs = [str(y) for y in range(end_int - n_years, end_int + 1)]

        def has_decline(r):
            vals  = [_to_float(r.get(y, 0)) for y in check_yrs]
            valid = [(vals[i], vals[i+1]) for i in range(len(vals)-1) if vals[i] > 0 and vals[i+1] > 0]
            return bool(valid) and all(b < a for a, b in valid)

        declining = list(filter(has_decline, rows))
        return [{"country": r["Country Name"], "continent": r.get("Continent", ""),
                 "years": n_years, "end_year": end_year}
                for r in declining]

    def _continent_contribution(self, rows, years):
        continents   = list({r.get("Continent", "") for r in rows})
        global_total = sum(_to_float(r.get(y, 0)) for r in rows for y in years)

        def contribution(cont):
            c_total = sum(_to_float(r.get(y, 0)) for r in rows if r.get("Continent", "") == cont for y in years)
            pct     = (c_total / global_total * 100) if global_total > 0 else 0.0
            return {"continent": cont, "total_gdp": round(c_total, 2), "contribution_pct": round(pct, 4)}

        return sorted(list(map(contribution, continents)), key=lambda x: x["contribution_pct"], reverse=True)
