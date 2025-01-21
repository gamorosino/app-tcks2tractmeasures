import argparse
import pandas as pd

def vertical_stack_tsv(tsv1_path, tsv2_path, output_path):
    # Load the two TSV files
    df1 = pd.read_csv(tsv1_path, sep="\t")
    df2 = pd.read_csv(tsv2_path, sep="\t")
    
    # Concatenate them vertically (stack rows)
    combined_df = pd.concat([df1, df2], axis=0)
    
    # Save the combined DataFrame to a new TSV file
    combined_df.to_csv(output_path, sep="\t", index=False)
    print(f"Vertically stacked TSV saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vertically stack two TSV files by appending rows of the second file below the first.")
    parser.add_argument("tsv1", type=str, help="Path to the first TSV file.")
    parser.add_argument("tsv2", type=str, help="Path to the second TSV file.")
    parser.add_argument("output", type=str, help="Path to save the stacked TSV file.")
    
    args = parser.parse_args()
    
    try:
        vertical_stack_tsv(args.tsv1, args.tsv2, args.output)
    except Exception as e:
        print(f"Error: {e}")
