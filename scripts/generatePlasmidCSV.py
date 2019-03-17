
# ========= #
# FUNCTIONS #
# ========= #

def handleArgs():
	import sys

	if len(sys.argv) != 10:
		sys.stderr.write("\n\tERROR: You must provide 8 arguments\n\t\t1- plasmid accession\n\t\t2- output csv dir\n\t\t3- input fasta dir\n\t\t4- input matches dir\n\t\t5- input incompatibility groups blast output dir\n\t\t6- input source info tsv file\n\t\t7- input plasmid blast results dir\n\t\t8- input discarded plasmids list\n\t\t9- input sequence techs tsv\n\n")
		sys.exit(1)
	
	plasmid_accession = sys.argv[1]
	output_csv_dir = sys.argv[2].rstrip('/')
	input_fasta_and_length_dir = sys.argv[3].rstrip('/')
	input_matches_dir = sys.argv[4].rstrip('/')
	input_incompatibility_groups_blast_output_dir = sys.argv[5].rstrip('/')
	input_source_info_fn = sys.argv[6]
	input_blast_results_dir = sys.argv[7].rstrip('/')
	input_discarded_plasmids_fn = sys.argv[8]
	input_sequence_techs_fn = sys.argv[9]

	return plasmid_accession, output_csv_dir, input_fasta_and_length_dir, input_matches_dir, input_incompatibility_groups_blast_output_dir, input_source_info_fn, input_blast_results_dir, input_discarded_plasmids_fn, input_sequence_techs_fn

def CSVify(some_str):
	return '"' + some_str + '"'

def getPlasmidLength(input_length_fn):
	with open(input_length_fn, 'r') as ifd:
		return int(ifd.readline().rstrip('\n'))

def parseMatchesSummaryFile(matches_fn):

	with open(matches_fn, 'r') as mfd:
		mfd.readline() # skip header
		return ','.join(mfd.readline().rstrip('\n').split('\t')[1:])

def getPercentOfTotal(count, total):
	if total:
		return count / total
	else:
		return "NA"

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

def getIdenticalPlasmids(input_identical_plasmids_fn, input_discarded_plsmids_fn):
	discarded_plasmids = []
	with open(input_discarded_plasmids_fn, 'r') as ifd:
		discarded_plasmids = [line.rstrip('\n') for line in ifd]
		
	identical_plasmids = []
	with open(input_identical_plasmids_fn, 'r') as ifd:
		identical_plasmids = [line.rstrip('\n') for line in ifd]
	
	identical_non_discarded_plasmids = ','.join([plasmid for plasmid in identical_plasmids if not plasmid in discarded_plasmids])
	return identical_non_discarded_plasmids if identical_non_discarded_plasmids else "NA"

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
	plasmid_accession, output_csv_dir, input_fasta_and_length_dir, input_matches_dir, input_incompatibility_groups_blast_output_dir, input_source_info_fn, input_blast_results_dir, input_discarded_plasmids_fn, input_sequence_techs_fn = handleArgs()

	# set some helpful vars
	ocn = output_csv_dir + '/' + plasmid_accession + ".csv"
	ifn = input_fasta_and_length_dir + '/' + plasmid_accession + ".fasta"
	iln = input_fasta_and_length_dir + '/' + plasmid_accession + ".length"
	mfn = input_matches_dir + '/' + plasmid_accession + "_matches-summary.tsv"
	iign = input_incompatibility_groups_blast_output_dir + '/' + plasmid_accession + "_families.list"
	isin = input_source_info_fn
	iipn = input_blast_results_dir + '/' + plasmid_accession + "_identicalPlasmids_concordant.list"
	idpn = input_discarded_plasmids_fn
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
	identical_plasmids = getIdenticalPlasmids(iipn,idpn)
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
	cds_info_output_str = parseMatchesSummaryFile(mfn)
	
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

