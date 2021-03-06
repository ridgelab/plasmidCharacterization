#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
PLASMID_FASTA_DIR="${MAIN_DIR}/data/plasmid_fasta"
PLASMID_CSV_DIR="${MAIN_DIR}/data/plasmid_csv"
PLASMID_MATCHES_DIR="${MAIN_DIR}/data/plasmid_matches"
INCOMP_BLAST_RESULTS_DIR="${MAIN_DIR}/data/incompatibility_groups/blast_results"
SOURCE_INFO_FN="${MAIN_DIR}/data/plasmid_sourceInfo/sourceInfo.tsv"
PLASMID_BLAST_RESULTS_DIR="${MAIN_DIR}/data/plasmid_blast_results"
SEQ_TECHS_FN="${MAIN_DIR}/data/plasmid_seqTech/seqTech.tsv"
DISCARDED_PLASMIDS_FN="${MAIN_DIR}/data/groups/discard/discard.list"
KEEP_FILE="${MAIN_DIR}/data/groups/keep/keep.list"

FAILED=0

mkdir -p ${PLASMID_CSV_DIR} &> /dev/null
chmod 644 ${PLASMID_CSV_DIR}/*.csv &> /dev/null
rm -f ${PLASMID_CSV_DIR}/*.csv

while read ACCESSION
do
	python3 ${SCRIPTS_DIR}/generatePlasmidCSV.py \
		"${ACCESSION}" \
		"${PLASMID_CSV_DIR}" \
		"${PLASMID_FASTA_DIR}" \
		"${PLASMID_MATCHES_DIR}" \
		"${INCOMP_BLAST_RESULTS_DIR}" \
		"${SOURCE_INFO_FN}" \
		"${PLASMID_BLAST_RESULTS_DIR}" \
		"${DISCARDED_PLASMIDS_FN}" \
		"${SEQ_TECHS_FN}"

	COMMAND_EXIT=$?

	if [ $COMMAND_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like generating plasmid CSV for ${ACCESSION} succeeded" 1>&2
	else
		printf "%s\n" "It looks like generating plasmid CSV for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi

done < "${KEEP_FILE}"

chmod 444 ${PLASMID_CSV_DIR}/*.csv &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like generating plasmid CSV for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like generating plasmid CSV for" "${FAILED}" "accession(s) failed" 1>&2
fi

