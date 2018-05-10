#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
PLASMID_MATCHES_DIR="${MAIN_DIR}/data/plasmid_matches"
GROUPS_DIR="${MAIN_DIR}/data/groups"
GROUP_MATCHES_DIR="${MAIN_DIR}/data/group_matches"

FAILED=0

mkdir -p ${GROUP_MATCHES_DIR} &> /dev/null
chmod 644 ${GROUP_MATCHES_DIR}/*_matches.tsv &> /dev/null
rm -f ${GROUP_MATCHES_DIR}/*_matches.tsv

while read ifn 
do
	GROUP=`basename "${ifn}" ".list"`
	ofn="${GROUP_MATCHES_DIR}/${GROUP}_matches.tsv"
	osfn="${GROUP_MATCHES_DIR}/${GROUP}_sorted_matches.tsv"

	# get the matches
	fns=`cat "${ifn}" | sed -r 's,^(.+)$,'"${PLASMID_MATCHES_DIR}"'/\1_matches.tsv,' | tr '\n' ' '`
	head -q -n 1 ${fns} | head -n 1 > "${ofn}"
	tail -q -n +2 ${fns} >> "${ofn}"

	TAIL_EXIT=$?

	if [ $TAIL_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like extracting MATCHES for ${GROUP} succeeded" 1>&2

		head -n 1 "${ofn}" \
			> "${osfn}"

		tail -n +2 "${ofn}" \
			| sort -s -t '	' -k 4,4 \
			| sort -s -t '	' -k 3,3 \
			| sort -s -t '	' -k 2,2 \
			| sort -s -t '	' -k 1,1 \
			>> "${osfn}"
	else
		printf "%s\n" "It looks like extracting MATCHES for ${GROUP} failed" 1>&2
	fi

	# increment the failed counter (if needed)
	if [ $TAIL_EXIT -ne 0 ]
	then
		FAILED=`bc <<< "${FAILED}+1"`
	fi

done < <(ls -1 "${GROUPS_DIR}"/*.list)

chmod 444 ${GROUP_MATCHES_DIR}/*_matches.tsv &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like generating the MATCHES for EACH group succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like generating the MATCHES for" "${FAILED}" "group(s) failed" 1>&2
fi

