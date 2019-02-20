#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
PLASMID_FASTA_DIR="${DATA_DIR}/plasmid_fasta"
PLASMID_BLAST_RESULTS_DIR="${DATA_DIR}/plasmid_blast_results"

mkdir -p ${PLASMID_BLAST_RESULTS_DIR} &> /dev/null

chmod 644 ${PLASMID_BLAST_RESULTS_DIR}/plasmids.fasta &> /dev/null
rm -f ${PLASMID_BLAST_RESULTS_DIR}/plasmids.fasta

chmod 644 ${PLASMID_BLAST_RESULTS_DIR}/plasmids.??? &> /dev/null
rm -f ${PLASMID_BLAST_RESULTS_DIR}/plasmids.???

chmod 644 ${PLASMID_BLAST_RESULTS_DIR}/makeBlastDB.log &> /dev/null
rm -f ${PLASMID_BLAST_RESULTS_DIR}/makeBlastDB.log &> /dev/null

cd ${PLASMID_BLAST_RESULTS_DIR}

cat "${PLASMID_FASTA_DIR}"/*.fasta > "${PLASMID_BLAST_RESULTS_DIR}/plasmids.fasta"

BLAST_BIN_PATH="${HOME}/software/blast+-2.4.0/c++/build/bin"

time ${BLAST_BIN_PATH}/makeblastdb \
	-dbtype nucl \
	-in  plasmids.fasta \
	-input_type fasta \
	-title plasmids \
	-parse_seqids \
	-hash_index \
	-out plasmids \
	-max_file_sz 2GB \
	-logfile makeBlastDB.log

CMD_EXIT=$?

cd - &> /dev/null

chmod 444 ${PLASMID_BLAST_RESULTS_DIR}/plasmids.fasta &> /dev/null
chmod 444 ${PLASMID_BLAST_RESULTS_DIR}/plasmids.??? &> /dev/null
chmod 444 ${PLASMID_BLAST_RESULTS_DIR}/makeBlastDB.log &> /dev/null

exit ${CMD_EXIT}
