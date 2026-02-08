import matplotlib.pyplot as plt

def Plot_Bar_Chart(header_text, data_rows, target_year):
    try:
        year_index = header_text.index(str(target_year))
    except ValueError:
        print(f"Year {target_year} not found in data header.")
        return

    sorted_rows = sorted(data_rows, key=lambda x: float(x[year_index]), reverse=True)
    
    top_rows = sorted_rows[:10]
    
    countries = [row[0] for row in top_rows]
    gdps = [float(row[year_index]) for row in top_rows]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(countries, gdps, color='#4c72b0')
    
    plt.xlabel('Country', fontsize=12)
    plt.ylabel(f'GDP (US$) in {target_year}', fontsize=12)
    plt.title(f'Top 10 GDPs by Country in {target_year}', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.ticklabel_format(style='plain', axis='y')
    plt.tight_layout()
    plt.show()

def Plot_Line_Chart(header_text, data_rows, start_year="1960", end_year="2020"):

    try:
        start_idx = header_text.index(str(start_year))
        end_idx = header_text.index(str(end_year))
    except ValueError:
        print("Year range not found in header.")
        return

    years = header_text[start_idx:end_idx+1]

    sorted_rows = sorted(data_rows, key=lambda x: float(x[end_idx]), reverse=True)
    
    top_rows = sorted_rows[:5]

    plt.figure(figsize=(12, 6))

    for row in top_rows:
        country_name = row[0]
        gdp_values = [float(val) for val in row[start_idx:end_idx+1]]
        plt.plot(years, gdp_values, label=country_name, linewidth=2)

    plt.xlabel('Year', fontsize=12)
    plt.ylabel('GDP (US$)', fontsize=12)
    plt.title(f'GDP Growth Trend ({start_year}-{end_year}) - Top 5 Countries', fontsize=14)
    
    plt.xticks(years[::5], rotation=45)
    plt.ticklabel_format(style='plain', axis='y')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()