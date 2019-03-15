#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
ORIG_GB_DIR="${DATA_DIR}/original_gb"
ORIG_GB_CUSTOM_DIR="${ORIG_GB_DIR}/custom_groups"
ORIG_INC_GRP_DIR="${DATA_DIR}/original_incompatibility_groups"

CMD_EXIT=0

mkdir -p "${ORIG_GB_CUSTOM_DIR}" "${ORIG_INC_GRP_DIR}" &> /dev/null

while read gn
do
	#GROUP=$(basename "${gn}" ".gb")
	ACC_LIST=$(cat "${ORIG_GB_DIR}/${gn}" | tr '\n' ' ' | sed -r 's, $,,')

	curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi" \
		--data-urlencode "db=nuccore" \
		--data-urlencode "rettype=gbwithparts" \
		--data-urlencode "retmode=text" \
		--data-urlencode "id=${ACC_LIST}" \
		-X "POST" \
		--compressed \
		-H "Upgrade-Insecure-Requests: 1" \
		-H "DNT: 1" \
		-H "Connection: keep-alive" \
		-o "${ORIG_GB_DIR}/${gn}"

done < <(find "${ORIG_GB_DIR}" -type f | sed -r 's,'"${ORIG_GB_DIR}"',,')

CMD_EXIT=$?

exit ${CMD_EXIT}

