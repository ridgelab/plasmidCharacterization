#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
PLASMID_FASTA_DIR="${MAIN_DIR}/data/plasmid_fasta"
INCOMP_BLAST_RESULTS_DIR="${MAIN_DIR}/data/incompatibility_groups/blast_results"

FAILED=0

mkdir -p ${INCOMP_BLAST_RESULTS_DIR} &> /dev/null
chmod 644 ${INCOMP_BLAST_RESULTS_DIR}/*_fmt6c.tsv &> /dev/null
rm -f ${INCOMP_BLAST_RESULTS_DIR}/*_fmt6c.tsv

while read ifn 
do
	ACCESSION=`basename "${ifn}" ".fasta"`
	${SCRIPTS_DIR}/blast.sh "${ACCESSION}"

	BLAST_EXIT=$?

	if [ $BLAST_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like blasting for ${ACCESSION} succeeded" 1>&2
	else
		printf "%s\n" "It looks like blasting for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi

done < <(ls -1 "${PLASMID_FASTA_DIR}"/*.fasta)

chmod 444 ${INCOMP_BLAST_RESULTS_DIR}/*_fmt6c.tsv &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like blasting for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like blasting for" "${FAILED} " "accession(s) failed" 1>&2
fi

