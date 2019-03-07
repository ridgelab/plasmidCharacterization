#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
PLASMID_FASTA_DIR="${DATA_DIR}/plasmid_fasta"
PLASMID_BLAST_RESULTS_DIR="${DATA_DIR}/plasmid_blast_results"

FAILED=0

chmod 644 ${PLASMID_BLAST_RESULTS_DIR}/*_fmt6c.tsv &> /dev/null
#rm -f ${PLASMID_BLAST_RESULTS_DIR}/*_fmt6c.tsv

while read ifn 
do
	ACCESSION=`basename "${ifn}" ".fasta"`
	${SCRIPTS_DIR}/blastPlasmids.sh "${ACCESSION}"

	BLAST_EXIT=$?

	if [ $BLAST_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like blasting for ${ACCESSION} succeeded" 1>&2
	else
		printf "%s\n" "It looks like blasting for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi

done < <(ls -1 "${PLASMID_FASTA_DIR}"/*.fasta)

chmod 444 ${PLASMID_BLAST_RESULTS_DIR}/*_fmt6c.tsv &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like blasting for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like blasting for" "${FAILED} " "accession(s) failed" 1>&2
fi

