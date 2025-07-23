import pandas as pd

def calculate_crop_ranges(data_file):
    """
    Calculate and display optimal ranges for each crop from the dataset.
    """
    # Load the data
    df = pd.read_csv(data_file)
    
    # Select the features we want to analyze
    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    # Group by crop and calculate statistics
    crop_stats = df.groupby('label')[features].agg(['min', 'max', 'mean'])
    
    # Display results for each crop
    for crop in crop_stats.index:
        print(f"\nOptimal ranges for {crop}:")
        for feature in features:
            stats = crop_stats.loc[crop, feature]
            print(f"{feature}: {stats['min']:.1f}-{stats['max']:.1f} (mean: {stats['mean']:.1f})")
    
    return crop_stats

# Example usage
if __name__ == "__main__":
    # Replace with your actual file path
    data_file = "Crop_recommendationV2.csv"
    
    print("Calculating optimal crop ranges...")
    crop_ranges = calculate_crop_ranges(data_file)
    
    # Optional: Save results to CSV
    crop_ranges.to_csv("crop_ranges_summary.csv")
    print("\nResults saved to 'crop_ranges_summary.csv'")
