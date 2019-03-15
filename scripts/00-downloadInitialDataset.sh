#! /bin/bash

# check to make sure this step should actually be run
clear
printf "%s\n" \
	"" \
	"Be advised: this step was not originally part of the pipeline. We downloaded" \
	"the GenBank files as described in our paper (see README). To reduce the barrier" \
	"of reproducibility, we have included this script to ensure you can get the same" \
	"set of input files we downloaded and curated. If you wish to proceed, the" \
	"contents of the data/original_gb and data/original_incompatibility_groups" \
	"directories will be removed. If you do not wish to have those directories" \
	"cleared and populated with the initial data from our analysis, please type \`no'" \
	"at the prompt or hit ^C (ctrl-C) now. Otherwise, type \`yes' at the prompt." \
	"The prompt will not stop seeking input until only either \`no' or \`yes' is" \
	"provided." \
	""

yn=''
while [ "$yn" != "no" ] && [ "$yn" != "yes" ]
do
	printf "%s" "Do you wish to proceed? (yes/no)  "
	read yn
done

printf "\r%s\r%s" \
	"                                       " \
	"You selected \`${yn}'."

if [ "$yn" == "no" ]
then
	printf "%s\n\n" \
		" Cheers!"
	exit 0

elif [ "$yn" == "yes" ]
then
	printf "%s\n" \
		" This is your last chance to exit."
	for i in {5..1}
	do
		printf "\r%u %s" \
			"${i}" \
			"seconds remaining. If you wish to exit, press ^C now."
		sleep 1
	done

	printf "\r%s\r%s\n\n" \
		"                                                       " \
		"Continuing now."

else
	printf "%s\n\n" \
		" This should not be possible. Exiting now."
	exit 1
fi
exit 0

MAIN_DIR="$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)"; cd ${MAIN_DIR}
SCRIPTS_DIR="${MAIN_DIR}/scripts"
DATA_DIR="${MAIN_DIR}/data"
ORIG_GB_DIR="${DATA_DIR}/original_gb"
ORIG_GB_CUSTOM_DIR="${ORIG_GB_DIR}/custom_groups"
ORIG_INC_GRP_DIR="${DATA_DIR}/original_incompatibility_groups"

CMD_EXIT=0

rm -rf "${ORIG_GB_DIR}" "${ORIG_INC_GRP_DIR}" &> /dev/null
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

Eaero_IMP.gb
Eaero_KPC.gb
Eaero_NDM.gb
Eclo_IMP.gb
Eclo_KPC.gb
Eclo_NDM.gb
Eclo_VIM.gb
Ecol_IMP.gb
Ecol_KPC.gb
Ecol_NDM.gb
Kpneu_IMP.gb
Kpneu_KPC.gb
Kpneu_NDM.gb
Kpneu_VIM.gb
Paeru_IMP.gb
Paeru_KPC.gb
Paeru_VIM.gb
Pstu_NDM.gb
Pstu_VIM.gb
S.mar_IMP.gb
S.mar_KPC.gb
S.mar_NDM.gb
S.mar_VIM.gb
custom_groups/E_aerogenes.gb
custom_groups/E_cloacae.gb
custom_groups/E_coli.gb
custom_groups/Enterobacteriaceae.gb
custom_groups/IMP.gb
custom_groups/KPC.gb
custom_groups/K_pneumoniae.gb
custom_groups/NDM.gb
custom_groups/NOT_Enterobacteriaceae.gb
custom_groups/P_aeruginosa.gb
custom_groups/P_stuartii.gb
custom_groups/S_marcescens.gb
custom_groups/VIM.gb
