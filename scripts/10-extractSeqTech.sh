#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
PLASMID_GB_DIR="${DATA_DIR}/plasmid_gb"
SEQ_TECH_DIR="${DATA_DIR}/plasmid_seqTech"

FAILED=0

mkdir -p ${SEQ_TECH_DIR} &> /dev/null
chmod 644 "${SEQ_TECH_DIR}/seqTech.tsv" &> /dev/null
rm -f "${SEQ_TECH_DIR}/seqTech.tsv" &> /dev/null

printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
	'accession' \
	'sequencing_technologies' \
	"num_total" \
	"num_short" \
	"num_long" \
	"num_illumina" \
	"num_454" \
	"num_abi" \
	"num_sanger" \
	"num_torrent" \
	"num_pacbio" \
	"num_nanopore" \
	> "${SEQ_TECH_DIR}/seqTech.tsv"

while read ifn 
do
	ACCESSION=`basename "${ifn}" ".gb"`

	printf '%s\t' "${ACCESSION}" >> "${SEQ_TECH_DIR}/seqTech.tsv"

	awk -f "${SCRIPTS_DIR}/sequesterSeqTech.awk" \
		"${PLASMID_GB_DIR}/${ACCESSION}.gb" \
		>> "${SEQ_TECH_DIR}/seqTech.tsv"

	COMMAND_EXIT=$?

	if [ $COMMAND_EXIT -eq 0 ]
	then
		printf "%s\n" "It looks like sequestering sequencing technology for ${ACCESSION} succeeded" 1>&2
	else
		printf "%s\n" "It looks like sequestering sequencing technology for ${ACCESSION} failed" 1>&2
		FAILED=`bc <<< "${FAILED}+1"`
	fi

done < <(ls -1 "${PLASMID_GB_DIR}"/*.gb)

chmod 444 "${SEQ_TECH_DIR}/seqTech.tsv" &> /dev/null

if [ $FAILED -eq 0 ]
then
	printf "%s\n" "It looks like sequestering sequencing technology for ALL accessions succeeded" 1>&2
else
	printf "%s %u %s\n" "It looks like sequestering sequencing technology for" "${FAILED} " "accession(s) failed" 1>&2
fi

