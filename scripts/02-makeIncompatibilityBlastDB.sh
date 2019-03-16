#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
ORIG_INC_GRP_DIR="${DATA_DIR}/original_incompatibility_groups"
INC_GRP_DIR="${DATA_DIR}/incompatibility_groups"

mkdir -p ${INC_GRP_DIR} &> /dev/null

chmod 644 ${INC_GRP_DIR}/incompatibility.??? &> /dev/null
rm -f ${INC_GRP_DIR}/incompatibility.???

chmod 644 ${INC_GRP_DIR}/makeBlastDB.log &> /dev/null
rm -f ${INC_GRP_DIR}/makeBlastDB.log &> /dev/null

cd ${INC_GRP_DIR}

BLAST_BIN_PATH="${HOME}/software/blast+-2.4.0/c++/build/bin"

time ${BLAST_BIN_PATH}/makeblastdb \
	-dbtype nucl \
	-in  incompatibility.fasta \
	-input_type fasta \
	-title incompatibility \
	-parse_seqids \
	-hash_index \
	-out incompatibility \
	-max_file_sz 2GB \
	-logfile makeBlastDB.log

CMD_EXIT=$?

cd -

chmod 444 ${INC_GRP_DIR}/incompatibility.??? &> /dev/null
chmod 444 ${INC_GRP_DIR}/makeBlastDB.log &> /dev/null

exit ${CMD_EXIT}
