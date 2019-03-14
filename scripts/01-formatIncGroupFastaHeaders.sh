#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
ORIG_INC_GRP_DIR="${DATA_DIR}/original_incompatibility_groups"
INC_GRP_DIR="${DATA_DIR}/incompatibility_groups"

mkdir -p ${INC_GRP_DIR} &> /dev/null
if [ -e ${INC_GRP_DIR}/incompatibility.fasta ]
then
	 chmod 644 ${INC_GRP_DIR}/incompatibility.fasta
	 rm -f ${INC_GRP_DIR}/incompatibility.fasta
fi

time awk -f ${SCRIPTS_DIR}/formatIncGroupFasta.awk \
	${ORIG_INC_GRP_DIR}/incompatibility.fasta \
	> ${INC_GRP_DIR}/incompatibility.fasta

CMD_EXIT=$?

chmod 444 ${INC_GRP_DIR}/incompatibility.fasta

exit ${CMD_EXIT}
