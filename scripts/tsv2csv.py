import pandas as pd
import argparse

def convert_tsv_to_csv(tsv_path, csv_path):
    """
    Converts a TSV file to a CSV file.
    Args:
        tsv_path (str): Path to the input TSV file.
        csv_path (str): Path to the output CSV file.
    """
    try:
        # Read the TSV file
        df = pd.read_csv(tsv_path, sep="\t")
        # Save the DataFrame as a CSV file
        df.to_csv(csv_path, index=False)
        print(f"File converted from TSV to CSV and saved as {csv_path}")
    except FileNotFoundError:
        print(f"Error: File not found at {tsv_path}. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert a TSV file to a CSV file.")
    parser.add_argument("tsv", type=str, help="Path to the input TSV file.")
    parser.add_argument("csv", type=str, help="Path to the output CSV file.")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Convert the TSV to CSV
    convert_tsv_to_csv(args.tsv, args.csv)
