#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
PLASMID_BLAST_RESULTS_DIR="${DATA_DIR}/plasmid_blast_results"

chmod 644 ${PLASMID_BLAST_RESULTS_DIR}/*_identicalPlasmids_concordance.list &> /dev/null
chmod 644 ${PLASMID_BLAST_RESULTS_DIR}/*_covInfo_concordance.tsv &> /dev/null
rm -f ${PLASMID_BLAST_RESULTS_DIR}/*_identicalPlasmids_concordance.list
rm -f ${PLASMID_BLAST_RESULTS_DIR}/*_covInfo_concordance.tsv

python3 ${SCRIPTS_DIR}/fixIdenticalPlasmidsNonConcordance.py \
	"${PLASMID_BLAST_RESULTS_DIR}" \
	"${PLASMID_BLAST_RESULTS_DIR}" \
	"_covInfo.tsv" \
	"_covInfo_concordant.tsv" \
	"_identicalPlasmids.list" \
	"_identicalPlasmids_concordant.list"

	#1- coverage info path
	#2- identical plasmids path
	#3- input coverage info suffix
	#4- output coverage info suffix
	#5- input identical plasmid suffix
	#6- output identical plasmid suffix

CMD_EXIT=$?

chmod 444 ${PLASMID_BLAST_RESULTS_DIR}/*_identicalPlasmids_concordance.list &> /dev/null
chmod 444 ${PLASMID_BLAST_RESULTS_DIR}/*_covInfo_concordance.tsv &> /dev/null

exit ${CMD_EXIT}

