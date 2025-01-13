import os
import pandas as pd
import argparse

def process_tract_files(folder_path, output_file):
    # Initialize an empty list to store dataframes
    dataframes = []
    
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".tsv"):
            file_path = os.path.join(folder_path, filename)
            
            # Extract the tract name from the filename (excluding extension)
            tract_name = os.path.splitext(filename)[0]
            
            # Read the file
            df = pd.read_csv(file_path, sep="\t", header=None)
            
            # Add a new column with the tract name
            df.columns = ['Index', 'Measurement']
            df.insert(0, 'Tract', tract_name)
            
            # Append the dataframe to the list
            dataframes.append(df)
    
    # Check if there are any valid .tsv files
    if not dataframes:
        print("No .tsv files found in the specified folder.")
        return
    
    # Concatenate all dataframes
    concatenated_df = pd.concat(dataframes, ignore_index=True)
    
    # Save the result to a new file
    concatenated_df.to_csv(output_file, sep="\t", index=False)
    print(f"Data successfully saved to {output_file}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Concatenate data from .tsv files in a folder.")
    parser.add_argument("folder", type=str, help="Path to the folder containing .tsv files")
    parser.add_argument("output", type=str, help="Path to the output .tsv file")
    
    args = parser.parse_args()
    
    # Process the folder
    process_tract_files(args.folder, args.output)