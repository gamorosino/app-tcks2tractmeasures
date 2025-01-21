#! /bin/bash
  tck=$1
  anat=$2
  
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

  [ -d ./trk ] || {  mkdir ./trk; }

  trk=./trk/$( basename ${tck//'.tck'/'.trk'} )

  [ $( exists ${trk}  ) -eq 0  ] && {  python ./scripts/tck2trk.py ${anat} ${tck}; mv ${tck//'.tck'/'.trk'} ./trk; }

  echo 'Calculate curvature and torsion using dipy...'
  
  python ./scripts/compute_curv_n_tors.py ${trk} --save-stats ./stat/curv_tors.tsv