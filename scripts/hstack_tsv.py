import argparse
import pandas as pd

def horizontal_stack_tsv(tsv1_path, tsv2_path, output_path):
    # Load the two TSV files
    df1 = pd.read_csv(tsv1_path, sep="\t")
    df2 = pd.read_csv(tsv2_path, sep="\t")
    
    # Check if the row counts match
    if len(df1) != len(df2):
        raise ValueError("The two TSV files have a different number of rows and cannot be horizontally stacked.")
    
    # Concatenate them horizontally (aligning by rows)
    combined_df = pd.concat([df1, df2], axis=1)
    
    # Save the combined DataFrame to a new TSV file
    combined_df.to_csv(output_path, sep="\t", index=False)
    print(f"Horizontally stacked TSV saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Horizontally stack two TSV files by combining their rows side-by-side.")
    parser.add_argument("tsv1", type=str, help="Path to the first TSV file.")
    parser.add_argument("tsv2", type=str, help="Path to the second TSV file.")
    parser.add_argument("output", type=str, help="Path to save the stacked TSV file.")
    
    args = parser.parse_args()
    
    try:
        horizontal_stack_tsv(args.tsv1, args.tsv2, args.output)
    except ValueError as e:
        print(f"Error: {e}")