import os
import pandas as pd
import argparse

def process_tract_files(folder_path, output_file):
    # Dictionary to store data with filenames as keys
    tract_data = {}
    measure_type = None

    # Loop through all files in the folder
    for idx, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".tsv"):
            file_path = os.path.join(folder_path, filename)
            
            # Extract the tract name from the filename (excluding extension)
            tract_name = os.path.splitext(filename)[0]
            
            # Read the file
            df = pd.read_csv(file_path, sep="\t", header=None)
            
            # Use the first column as "type of measure" if it's the first file
            if idx == 0:
                measure_type = df.iloc[:, 0].values
            
            # Use the second column as data and add it to the dictionary
            tract_data[tract_name] = df.iloc[:, 1].values

    # Create a DataFrame where each key in the dictionary is a column
    combined_df = pd.DataFrame(tract_data)
    
    # Add the "type of measure" as the first column
    combined_df.insert(0, "Type of Measure", measure_type)
    
    # Save the result to a new file
    combined_df.to_csv(output_file, sep="\t", index=False)
    print(f"Data successfully saved to {output_file}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Concatenate data from .tsv files in a folder, aligning columns by subjects.")
    parser.add_argument("folder", type=str, help="Path to the folder containing .tsv files")
    parser.add_argument("output", type=str, help="Path to the output .tsv file")
    
    args = parser.parse_args()
    
    # Process the folder
    process_tract_files(args.folder, args.output)