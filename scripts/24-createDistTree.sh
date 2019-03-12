#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
TREE_DIR="${DATA_DIR}/tree"

#########################
######### MAIN ##########
#########################

rm -f "${TREE_DIR}"/*.newick &> /dev/null

makeNewick.py \
	-i "${TREE_DIR}/dist_matrix.csv" \
	-o "${TREE_DIR}/dist_tree.newick"

CMD_EXIT=$?

chmod 444 "${TREE_DIR}/tree/*.newick" &> /dev/null

exit $CMD_EXIT

#usage: makeNewick.py [-h] -i INPUT [-o OUTPUT] [-p] [-f LARGETREE] [-v]
#
#Make Newick File from Distance Matrix.
#
#optional arguments:
#  -h, --help    show this help message and exit
#  -i INPUT      Input Fasta Files
#  -o OUTPUT     Output File
#  -p            Phylip format
#  -f LARGETREE  Use faster neighbor-joining algorithm
#  -v            Verbose for faster neighbor-joining algorithm
