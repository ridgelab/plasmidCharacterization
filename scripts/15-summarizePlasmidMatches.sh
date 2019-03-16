#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
PLASMID_MATCHES_DIR="${MAIN_DIR}/data/plasmid_matches"

FAILED=0

chmod 644 ${PLASMID_MATCHES_DIR}/*_matches-summary.tsv &> /dev/null
rm -f ${PLASMID_MATCHES_DIR}/*_matches-summary.tsv

while read SMFN
do
	ACCESSION=`basename "${SMFN}" "_sorted_matches.tsv"`

	python3 ${SCRIPTS_DIR}/summarizePlasmidMatchInfo.py \
		"${ACCESSION}" \
		"${PLASMID_MATCHES_DIR}"

	COMMAND_EXIT=$?

	if [ $COMMAND_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like summarizing matches for ${ACCESSION} succeeded" 1>&2
	else
		printf "%s\n" "It looks like summarizing matches for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi

done < <(ls -1 "${PLASMID_MATCHES_DIR}"/*_sorted_matches.tsv)

chmod 444 ${PLASMID_MATCHES_DIR}/*_matches-summary.tsv &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like summarizing matches for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like summarizing matches for" "${FAILED}" "accession(s) failed" 1>&2
fi

