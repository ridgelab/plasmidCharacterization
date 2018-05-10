#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
INCOMP_BLAST_RESULTS_DIR="${MAIN_DIR}/data/incompatibility_groups/blast_results"

cat ${INCOMP_BLAST_RESULTS_DIR}/*_fmt6c.tsv | cut -f 5 > ${INCOMP_BLAST_RESULTS_DIR}/evalues.list
cat ${INCOMP_BLAST_RESULTS_DIR}/*_fmt6c_cov60.tsv | cut -f 5 > ${INCOMP_BLAST_RESULTS_DIR}/evalues_cov60.list

${SCRIPTS_DIR}/eValueHist.R 


