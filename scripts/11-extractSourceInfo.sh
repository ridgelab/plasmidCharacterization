#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
PLASMID_GB_DIR="${DATA_DIR}/plasmid_gb"
SOURCE_COUNTS_DIR="${DATA_DIR}/plasmid_sourceInfo"

FAILED=0

mkdir -p ${SOURCE_COUNTS_DIR} &> /dev/null
chmod 644 "${SOURCE_COUNTS_DIR}/sourceInfo.tsv" &> /dev/null
rm -f "${SOURCE_COUNTS_DIR}/sourceInfo.tsv" &> /dev/null

printf "%s\t%s\t%s\t%s\t%s\n" \
	'accession' \
	'organism' \
	'isolation_source' \
	'country' \
	'collection_data' \
	> "${SOURCE_COUNTS_DIR}/sourceInfo.tsv"

while read ifn 
do
	ACCESSION=`basename "${ifn}" ".gb"`

	printf '%s\t' "${ACCESSION}" >> "${SOURCE_COUNTS_DIR}/sourceInfo.tsv"

	awk -f "${SCRIPTS_DIR}/snagSourceInfo.awk" \
		"${PLASMID_GB_DIR}/${ACCESSION}.gb" \
		>> "${SOURCE_COUNTS_DIR}/sourceInfo.tsv"

	COMMAND_EXIT=$?

	if [ $COMMAND_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like snagging source info for ${ACCESSION} succeeded" 1>&2
	else
		printf "%s\n" "It looks like snagging source info for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi

done < <(ls -1 "${PLASMID_GB_DIR}"/*.gb)

chmod 444 "${SOURCE_COUNTS_DIR}/sourceInfo.tsv" &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like snagging source info for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like snagging source info for" "${FAILED} " "accession(s) failed" 1>&2
fi

