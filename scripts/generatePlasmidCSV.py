
# ========= #
# FUNCTIONS #
# ========= #

def handleArgs():
	import sys

	if len(sys.argv) != 9:
		sys.stderr.write("\n\tERROR: You must provide 8 arguments\n\t\t1- plasmid accession\n\t\t2- output csv dir\n\t\t3- input fasta dir\n\t\t4- input matches dir\n\t\t5- input incompatibility groups blast output dir\n\t\t6- input source info tsv file\n\t\t7- input plasmid blast results dir\n\t\t8- input sequence techs tsv\n\n")
		sys.exit(1)
	
	plasmid_accession = sys.argv[1]
	output_csv_dir = sys.argv[2].rstrip('/')
	input_fasta_and_length_dir = sys.argv[3].rstrip('/')
	input_matches_dir = sys.argv[4].rstrip('/')
	input_incompatibility_groups_blast_output_dir = sys.argv[5].rstrip('/')
	input_source_info_fn = sys.argv[6]
	input_blast_results_dir = sys.argv[7].rstrip('/')
	input_sequence_techs_fn = sys.argv[8]

	return plasmid_accession, output_csv_dir, input_fasta_and_length_dir, input_matches_dir, input_incompatibility_groups_blast_output_dir, input_source_info_fn, input_blast_results_dir, input_sequence_techs_fn

def CSVify(some_str):
	return '"' + some_str + '"'

def getPlasmidLength(input_length_fn):
	with open(input_length_fn, 'r') as ifd:
		return int(ifd.readline().rstrip('\n'))

def getRegionCounts(categories):
	cats = [ "Antimicrobial Resistance", "Beta-lactamase", "Beta-lactamase Special", 
		"Plasmid Transfer", "Toxin System", "DNA Maintenance", 
		"DNA Maintenance Special", "Mobile Genetic Elements", "Hypothetical Genes", "Other" ]
	
	counts = [0] * len(cats)

	category_counts = {}

	for category in sorted(categories):
		if not category in category_counts:
			category_counts[category] = 0
		category_counts[category] += 1
	
	for i,cat in enumerate(cats):
		counts[i] = category_counts[cat] if cat in category_counts else 0

	return counts


def updateCDScounts(cds_counts, cds_region_counts):
	for i,cds_region_count in enumerate(cds_region_counts):
		cds_counts[i] += cds_region_count
	
	return cds_counts

def parseMatchesFile(matches_fn):
	import re

	with open(matches_fn, 'r') as ifd:
		cds_counts = [0] * 10 # 10 CDS related columns in output

		# skip past the TSV header line
		ifd.readline()

		# grab first data line
		line = ifd.readline()
	
		while line != "":
			fields = line.rstrip('\n').split('\t')

			ignore = True if fields[0] == "True" else False
			categories = fields[1].split(',')
			key_term = fields[2]
			cds_search_region = fields[3]

			if not ignore:
				cds_counts = updateCDScounts(cds_counts, getRegionCounts(categories) )
		
			# grab the next line
			line = ifd.readline()
			tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]

		return cds_counts

def getPercentOfTotal(count, total):
	if total:
		return count / total
	else:
		return "NA"

def convertCdsInfoToOutputStr(antimicrob_resist_cds_count, beta_lact_cds_count, beta_lact_special_copy_num, plasmid_transfer_cds_count, \
		toxin_cds_count, dna_maint_cds_count, dna_maint_special_copy_num, mobile_genetic_elements_cds_count, \
		hypothetical_genes_cds_count, other_cds_count):
	
	# initialize output list (will eventually become a giant string). Each item will need to be easily converted to a string using str.
	output = []

	# find the total num of cds regions
	total_cds_count = sum((antimicrob_resist_cds_count, plasmid_transfer_cds_count, toxin_cds_count, \
		dna_maint_cds_count, mobile_genetic_elements_cds_count, hypothetical_genes_cds_count, other_cds_count))

	# append columns to output

	#	antimicrob resist (w/ beta lact)
	#		antimicrob resist
	output.append(antimicrob_resist_cds_count) # count
	output.append(getPercentOfTotal(antimicrob_resist_cds_count, total_cds_count)) # percent of total
	#		beta lact
	output.append(beta_lact_cds_count) # count
	output.append(getPercentOfTotal(beta_lact_cds_count, total_cds_count)) # percent of total
	#			special copy num
	output.append(beta_lact_special_copy_num) # count
	output.append(getPercentOfTotal(beta_lact_special_copy_num, beta_lact_cds_count)) # percent of beta lact
	output.append(getPercentOfTotal(beta_lact_special_copy_num, total_cds_count)) # percent of total
	output.append("No" if beta_lact_special_copy_num else "Yes") # absent (Yes/No)

	#	plasmid transfer
	output.append(plasmid_transfer_cds_count) # count
	output.append(getPercentOfTotal(plasmid_transfer_cds_count, total_cds_count)) # percent of total

	#	toxin system
	output.append(toxin_cds_count) # count
	output.append(getPercentOfTotal(toxin_cds_count, total_cds_count)) # percent of total
	output.append("Yes" if toxin_cds_count else "No") # present (Yes/No)

	#	dna maint
	output.append(dna_maint_cds_count) # count
	output.append(getPercentOfTotal(dna_maint_cds_count, total_cds_count)) # percent of total
	#		special copy num
	output.append(dna_maint_special_copy_num) # count
	output.append(getPercentOfTotal(dna_maint_special_copy_num, dna_maint_cds_count)) # percent of dna maint
	output.append(getPercentOfTotal(dna_maint_special_copy_num, total_cds_count)) # percent of total
	output.append("Yes" if dna_maint_special_copy_num else "No") # present (Yes/No)

	#	mobile genetic elements
	output.append(mobile_genetic_elements_cds_count) # count
	output.append(getPercentOfTotal(mobile_genetic_elements_cds_count, total_cds_count)) # percent of total

	#	hypothetical genes
	output.append(hypothetical_genes_cds_count) # count
	output.append(getPercentOfTotal(hypothetical_genes_cds_count, total_cds_count)) # percent of total

	#	other (/unknown)
	output.append(other_cds_count) # count
	output.append(getPercentOfTotal(other_cds_count, total_cds_count)) # percent of total

	#	total
	output.append(total_cds_count) # count

	# convert all elements to str, join by ",", and add leading and trailing "
	output = CSVify("\",\"".join(list(map(str, output))))

	# return
	return output

def getIncompatibilityGroups(input_incompatibility_groups_fn):
	with open(input_incompatibility_groups_fn, 'r') as ifd:
		return [line.rstrip('\n') for line in ifd]

def extractSourceInfo(input_source_info_fn, accession):
	with open(input_source_info_fn, 'r') as ifd:
		for line in ifd:
			fields = line.rstrip('\n').split('\t')
			acc_num = fields[0]
			organism = fields[1]
			isolation_source = fields[2]
			country = fields[3]
			collection_date = fields[4]
			if acc_num == accession:
				return organism, isolation_source, country, collection_date

def getIdenticalPlasmids(input_identical_plasmids_fn):
	identical_plasmids = ''
	with open(input_identical_plasmids_fn, 'r') as ifd:
		identical_plasmids = ifd.read().rstrip('\n').replace('\n', ',')
	
	return identical_plasmids if identical_plasmids else "NA"

def extractSeqTechInfo(input_sequencing_technology_fn, plasmid_accession):
	with open(input_sequencing_technology_fn, 'r') as ifd:
		for line in ifd:
			fields = line.rstrip('\n').split('\t')
			if fields[0] == plasmid_accession:
				return fields[1:]


# ==== #
# MAIN #
# ==== #

if __name__ == "__main__":

	import sys
	
	# handle args
	plasmid_accession, output_csv_dir, input_fasta_and_length_dir, input_matches_dir, input_incompatibility_groups_blast_output_dir, input_source_info_fn, input_blast_results_dir, input_sequence_techs_fn = handleArgs()

	# set some helpful vars
	ocn = output_csv_dir + '/' + plasmid_accession + ".csv"
	ifn = input_fasta_and_length_dir + '/' + plasmid_accession + ".fasta"
	iln = input_fasta_and_length_dir + '/' + plasmid_accession + ".length"
	mfn = input_matches_dir + '/' + plasmid_accession + "_matches.tsv"
	iign = input_incompatibility_groups_blast_output_dir + '/' + plasmid_accession + "_families.list"
	isin = input_source_info_fn
	iipn = input_blast_results_dir + '/' + plasmid_accession + "_identicalPlasmids.list"
	istn = input_sequence_techs_fn

	csv_header = [ "Accession #", 
		"Identical Plasmids", 
		"Source: Organism", "Source: Isolation Source", "Source: Country", "Source: Collection Date", 
		"Sequencing Technologies", "Sequencing Technologies Count", "Short Read Count", "Long Read Count", "Illumina Count", "Roche 454 Count", "ABI Solid Count", "Sanger Count", "Ion Torrent Count", "PacBio Count", "ONT Count", 
		"Plasmid Length", 
		"Antimicrobial Resistance CDS", "Antimicrobial Resistance CDS %", 
		"Beta-lactamase CDS","Beta-lactamase CDS %", "Beta-lactamase Special (Carbapenem*,IMP,KPC,NDM,VIM) Copy #", "Beta-lactamase Special (Carbapenem*,IMP,KPC,NDM,VIM) Copy # % of Beta-lactamase", "Beta-lactamase Special (Carbapenem*,IMP,KPC,NDM,VIM) Copy # % of Total", "Beta-lactamase Special (Carbapenem*,IMP,KPC,NDM,VIM) Absent (Yes/No)", 
		"Plasmid Transfer CDS", "Plasmid Transfer CDS %", 
		"Toxin/Antitoxin System CDS", "Toxin/Antitoxin System CDS %", "Toxin/Antitoxin System Present (Yes/No)", 
		"DNA Maintenance/Modification CDS", "DNA Maintenance/Modification CDS %", "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Copy #", "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Copy # % of DNA Maintenance/Modification", "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Copy # % of Total", "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Present (Yes/No)", 
		"Mobile Genetic Elements CDS", "Mobile Genetic Elements CDS %",
		"Hypothetical Genes CDS", "Hypothetical Genes CDS %", 
		"Other CDS", "Other CDS %", 
		"Total CDS", 
		"Incompatibility Groups" ]

	# get necessary information
	#	get CSV Header
	csv_header_output_str = CSVify("\",\"".join(csv_header))
	
	#	get plasmid accession #
	plasmid_accession_output_str = CSVify(plasmid_accession)

	#	get identical plasmid accession #s
	identical_plasmids = getIdenticalPlasmids(iipn)
	identical_plasmids_output_str = CSVify(identical_plasmids)

	#	get source info
	organism, isolation_source, country, collection_data = extractSourceInfo(isin, plasmid_accession)
	source_info_output_str = '"' + organism + '","' + isolation_source + '","' + country + '","' + collection_data + '"'

	#	get seq. tech. info
	seq_tech_cols = extractSeqTechInfo(istn, plasmid_accession)
	seq_tech_output_str = CSVify('","'.join(seq_tech_cols))

	#	get plasmid length
	plasmid_length = getPlasmidLength(iln)
	plasmid_length_output_str = CSVify(str(plasmid_length))

	# 	get CDS info (Antimicrobial Resistance CDS (%) ... Total CDS)
	cds_info = parseMatchesFile(mfn)
	cds_info_output_str = convertCdsInfoToOutputStr(*cds_info)
	
	#	get incompatibility groups
	incompatibility_groups = getIncompatibilityGroups(iign)
	incompatibility_groups_output_str = CSVify(','.join(incompatibility_groups)) if len(incompatibility_groups) > 0 else CSVify("NA")

	# write output
	with open (ocn, 'w') as ocd:
		# csv header line
		ocd.write(csv_header_output_str + '\n') # csv header

		# csv data line
		ocd.write(plasmid_accession_output_str + ',') # accession #
		ocd.write(identical_plasmids_output_str + ',') # identical plasmids
		ocd.write(source_info_output_str + ',') # source info
		ocd.write(seq_tech_output_str + ',') # sequencing technologies
		ocd.write(plasmid_length_output_str + ',') # plasmid length
		ocd.write(cds_info_output_str + ',') # CDS info (Antimicrobial Resistance CDS (%) ... Total CDS)
		ocd.write(incompatibility_groups_output_str + '\n') # incompatibility groups

	# exit
	sys.exit(0)

