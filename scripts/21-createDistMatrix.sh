#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
PLASMID_BLAST_RESULTS_DIR="${DATA_DIR}/plasmid_blast_results"
TREE_DIR="${DATA_DIR}/tree"

mkdir "${TREE_DIR}" &> /dev/null

chmod 644 ${TREE_DIR}/dist_matrix.tsv &> /dev/null
rm -f ${TREE_DIR}/dist_matrix.tsv &> /dev/null

# write the title line
ls -1 "${PLASMID_BLAST_RESULTS_DIR}"/*_covInfo.tsv \
	| gsed -r 's,^.+/(.+)_covInfo\.tsv$,\1,' \
	| sort -V \
	| tr '\n' '\t' \
	| gsed -r 's,\t$,\n,' \
	| gsed -r 's,^,accession\t,' \
	> "${TREE_DIR}/dist_matrix.tsv"

while read ifn 
do
	ACCESSION=`basename "${ifn}" "_covInfo.tsv"`
	ifn="${PLASMID_BLAST_RESULTS_DIR}/${ifn}"

	printf "%s\t" "${ACCESSION}" >> "${TREE_DIR}/dist_matrix.tsv" # write the accession number

	# create the remaining columns
	COLS=""
	while read ifn2
	do
		ACC2=`basename "${ifn2}" "_covInfo.tsv"`
		ifn2="${PLASMID_BLAST_RESULTS_DIR}/${ifn2}"

		if [ "${ACCESSION}" == "${ACC2}" ]
		then
			COLS="${COLS}0\t"
		else
			COUNT=`grep -c "${ACC2}" "${ifn}"` # this should be zero or one
			if [ $COUNT -eq 0 ]
			then
				COLS="${COLS}1\t"
			elif [ $COUNT -eq 1 ]
			then

				FIELDS=`grep "${ACC2}" "${ifn}"` # this will only ever be a single line
				DIST=`printf "${FIELDS}" | awk '{print 1 - (($2+$6)/($3+$7))}' | tr -d '\n'`
				COLS="${COLS}${DIST}\t"
			else
				printf "%s\n" "This shouldn't happen!" 1>&2
				exit 1
			fi
		fi

	#done < <(ls -1 "${PLASMID_BLAST_RESULTS_DIR}"/*_covInfo.tsv | sort -t '_' -k 1,1V)
	done < <(gfind "${PLASMID_BLAST_RESULTS_DIR}" -mindepth 1 -maxdepth 1 -type f -name '*_covInfo.tsv' -printf '%f\n' | sort -t '_' -k 1,1V)
	
	
	# write the remaining columns
	printf "${COLS}" \
		| gsed -r 's,\t$,\n,' \
		>> "${TREE_DIR}/dist_matrix.tsv"

done < <(gfind "${PLASMID_BLAST_RESULTS_DIR}" -mindepth 1 -maxdepth 1 -type f -name '*_covInfo.tsv' -printf '%f\n' | sort -t '_' -k 1,1V)
#done < <(ls -1 "${PLASMID_BLAST_RESULTS_DIR}"/*_covInfo.tsv | sort -t '_' -k 1,1V)

chmod 444 ${TREE_DIR}/dist_matrix.tsv &> /dev/null

# NOTE that the input tsv file has the following columns:
#
#	1      2      3    4    5      6      7    8
#	qseqid qcount qlen qcov sseqid qcount qlen qcov
#
