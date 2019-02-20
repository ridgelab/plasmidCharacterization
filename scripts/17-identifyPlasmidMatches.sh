#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
PLASMID_FASTA_DIR="${MAIN_DIR}/data/plasmid_fasta"
PLASMID_SEARCH_REGIONS_DIR="${MAIN_DIR}/data/plasmid_searchRegions"
PLASMID_MATCHES_DIR="${MAIN_DIR}/data/plasmid_matches"

FAILED=0

mkdir -p ${PLASMID_MATCHES_DIR} &> /dev/null
chmod 644 ${PLASMID_MATCHES_DIR}/*_matches.tsv &> /dev/null
rm -f ${PLASMID_MATCHES_DIR}/*_matches.tsv

while read ifn 
do
	ACCESSION=`basename "${ifn}" "_searchRegions.gb"`
	python3 ${SCRIPTS_DIR}/identifyPlasmidMatches.py \
		"${ACCESSION}" \
		"${PLASMID_SEARCH_REGIONS_DIR}" \
		"${PLASMID_MATCHES_DIR}"
	
	COMMAND_EXIT=$?

	if [ $COMMAND_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like identifying matches for ${ACCESSION} succeeded" 1>&2

		head -n 1 "${PLASMID_MATCHES_DIR}/${ACCESSION}_matches.tsv" \
			> "${PLASMID_MATCHES_DIR}/${ACCESSION}_sorted_matches.tsv"

		tail -n +2 "${PLASMID_MATCHES_DIR}/${ACCESSION}_matches.tsv" \
			| sort -s -t '	' -k 4,4 \
			| sort -s -t '	' -k 3,3 \
			| sort -s -t '	' -k 2,2 \
			| sort -s -t '	' -k 1,1 \
			>> "${PLASMID_MATCHES_DIR}/${ACCESSION}_sorted_matches.tsv"
	else
		printf "%s\n" "It looks like identifying matches for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi


done < <(ls -1 "${PLASMID_SEARCH_REGIONS_DIR}"/*_searchRegions.gb)

chmod 444 ${PLASMID_MATCHES_DIR}/*_matches.tsv &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like identifying matches for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like identifying matches for" "${FAILED}" "accession(s) failed" 1>&2
fi

