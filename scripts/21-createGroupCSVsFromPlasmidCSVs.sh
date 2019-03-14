#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
PLASMID_CSV_DIR="${MAIN_DIR}/data/plasmid_csv"
GROUPS_DIR="${MAIN_DIR}/data/groups/keep"
GROUP_CSV_DIR="${MAIN_DIR}/data/group_csv"

FAILED=0

mkdir -p ${GROUP_CSV_DIR} &> /dev/null
chmod 644 ${GROUP_CSV_DIR}/*.csv &> /dev/null
rm -f ${GROUP_CSV_DIR}/*.csv

while read ifn 
do
	GROUP=`basename "${ifn}" ".list"`
	ofn="${GROUP_CSV_DIR}/${GROUP}.csv"

	# get the header
	hfn=`head -q -n 1 "${ifn}"`".csv"
	hfn="${PLASMID_CSV_DIR}/${hfn}"
	head -q -n 1 "${hfn}" > "${ofn}"
	
	HEAD_EXIT=$?

	if [ $HEAD_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like extracting header for ${GROUP} CSV succeeded" 1>&2
	else
		printf "%s\n" "It looks like extracting for ${GROUP} CSV failed" 1>&2
	fi

	# get the non-header csv lines
	nhfns=`cat "${ifn}" | sed -r 's,^(.+)$,'"${PLASMID_CSV_DIR}"'/\1.csv,' | tr '\n' ' '`
	tail -q -n +2 ${nhfns} >> "${ofn}"

	TAIL_EXIT=$?

	if [ $TAIL_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like extracting CSV lines for ${GROUP} succeeded" 1>&2
	else
		printf "%s\n" "It looks like extracting CSV lines for ${GROUP} failed" 1>&2
	fi

	# increment the failed counter (if needed)
	if [ $TAIL_EXIT -ne 0 ] || [ $HEAD_EXIT -ne 0 ]
	then
		FAILED=`bc <<< "${FAILED}+1"`
	fi

done < <(ls -1 "${GROUPS_DIR}"/*.list | grep -v "keep.list")

chmod 444 ${GROUP_CSV_DIR}/*.csv &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like generating the CSV for EACH group succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like generating the CSV for" "${FAILED}" "group(s) failed" 1>&2
fi

