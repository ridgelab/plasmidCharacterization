#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
PLASMID_GB_DIR="${MAIN_DIR}/data/plasmid_gb"
PLASMID_FASTA_DIR="${MAIN_DIR}/data/plasmid_fasta"

mkdir -p ${PLASMID_FASTA_DIR} &> /dev/null

while read ifn 
do
	bfn=`basename "${ifn}" ".gb"`
	ofn="${PLASMID_FASTA_DIR}/${bfn}.fasta"
	lfn="${PLASMID_FASTA_DIR}/${bfn}.length"

	if [ -e "${ofn}" ]
	then
		chmod 644 "${ofn}" "${lfn}" &> /dev/null
		rm -f "${ofn}" "${lfn}"
	fi
	
	awk \
		-f "${SCRIPTS_DIR}/extractOriginSeqFromGBtoFasta.awk" \
		"${ifn}" \
		> "${ofn}"
	
	tail -n 1 "${ofn}" | wc -m > "${lfn}"
	
	chmod 444 "${ofn}" "${lfn}" &> /dev/null

done < <(ls -1 "${PLASMID_GB_DIR}"/*.gb)

