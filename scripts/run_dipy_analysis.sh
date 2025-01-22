#! /bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/"

tcks=$1
trks=$2
anat=$3
dipy_stat_dir=$4

[ -d $trks ] ||  { mkdir $trks; }

for tck in $( ls ${tcks}/*.tck ); do
  
  ##### Dipy analysis
  echo "processing track" ${tck} "..."
  trk=${trks}/$( basename ${tck//'.tck'/'.trk'} )

  dipy_stat=${dipy_stat_dir}/$( basename ${trk//'.trk'/''} ).tsv

  bash ${SCRIPT_DIR}/dipy_analysis.sh ${tck}  ${anat} ${dipy_stat} ${trk}

  cat ${dipy_stat}

done