
  #! /bin/bash
  
  trk=$1
  
  gzip -c ${trk} > data.${trk##*/}.gz

  dsi_studio --action=exp --source=data.${trk##*/}.gz --output=data.${trk##*/}.tt.gz

  rm -f data.${trk##*/}.gz

  # move file to tt folder
  mkdir -p tt
  tt=tt/$( basename ${trk//'.trk'/''} ).tt.gz
  mv data.${trk##*/}.tt.gz ${tt}

  ##### analyze tt file

  echo "Starting DSI Studio analysis..."
  dsi_studio --action=ana --source="${tt}" --tract="${tt}" --export=stat

  # Move file to stat folder
  mkdir -p stat
  if [[ -f "${tt}.stat.txt" ]]; then
    mv "${tt}.stat.txt" ./stat/tractmeasure.tsv
  else
    echo "ERROR: Output file not generated. Check DSI Studio logs."
    exit 1
  fi

  stat_track=stat/$( basename ${trk//'.trk'/''} ).tsv
  mv ./stat/tractmeasure.tsv ${stat_track}

  echo "DSI Studio analysis completed successfully!"