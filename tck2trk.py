import argparse
import os
import nibabel as nib
from nibabel.streamlines import Field
from nibabel.orientations import aff2axcodes
import sys

def build_argparser_tck2trk():
    DESCRIPTION = "Convert tractograms (TCK -> TRK)."
    p = argparse.ArgumentParser(description=DESCRIPTION)
    p.add_argument('anatomy', help='Reference anatomy image (.nii|.nii.gz).')
    p.add_argument('tractograms', metavar='tractogram', nargs="+", help='List of tractograms (.tck).')
    p.add_argument('-f', '--force', action="store_true", help='Overwrite existing output files.')
    return p

def tck2trk(args=None):
    parser = build_argparser_tck2trk()
    if args is not None:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    try:
        nii = nib.load(args.anatomy)
    except Exception as e:
        print("Failed to load the anatomy image '{}': {}".format(args.anatomy, e), file=sys.stderr)
        sys.exit(1)

    for tractogram in args.tractograms:
        if nib.streamlines.detect_format(tractogram) is not nib.streamlines.TckFile:
            print("Skipping non-TCK file: '{}'".format(tractogram))
            continue

        output_filename = os.path.splitext(tractogram)[0] + '.trk'
        if os.path.isfile(output_filename) and not args.force:
            print("Skipping existing file: '{}'. Use -f to overwrite.".format(output_filename))
            continue

        header = {}
        header[Field.VOXEL_TO_RASMM] = nii.affine.copy()
        header[Field.VOXEL_SIZES] = nii.header.get_zooms()[:3]
        header[Field.DIMENSIONS] = nii.shape[:3]
        header[Field.VOXEL_ORDER] = "".join(aff2axcodes(nii.affine))

        try:
            tck = nib.streamlines.load(tractogram)
            nib.streamlines.save(tck.tractogram, output_filename, header=header)
            print("Converted: '{}' -> '{}'".format(tractogram, output_filename))
        except Exception as e:
            print("Error converting '{}': {}".format(tractogram, e), file=sys.stderr)

if __name__ == "__main__":
    tck2trk()
