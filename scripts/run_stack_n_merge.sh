#! /bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/"

dsi_stat_dir=$1
dipy_stat_dir=$2
stat_dir=$3
output=$4
merge_dir=$( dirname ${stat_dir} )'/merge_dir_temp/'
mkdir $merge_dir
for dsi_stat in $( ls ${dsi_stat_dir}/*.tsv ); do  

  dipy_stat=${dipy_stat_dir}'/'$( basename ${dsi_stat} )

  echo "merging..."  ${dsi_stat} " and " ${dipy_stat}

  stat_track=${merge_dir}/$( basename ${dsi_stat} )

  python ${SCRIPT_DIR}/vstack_tsv.py ${dsi_stat} ${dipy_stat} ${stat_track} 

  cat ${stat_track}

done

output_tsv=${output//'.csv'/'.tsv'}

python ${SCRIPT_DIR}/merge_tractmeasures.py ${merge_dir} ${output}

python  ${SCRIPT_DIR}/tsv2csv.py ${output_tsv} ${output}

rm ${output_tsv}

[ -d $merge_dir ] && { rm -rf $merge_dir; }

echo Data successfully saved to ${output}