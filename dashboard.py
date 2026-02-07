import matplotlib.pyplot as plt
import data_loader
import data_process

def display_dashboard():
    try:
        # Load and Process [cite: 49]
        config = data_loader.loading_json_data()
        header, raw_data = data_loader.loading_csv_data()
        clean_data = data_process.clean_csv(raw_data)
        
        filtered = data_process.filter_data(clean_data, config)
        result = data_process.perform_operation(filtered, config['operation'])

        # 1. Print Text Results [cite: 51, 52]
        print("--- GDP ANALYSIS DASHBOARD ---")
        print(f"Region: {config['region']} | Year: {config['year']}")
        print(f"Operation: {config['operation'].upper()}")
        print(f"Result: {result:,.2f}")
        print("-------------------------------")

        if not filtered:
            print("No data available for these filters.")
            return

        # 2. Visualizations [cite: 29, 32, 53]
        countries = [row[0] for row in filtered]
        gdps = [float(row[3]) for row in filtered]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Chart 1: Bar Chart [cite: 30]
        ax1.bar(countries[:10], gdps[:10], color='skyblue')
        ax1.set_title(f"Top Countries in {config['region']} ({config['year']})")
        ax1.set_ylabel("GDP Value")
        ax1.tick_params(axis='x', rotation=45)

        # Chart 2: Pie Chart [cite: 30]
        ax2.pie(gdps[:5], labels=countries[:5], autopct='%1.1f%%')
        ax2.set_title("GDP Distribution (Top 5)")

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Dashboard Error: {e}")

if __name__ == "__main__":
    display_dashboard()