#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
INCOMP_BLAST_RESULTS_DIR="${MAIN_DIR}/data/incompatibility_groups/blast_results"

FAILED=0

chmod 644 ${INCOMP_BLAST_RESULTS_DIR}/*_fmt6c_cov60_fam.tsv &> /dev/null
rm -f ${INCOMP_BLAST_RESULTS_DIR}/*_fmt6c_cov60_fam.tsv

while read ifn 
do
	ACCESSION=`basename "${ifn}" "_fmt6c_cov60.tsv"`
	${SCRIPTS_DIR}/addFamCol.awk "${INCOMP_BLAST_RESULTS_DIR}/${ACCESSION}_fmt6c_cov60.tsv" > "${INCOMP_BLAST_RESULTS_DIR}/${ACCESSION}_fmt6c_cov60_fam.tsv"

	AWK_EXIT=$?

	if [ $AWK_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like adding family column for ${ACCESSION} succeeded" 1>&2
	else
		printf "%s\n" "It looks like adding family column for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi

done < <(ls -1 "${INCOMP_BLAST_RESULTS_DIR}"/*_fmt6c_cov60.tsv)

chmod 444 ${INCOMP_BLAST_RESULTS_DIR}/*_fmt6c_cov60_fam.tsv &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like adding family column for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like adding family column for" "${FAILED} " "accession(s) failed" 1>&2
fi

# NOTE that the blastn output is a customized format 6. It had scov added as
# column 14. It will be tab-separated and have the following columns:
#
#	1      2      3      4      5      6      7      8    9    10     11   12     13   14    15   16
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send scov qseq sseq
#
# After this is run, it will have a new column (family, col 3) and will look like this:
#
#	1      2      3      4      5      6      7      8    9      10   11     12   13     14   15   16   17
#	qseqid sseqid family pident length evalue qframe qlen qstart qend sframe slen sstart send scov qseq sseq
#
