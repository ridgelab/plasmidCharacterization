#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
PLASMID_BLAST_RESULTS_DIR="${DATA_DIR}/plasmid_blast_results"
TREE_DIR="${DATA_DIR}/tree"
DISCARD_FILE="${DATA_DIR}/groups/discard/discard.list"
#KEEP_FILE="${DATA_DIR}/groups/keep/keep.list"

distInfo()
{
	local ACC1
	local ACC2
	local ACC1_FILE
	local DIST_FILE
	local COUNT
	local DIST
	local CMD_EXIT
	local COLS
	local DISCARD_CNT
	
	ACC1="${1}"
	ACC2="${2}"
	ACC1_FILE="${PLASMID_BLAST_RESULTS_DIR}/${ACC1}_covInfo.tsv"
	DIST_FILE="${TREE_DIR}/${ACC1}.dist"
	CMD_EXIT=0
	COLS=""

	# create the columns
	while read ifn2
	do
		ACC2=`basename "${ifn2}" "_covInfo.tsv"`
		ifn2="${PLASMID_BLAST_RESULTS_DIR}/${ifn2}"

		DISCARD_CNT=`grep -c "${ACC2}" "${DISCARD_FILE}"`
		if [ $DISCARD_CNT -eq 0 ]
		then
			if [ "${ACC1}" == "${ACC2}" ]
			then
				COLS="${COLS}0\t"
			else
				COUNT=`grep -c "${ACC2}" "${ACC1_FILE}"` # this should be zero or one
				if [ $COUNT -eq 0 ]
				then
					COLS="${COLS}1\t"

				elif [ $COUNT -eq 1 ]
				then

					FIELDS=`grep "${ACC2}" "${ACC1_FILE}"` # this will only ever be a single line
					DIST=`printf "${FIELDS}" | awk '{print 1 - (($2+$6)/($3+$7))}' | tr -d '\n'`
					COLS="${COLS}${DIST}\t"

				else
					printf "%s\n" "This shouldn't happen!" 1>&2
					CMD_EXIT=1
					break

				fi
			fi
		fi

	done < <(find "${PLASMID_BLAST_RESULTS_DIR}" -mindepth 1 -maxdepth 1 -type f -name '*_covInfo.tsv' -printf '%f\n' | sort -t '_' -k 1,1V)

	# write the columns
	printf "${COLS}" \
		| sed -r 's,\t$,\n,' \
		> "${DIST_FILE}"

	if [ $CMD_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like dist matrix calcs for ${ACCESSION} succeeded" 1>&2
	else
		printf "%s\n" "It looks like dist matrix calcs for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi
}

mkdir "${TREE_DIR}" &> /dev/null
rm -f "${TREE_DIR}"/*.dist &> /dev/null

FAILED=0

while read ifn
do
	ACCESSION=`basename "${ifn}" "_covInfo.tsv"`
	ifn="${PLASMID_BLAST_RESULTS_DIR}/${ifn}"

	DISCARD_COUNT=`grep -c "${ACCESSION}" "${DISCARD_FILE}"`
	if [ $DISCARD_COUNT -eq 0 ]
	then
		distInfo "${ACCESSION}" &

		while [ `jobs -p | wc -l | tr -d ' '` -ge 12 ]
		do
			for job in `jobs -p`
			do
				if [ ${job} -ne $$ ]
				then
					#wait ${job}
					sleep 3
					break
				fi
			done
		done
	fi


done < <(find "${PLASMID_BLAST_RESULTS_DIR}" -mindepth 1 -maxdepth 1 -type f -name '*_covInfo.tsv' -printf '%f\n' | sort -t '_' -k 1,1V)

wait `jobs -p`

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like dist matrix calcs for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like dist matrix calcs for" "${FAILED} " "accession(s) failed" 1>&2
fi

chmod 644 ${TREE_DIR}/dist_matrix.tsv &> /dev/null
rm -f ${TREE_DIR}/dist_matrix.tsv &> /dev/null

# write the title line
TMP="/tmp/$$"
ls -1 "${PLASMID_BLAST_RESULTS_DIR}"/*_covInfo.tsv \
        | sed -r 's,^.+/(.+)_covInfo\.tsv$,\1,' \
        | sort -V \
        > "${TMP}"

comm --nocheck-order -2 -3 "${TMP}" <(sort -V "${DISCARD_FILE}") \
        | tr '\n' '\t' \
        | sed -r 's,\t$,\n,' \
        | sed -r 's,^,accession\t,' \
        > "${TREE_DIR}/dist_matrix.tsv"

rm -f "${TMP}"

# write the remaining lines
while read ifn 
do
	ACCESSION=`basename "${ifn}" ".dist"`
	ifn="${TREE_DIR}/${ifn}"

	printf "${ACCESSION}\t" >> "${TREE_DIR}/dist_matrix.tsv"
	cat "${ifn}" >> "${TREE_DIR}/dist_matrix.tsv"

done < <(find "${TREE_DIR}" -mindepth 1 -maxdepth 1 -type f -name '*.dist' -printf '%f\n' | sort -t '.' -k 1,1V)

chmod 444 ${TREE_DIR}/dist_matrix.tsv &> /dev/null

exit ${FAILED}

# NOTE that the input tsv file has the following columns:
#
#	1      2      3    4    5      6      7    8
#	qseqid qcount qlen qcov sseqid qcount qlen qcov
#
