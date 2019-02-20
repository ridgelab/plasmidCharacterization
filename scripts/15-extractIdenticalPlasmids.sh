#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
PLASMID_BLAST_RESULTS_DIR="${DATA_DIR}/plasmid_blast_results"

FAILED=0

chmod 644 ${PLASMID_BLAST_RESULTS_DIR}/*_identicalPlasmids.list &> /dev/null
rm -f ${PLASMID_BLAST_RESULTS_DIR}/*_identicalPlasmids.list

while read ifn 
do
	ACCESSION=`basename "${ifn}" "_fmt6c_cov98.tsv"`
	cut -f 2 "${PLASMID_BLAST_RESULTS_DIR}/${ACCESSION}_fmt6c_cov98.tsv" \
		| sort \
		| uniq \
		| awk '/^'${ACCESSION}'$/{next;}{print $0}' \
		> "${PLASMID_BLAST_RESULTS_DIR}/${ACCESSION}_identicalPlasmids.list"

	COMMAND_EXIT=$?

	if [ $COMMAND_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like extracting identical plasmids for ${ACCESSION} succeeded" 1>&2
	else
		printf "%s\n" "It looks like extracting identical plasmids for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi

done < <(ls -1 "${PLASMID_BLAST_RESULTS_DIR}"/*_fmt6c_cov98.tsv)

chmod 444 ${PLASMID_BLAST_RESULTS_DIR}/*_identicalPlasmids.list &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like extracting identical plasmids for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like extracting identical plasmids for" "${FAILED} " "accession(s) failed" 1>&2
fi

# NOTE that the blastn output is a customized format 6. It had qcov and scov added as
# columns 14 and 15. It will be tab-separated and have the following columns:
#
#	1      2      3      4      5      6      7    8      9    10     11   12     13   14   15   16   17
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send qcov scov qseq sseq
#
