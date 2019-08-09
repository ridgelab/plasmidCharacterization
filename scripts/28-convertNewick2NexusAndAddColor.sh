#! /bin/bash

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
TREE_DIR="${DATA_DIR}/tree"
NEXUS_FN="${TREE_DIR}/dist_tree_labels_colors.nexus"
COLORS_FN="data/colors.tsv"
NEWICK_FN="${TREE_DIR}/dist_tree_labels.newick"
GROUPS_FNS=(data/groups/keep/{IMP,KPC,NDM,VIM}.list)

#########################
######### MAIN ##########
#########################

rm -f "${NEXUS_FN}" &> /dev/null

time python3 "${SCRIPTS_DIR}/convertNewick2NexusAndAddColor.py" \
	"${NEXUS_FN}" \
	"${COLORS_FN}" \
	"${NEWICK_FN}" \
	"${GROUPS_FNS[@]}"

CMD_EXIT=$?

chmod 444 "${NEXUS_FN}" &> /dev/null

exit $CMD_EXIT

