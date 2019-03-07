#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
PLASMID_FASTA_DIR="${MAIN_DIR}/data/plasmid_fasta"
PLASMID_GB_DIR="${MAIN_DIR}/data/plasmid_gb"
PLASMID_SEARCH_REGIONS_DIR="${MAIN_DIR}/data/plasmid_searchRegions"

FAILED=0

mkdir -p ${PLASMID_SEARCH_REGIONS_DIR} &> /dev/null
chmod 644 ${PLASMID_SEARCH_REGIONS_DIR}/*_searchRegions.{gb,txt} &> /dev/null
rm -f ${PLASMID_SEARCH_REGIONS_DIR}/*_searchRegions.{gb,txt}

while read ifn 
do
	ACCESSION=`basename "${ifn}" ".fasta"`
	python3 ${SCRIPTS_DIR}/extractPlasmidSearchRegions.py \
		"${ACCESSION}" \
		"${PLASMID_SEARCH_REGIONS_DIR}" \
		"${PLASMID_GB_DIR}" \

	COMMAND_EXIT=$?

	if [ $COMMAND_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like extracting search regions for ${ACCESSION} succeeded" 1>&2
		diff -q \
			${PLASMID_GB_DIR}/${ACCESSION}.gb \
			<(cat ${PLASMID_SEARCH_REGIONS_DIR}/${ACCESSION}_searchRegions.gb | sed -r 's/\o033\[0[;1-4]{0,3}m//g')
	else
		printf "%s\n" "It looks like extracting search regions for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi


done < <(ls -1 "${PLASMID_FASTA_DIR}"/*.fasta)

chmod 444 ${PLASMID_SEARCH_REGIONS_DIR}/*_searchRegions.{gb,txt} &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like extracting search regions for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like extracting search regions for" "${FAILED}" "accession(s) failed" 1>&2
fi

