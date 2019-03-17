#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
PLASMID_FASTA_DIR="${DATA_DIR}/plasmid_fasta"
PLASMID_BLAST_RESULTS_DIR="${DATA_DIR}/plasmid_blast_results"
KEEP_FILE="${DATA_DIR}/groups/keep/keep.list"

FAILED=0

chmod 644 ${PLASMID_BLAST_RESULTS_DIR}/*_fmt6c.tsv &> /dev/null
rm -f ${PLASMID_BLAST_RESULTS_DIR}/*_fmt6c.tsv

while read ACCESSION
do
	${SCRIPTS_DIR}/blastPlasmids.sh "${ACCESSION}" &

	while [ `jobs -p | wc -l | tr -d ' '` -ge  4 ]
	do
		for job in `jobs -p`
		do
			if [ ${job} -ne $$ ]
			then
				sleep 1
				break
			fi
		done
	done

done < "${KEEP_FILE}"

wait `jobs -p`

chmod 444 ${PLASMID_BLAST_RESULTS_DIR}/*_fmt6c.tsv &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like blasting for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like blasting for" "${FAILED} " "accession(s) failed" 1>&2
fi

