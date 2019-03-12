#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
SOURCE_INFO_FILE="${DATA_DIR}/plasmid_sourceInfo/sourceInfo.tsv"
TREE_DIR="${DATA_DIR}/tree"
ORIG_TREE="${TREE_DIR}/dist_tree.newick"
LABEL_TREE="${TREE_DIR}/dist_tree_labels.newick"

#########################
######### MAIN ##########
#########################

rm -f "${TREE_DIR}"/dist_tree_labels.newick &> /dev/null

python3 "${SCRIPTS_DIR}/modifyLeafLabels.py" \
	"${SOURCE_INFO_FILE}" \
	"${ORIG_TREE}" \
	"${LABEL_TREE}"

CMD_EXIT=$?

chmod 444 "${TREE_DIR}/tree/dist_tree_labels.newick" &> /dev/null

exit $CMD_EXIT

