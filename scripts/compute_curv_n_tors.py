import argparse
import nibabel as nib
from dipy.io.streamline import load_trk
from dipy.tracking.metrics import mean_curvature
import numpy as np
import pandas as pd

def compute_torsion(streamline):
    tangent_vectors = np.gradient(streamline, axis=0)
    tangent_magnitudes = np.linalg.norm(tangent_vectors, axis=1)
    unit_tangents = tangent_vectors / tangent_magnitudes[:, None]
    
    curvatures = mean_curvature(streamline)
    curvature_magnitudes = np.abs(curvatures)
    normal_vectors = np.gradient(unit_tangents, axis=0) / (curvature_magnitudes[:, None] + 1e-8)
    
    binormal_vectors = np.cross(unit_tangents[:-1], normal_vectors[:-1])
    torsion_numerators = np.gradient(binormal_vectors, axis=0)[:-1] * unit_tangents[:-2]
    torsion = np.sum(torsion_numerators, axis=1) / (tangent_magnitudes[1:-1] + 1e-8)
    
    return np.nanmean(np.abs(torsion))  # Return the mean absolute torsion for the streamline

def calculate_tract_properties(tractogram, save_stats=None):
    streamlines = tractogram.streamlines
    curvatures = [np.nanmean(np.abs(mean_curvature(s))) for s in streamlines]
    torsions = [compute_torsion(s) for s in streamlines]

    # Combine results into a DataFrame
    data = {
        "Curvature (1/mm)": curvatures,
        "Torsion (1/mm)": torsions
    }
    df = pd.DataFrame(data)

    # Save results or print them
    if save_stats:
        df.to_csv(save_stats, sep="\t", index=False)
        print(f"Results saved to {save_stats}")
    else:
        print(df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute tract properties from a tractography file.")
    parser.add_argument("tractogram", type=str, help="Path to the tractogram file (e.g., .trk file).")
    parser.add_argument("--reference", type=str, default=None, help="Optional reference image to determine voxel size and spacing.")
    parser.add_argument("--save-stats", type=str, default=None, help="Path to save the results (tsv format).")

    args = parser.parse_args()

    # Determine voxel size (currently not used but required for compatibility)
    if args.reference:
        struct_nib = nib.load(args.reference)
        header = struct_nib.header
        voxel_size = header.get_zooms()
    else:
        sft = load_trk(args.tractogram, reference="same")
        affine, dimensions, voxel_sizes, _ = sft.space_attributes

    # Load the tractogram
    tractogram = load_trk(args.tractogram, reference="same")

    # Calculate properties
    calculate_tract_properties(tractogram, save_stats=args.save_stats)