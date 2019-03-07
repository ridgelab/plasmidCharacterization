#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
PLASMID_BLAST_RESULTS_DIR="${DATA_DIR}/plasmid_blast_results"

extractIdenticalPlasmids()
{
	local ACCESSION
	ACCESSION="${1}"

	python3 ${SCRIPTS_DIR}/queryAndSubCovCutoff98-multiHit.py \
		"${PLASMID_BLAST_RESULTS_DIR}/${ACCESSION}_fmt6c.tsv" \
		"${PLASMID_BLAST_RESULTS_DIR}/${ACCESSION}_identicalPlasmids.list" \
		"${PLASMID_BLAST_RESULTS_DIR}/${ACCESSION}_covInfo.tsv"

	local CMD_EXIT
	CMD_EXIT=$?

	if [ $CMD_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like q&s cov. cutoff (98%) for ${ACCESSION} succeeded" 1>&2
	else
		printf "%s\n" "It looks like q&s cov. cutoff (98%) for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi
}

FAILED=0

chmod 644 ${PLASMID_BLAST_RESULTS_DIR}/*_identicalPlasmids.list &> /dev/null
rm -f ${PLASMID_BLAST_RESULTS_DIR}/*_identicalPlasmids.list

while read ifn 
do
	ACCESSION=`basename "${ifn}" "_fmt6c.tsv"`

	extractIdenticalPlasmids "${ACCESSION}" &

	while [ `jobs -p | wc -l | tr -d ' '` -ge 8 ]
        do
                for job in `jobs -p`
                do
                        if [ ${job} -ne $$ ]
                        then
                                wait ${job}
                                break
                        fi
                done
        done

done < <(ls -1 "${PLASMID_BLAST_RESULTS_DIR}"/*_fmt6c.tsv)

wait `jobs -p`

chmod 444 ${PLASMID_BLAST_RESULTS_DIR}/*_identicalPlasmids.list &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like q&s cov. cutoff (98%) for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like q&s cov. cutoff (98%) for" "${FAILED} " "accession(s) failed" 1>&2
fi

exit ${FAILED} # 0: success, 1+: failed


# NOTE that the blastn output is a customized format 6. It will be
# tab-separated and have the following columns:
#
#	1      2      3      4      5      6      7    8      9    10     11   12     13   14   15
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send qseq sseq
#
# After this is run, it will have two new columns (qcov & scov, cols 14 & 15) and will look like this:
#
#	1      2      3      4      5      6      7      8    9    10     11   12     13   14   15   16   17
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send qcov scov qseq sseq
#

