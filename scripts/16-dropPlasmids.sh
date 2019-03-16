#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
PLASMID_MATCHES_DIR="${MAIN_DIR}/data/plasmid_matches"
GROUPS_DIR="${MAIN_DIR}/data/groups"
KEEP_DIR="${GROUPS_DIR}/keep"
DISCARD_DIR="${GROUPS_DIR}/discard"

FAILED=0

mkdir -p ${KEEP_DIR} ${DISCARD_DIR} &> /dev/null
chmod 644 ${KEEP_DIR}/*.list ${DISCARD_DIR}/discard.list &> /dev/null
rm -f ${KEEP_DIR}/*.list ${DISCARD_DIR}/discard.list

while read ifn 
do
	GROUP=`basename "${ifn}" ".list"`
	ofn="${KEEP_DIR}/${GROUP}.list"

	while read ACC
	do
		COUNT=`tail -n 1 "${PLASMID_MATCHES_DIR}/${ACC}_matches-summary.tsv" | cut -d '	' -f 6 | tr -d '"'`
		if [ $COUNT -ge 1 ] && [ $COUNT -le 6 ]
		then
			printf "${ACC}\n" >> "${ofn}"
			printf "${ACC}\n" >> "${KEEP_DIR}/keep.list"
		else
			printf "${ACC}\n" >> "${DISCARD_DIR}/discard.list"
		fi

	done < "${ifn}"

done < <(ls -1 "${GROUPS_DIR}"/*.list)

TMP=/tmp/$$
cat "${DISCARD_DIR}/discard.list" \
	| sort -V \
	| uniq \
	> $TMP
mv "${TMP}" "${DISCARD_DIR}/discard.list"

cat "${KEEP_DIR}/keep.list" \
	| sort -V \
	| uniq \
	> $TMP
mv "${TMP}" "${KEEP_DIR}/keep.list"

chmod 444 ${KEEP_DIR}/*.list ${DISCARD_DIR}/discard.list &> /dev/null

