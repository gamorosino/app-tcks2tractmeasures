#! /bin/bash
  tck=$1
  anat=$2
  stat=$3
  trk=$4
  
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/"

  exists () {                      			
		if [ $# -lt 1 ]; then
		    echo $0: "usage: exists <filename> "
		    echo "    echo 1 if the file (or folder) exists, 0 otherwise"
		    return 1;		    
		fi 
		
		if [ -d "${1}" ]; then 

			echo 1;
		else
			([ -e "${1}" ] && [ -f "${1}" ]) && { echo 1; } || { echo 0; }	
		fi		
		};



  ##### Convert tck to trk

  if [ -z $trk ]; then
  
    [ -d ${SCRIPT_DIR}/trk ] || {  mkdir ${SCRIPT_DIR}/trk; }

    trk=${SCRIPT_DIR}/trk/$( basename ${tck//'.tck'/'.trk'} )
  fi

  [ $( exists ${trk}  ) -eq 0  ] && {  python ${SCRIPT_DIR}/tck2trk.py ${anat} ${tck}; mv ${tck//'.tck'/'.trk'} ${trk}; }

  echo 'Calculate curvature and torsion using dipy...'
  
  python ${SCRIPT_DIR}/compute_curv_n_tors.py ${trk} --save-stats ${stat}