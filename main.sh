#!/bin/bash

tcks=${1}
anat=${2}
outputdir=${3}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/"
[ -z ${outputdir} ] && {  outputdir=${SCRIPT_DIR}; } \
                    || { mkdir -p ${outputdir}; }
trks=${outputdir}/trks

run_dipy=${SCRIPT_DIR}/scripts/run_dipy_analysis.sh
run_dsi=${SCRIPT_DIR}/scripts/run_dsi_analysis.sh 
run_merge=${SCRIPT_DIR}/scripts/run_stack_n_merge.sh

# Check if the required arguments are provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <tcks> <anat> [outputdir]"
    echo ""
    echo "Arguments:"
    echo "  <tcks>       Path to the folder containing TCK files (tractogram files)."
    echo "  <anat>       Path to the anatomical file."
    echo "  [outputdir]  Optional: Path to the output directory where results will be stored."
    echo "               If not provided, the output is saved in the same directory where the script is executed."
    echo ""
    echo "Description:"
    echo "  This script performs tract-based analysis using Dipy and DSI Studio tools,"
    echo "  on all the tracts in the TCK folder and merges the results into a single CSV file."
    echo "  By default, the output is stored as ./stat/tractmeasures.csv."
    echo ""
    echo "Example:"
    echo "  $0 ./tcks_folder reference.nii.gz"
    echo "  $0 ./tcks_folder reference.nii.gz /path/to/output"
    exit 1
fi


##### Dipy analysis
dipy_stat_dir=${outputdir}/dipy_stat
[ -d ${dipy_stat_dir} ] || { mkdir ${dipy_stat_dir}; }
singularity exec -e docker://brainlife/dipy:1.4.1 bash ${run_dipy} ${tcks} ${trks} ${anat} ${dipy_stat_dir} 

##### DSI analysis
dsi_stat_dir=${outputdir}/dsi_stat
[ -d ${dsi_stat_dir} ] || { mkdir ${dsi_stat_dir}; }
singularity exec -e docker://dsistudio/dsistudio:hou-2025-04-29 bash ${run_dsi} ${trks} ${dsi_stat_dir}

##### merging results
stat_dir=${outputdir}//stat
output=${stat_dir}/tractmeasures.csv
[ -d ${stat_dir} ] || { mkdir ${stat_dir} ; }
singularity exec -e docker://brainlife/dipy:1.4.1 bash ${run_merge} ${dsi_stat_dir} ${dipy_stat_dir} ${stat_dir} ${output}


