#! /bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/"

trks=$1
dsi_stat_dir=$2

for trk in $( ls ${trks}/*.trk ); do  
  ##### DSI analysis

  dsi_stat=${dsi_stat_dir}/$( basename ${trk//'.trk'/''} ).tsv
  
   bash ${SCRIPT_DIR}/dsi_analysis.sh ${trk} ${dsi_stat}

  cat ${dsi_stat}

done