#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
ORIG_GB_DIR="${MAIN_DIR}/data/original_gb"
PLASMID_GB_DIR="${MAIN_DIR}/data/plasmid_gb"

mkdir -p "${PLASMID_GB_DIR}" &> /dev/null
cd "${PLASMID_GB_DIR}"

chmod 644 "${PLASMID_GB_DIR}"/*.gb &> /dev/null
rm -f "${PLASMID_GB_DIR}"/*.gb

while read ifn 
do
	awk -f "${SCRIPTS_DIR}/splitMultiGB.awk" "${ifn}"

done < <(ls -1 "${ORIG_GB_DIR}"/*.gb)

chmod 644 "${PLASMID_GB_DIR}"/*.gb

cd "${MAIN_DIR}"
