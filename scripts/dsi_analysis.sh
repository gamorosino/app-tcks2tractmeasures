
  #! /bin/bash
  
  trk=$1
  dsi_stat=$2
  
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

  if [[ -f "${tt}.stat.txt" ]]; then
    mv "${tt}.stat.txt" ${dsi_stat}
  else
    echo "ERROR: Output file not generated. Check DSI Studio logs."
    exit 1
  fi

  echo "DSI Studio analysis completed successfully!"