import argparse
import pandas as pd

def vertical_stack_tsv(tsv1_path, tsv2_path, output_path):
    try:
        # Load the first TSV file, treating it as key-value pairs
        df1 = pd.read_csv(tsv1_path, sep="\t", header=None, names=["Metric", "Value"])
        # Load the second TSV file in the same format
        df2 = pd.read_csv(tsv2_path, sep="\t", header=None, names=["Metric", "Value"])
        
        # Concatenate them vertically (stack rows) and reset the index
        combined_df = pd.concat([df1, df2], axis=0, ignore_index=True)
        
        # Save the combined DataFrame to a new TSV file without headers
        combined_df.to_csv(output_path, sep="\t", index=False, header=False)
        print(f"Vertically stacked TSV saved to {output_path}")
    
    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}. Please check the file paths.")
    except pd.errors.EmptyDataError:
        print("Error: One or both of the files are empty.")
    except ValueError as ve:
        print(f"Error: {ve}. Ensure the data structure is consistent.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vertically stack two TSV files by appending rows of the second file below the first.")
    parser.add_argument("tsv1", type=str, help="Path to the first TSV file.")
    parser.add_argument("tsv2", type=str, help="Path to the second TSV file.")
    parser.add_argument("output", type=str, help="Path to save the stacked TSV file.")
    
    args = parser.parse_args()
    
    vertical_stack_tsv(args.tsv1, args.tsv2, args.output)
