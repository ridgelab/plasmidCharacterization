#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
ORIG_GB_DIR="${MAIN_DIR}/data/original_gb"
GROUP_LISTS_DIR="${MAIN_DIR}/data/groups"

mkdir -p "${GROUP_LISTS_DIR}" &> /dev/null
cd "${GROUP_LISTS_DIR}"

chmod 644 *.list &> /dev/null
rm -f *.list

while read ifn 
do
	awk -f "${SCRIPTS_DIR}/extractGroupLists.awk" "${ifn}"

done < <(ls -1 "${ORIG_GB_DIR}"/*.gb "${ORIG_GB_DIR}"/custom_groups/*.gb 2> /dev/null)

chmod 444 *.list &> /dev/null

cd "${MAIN_DIR}"
