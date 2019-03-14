#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
GROUPS_DIR="${MAIN_DIR}/data/groups/keep"
GROUP_CSV_DIR="${MAIN_DIR}/data/group_csv"
GROUP_STATS_DIR="${MAIN_DIR}/data/group_stats"

FAILED=0

mkdir -p ${GROUP_STATS_DIR} &> /dev/null
chmod 644 ${GROUP_STATS_DIR}/*.stats &> /dev/null
rm -f ${GROUP_STATS_DIR}/*.stats

while read gfn 
do
	GROUP=`basename "${gfn}" ".list"`
	ifn="${GROUP_CSV_DIR}/${GROUP}.csv"
	ofn="${GROUP_STATS_DIR}/${GROUP}.stats"

	# the command to calc stuff
	python3 "${SCRIPTS_DIR}/calcGroupCSVstats.py" "${ifn}" "${ofn}"

	COMMAND_EXIT=$?

	if [ $COMMAND_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like calculating stats for ${GROUP} succeeded" 1>&2
	else
		printf "%s\n" "It looks like calculating stats for ${GROUP} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi

done < <(ls -1 "${GROUPS_DIR}"/*.list | grep -v "keep.list")

chmod 444 ${GROUP_STATS_DIR}/*.stats &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like calculating stats for ALL groups succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like calculating stats for" "${FAILED}" "group(s) failed" 1>&2
fi

