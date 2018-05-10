
#############
# FUNCTIONS #
#############

def handleArgs(args, sefd, sexit):
	if len(args) != 3:
		sefd.write("\n\tERROR: Incorrect arguments\n\t\t1- input group csv file\n\t\t2- output text file\n\n")
		sexit(1)
	
	ifn = sys.argv[1]
	ofn = sys.argv[2]

	return ifn, ofn

def writeIncGroupsStructure(ofd, inc_groups):
	
	output = []
	sizes = []
	
	header1 = ("Inc.", "Plasmid", "Size", "Size")
	header2 = ("Group", "Count", "Mean", "St. Dev.")

	output.append(header1)
	sizes.append(tuple(map(len, output[-1])))
	output.append(header2)
	sizes.append(tuple(map(len, output[-1])))

	for inc_group in sorted(inc_groups.keys()):
		if inc_group != "NA":
			lengths = inc_groups[inc_group]
			count = len(lengths)
			mean = count
			st_dev = 0
			if count > 1:
				mean = stats.mean(lengths)
				st_dev = stats.stdev(lengths)
			output.append((inc_group, str(count), "{0:.3f}".format(mean), "{0:.3f}".format(st_dev)))
			sizes.append(tuple(map(len, output[-1])))
	
	c0 = 0
	c1 = 0
	c2 = 0
	c3 = 0
	for size in sizes:
		if size[0] > c0:
			c0 = size[0]
		if size[1] > c1:
			c1 = size[1]
		if size[2] > c2:
			c2 = size[2]
		if size[3] > c3:
			c3 = size[3]
	
	ofd.write("Incompatibility Groups Structure:\n")
	for o,s in zip(output,sizes):
		ofd.write('\t')
		ofd.write(o[0] + ' ' * (c0 - s[0] + 3))
		ofd.write(o[1] + ' ' * (c1 - s[1] + 3))
		ofd.write(o[2] + ' ' * (c2 - s[2] + 3))
		ofd.write(o[3] + ' ' * (c3 - s[3] + 3))
		ofd.write('\n')

def getGroupStructureMeanStr(lengths):
	if len(lengths) > 0:
		return "{0:.3f}".format(stats.mean(lengths))
	else:
		return "NA"

def getGroupStructureStDevStr(lengths):
	if len(lengths) > 1:
		return "{0:.3f}".format(stats.stdev(lengths))
	elif len(lengths) < 1: # == 0
		return "NA"
	else: # == 1
		return str(lengths[0])

def writeGroupStructure(ofd, all_group_structure_fields):

	# set up the group structure arrays (to be populated with plasmid lengths)
	anti_microb_resist = []
	anti_microb_resist_not = []
	beta_lact = []
	beta_lact_not = []
	plasmid_transfer = []
	plasmid_transfer_not = []
	toxin = []
	toxin_not = []
	dna_maint = []
	dna_maint_not = []
	mob_gen_elem = []
	mob_gen_elem_not = []
	hypo_genes = []
	hypo_genes_not = []
	other = []
	other_not = []

	# extract the information and load it into the group structure arrays
	for group_structure_fields in all_group_structure_fields:
		# if three is a count, add it. else add it to the not. We're adding the length.
		length = group_structure_fields[0]
		anti_microb_resist_count = group_structure_fields[1]
		beta_lact_count = group_structure_fields[2]
		plasmid_transfer_count = group_structure_fields[3]
		toxin_count = group_structure_fields[4]
		dna_maint_count = group_structure_fields[5]
		mob_gen_elem_count = group_structure_fields[6]
		hypo_genes_count = group_structure_fields[7]
		other_count = group_structure_fields[8]

		if anti_microb_resist_count:
			anti_microb_resist.append(length)
		else:
			anti_microb_resist_not.append(length)
		if beta_lact_count:
			beta_lact.append(length)
		else:
			beta_lact_not.append(length)
		if plasmid_transfer_count:
			plasmid_transfer.append(length)
		else:
			plasmid_transfer_not.append(length)
		if toxin_count:
			toxin.append(length)
		else:
			toxin_not.append(length)
		if dna_maint_count:
			dna_maint.append(length)
		else:
			dna_maint_not.append(length)
		if mob_gen_elem_count:
			mob_gen_elem.append(length)
		else:
			mob_gen_elem_not.append(length)
		if hypo_genes_count:
			hypo_genes.append(length)
		else:
			hypo_genes_not.append(length)
		if other_count:
			other.append(length)
		else:
			other_not.append(length)

	# for each of the arrays, calc mean & st. dev., write to file

	#	calc
	anti_microb_resist_mean_str = getGroupStructureMeanStr(anti_microb_resist)
	anti_microb_resist_stdev_str = getGroupStructureStDevStr(anti_microb_resist)
	anti_microb_resist_not_mean_str = getGroupStructureMeanStr(anti_microb_resist_not)
	anti_microb_resist_not_stdev_str = getGroupStructureStDevStr(anti_microb_resist_not)
	beta_lact_mean_str = getGroupStructureMeanStr(beta_lact)
	beta_lact_stdev_str = getGroupStructureStDevStr(beta_lact)
	beta_lact_not_mean_str = getGroupStructureMeanStr(beta_lact_not)
	beta_lact_not_stdev_str = getGroupStructureStDevStr(beta_lact_not)
	plasmid_transfer_mean_str = getGroupStructureMeanStr(plasmid_transfer)
	plasmid_transfer_stdev_str = getGroupStructureStDevStr(plasmid_transfer)
	plasmid_transfer_not_mean_str = getGroupStructureMeanStr(plasmid_transfer_not)
	plasmid_transfer_not_stdev_str = getGroupStructureStDevStr(plasmid_transfer_not)
	toxin_mean_str = getGroupStructureMeanStr(toxin)
	toxin_stdev_str = getGroupStructureStDevStr(toxin)
	toxin_not_mean_str = getGroupStructureMeanStr(toxin_not)
	toxin_not_stdev_str = getGroupStructureStDevStr(toxin_not)
	dna_maint_mean_str = getGroupStructureMeanStr(dna_maint)
	dna_maint_stdev_str = getGroupStructureStDevStr(dna_maint)
	dna_maint_not_mean_str = getGroupStructureMeanStr(dna_maint_not)
	dna_maint_not_stdev_str = getGroupStructureStDevStr(dna_maint_not)
	mob_gen_elem_mean_str = getGroupStructureMeanStr(mob_gen_elem)
	mob_gen_elem_stdev_str = getGroupStructureStDevStr(mob_gen_elem)
	mob_gen_elem_not_mean_str = getGroupStructureMeanStr(mob_gen_elem_not)
	mob_gen_elem_not_stdev_str = getGroupStructureStDevStr(mob_gen_elem_not)
	hypo_genes_mean_str = getGroupStructureMeanStr(hypo_genes)
	hypo_genes_stdev_str = getGroupStructureStDevStr(hypo_genes)
	hypo_genes_not_mean_str = getGroupStructureMeanStr(hypo_genes_not)
	hypo_genes_not_stdev_str = getGroupStructureStDevStr(hypo_genes_not)
	other_mean_str = getGroupStructureMeanStr(other)
	other_stdev_str = getGroupStructureStDevStr(other)
	other_not_mean_str = getGroupStructureMeanStr(other_not)
	other_not_stdev_str = getGroupStructureStDevStr(other_not)

	#	write to file
	ofd.write("Key Words Structure:\n")

	#		create columned output
	output = []
	sizes = []

	header1 = ("Key", "Plasmid", "Size", "Size")
	header2 = ("Word", "Count", "Mean", "St. Dev.")
	output.append(header1)
	output.append(header2)
	
	output.append( ( "anti_microb_resist", str(len(anti_microb_resist)), anti_microb_resist_mean_str, anti_microb_resist_stdev_str ) )
	output.append( ( "anti_microb_resist_not", str(len(anti_microb_resist_not)), anti_microb_resist_not_mean_str, anti_microb_resist_not_stdev_str ) )
	output.append( ( "beta_lact", str(len(beta_lact)), beta_lact_mean_str, beta_lact_stdev_str ) )
	output.append( ( "beta_lact_not", str(len(beta_lact_not)), beta_lact_not_mean_str, beta_lact_not_stdev_str ) )
	output.append( ( "plasmid_transfer", str(len(plasmid_transfer)), plasmid_transfer_mean_str, plasmid_transfer_stdev_str ) )
	output.append( ( "plasmid_transfer_not", str(len(plasmid_transfer_not)), plasmid_transfer_not_mean_str, plasmid_transfer_not_stdev_str ) )
	output.append( ( "toxin", str(len(toxin)), toxin_mean_str, toxin_stdev_str ) )
	output.append( ( "toxin_not", str(len(toxin_not)), toxin_not_mean_str, toxin_not_stdev_str ) )
	output.append( ( "dna_maint", str(len(dna_maint)), dna_maint_mean_str, dna_maint_stdev_str ) )
	output.append( ( "dna_maint_not", str(len(dna_maint_not)), dna_maint_not_mean_str, dna_maint_not_stdev_str ) )
	output.append( ( "mob_gen_elem", str(len(mob_gen_elem)), mob_gen_elem_mean_str, mob_gen_elem_stdev_str ) )
	output.append( ( "mob_gen_elem_not", str(len(mob_gen_elem_not)), mob_gen_elem_not_mean_str, mob_gen_elem_not_stdev_str ) )
	output.append( ( "hypo_genes", str(len(hypo_genes)), hypo_genes_mean_str, hypo_genes_stdev_str ) )
	output.append( ( "hypo_genes_not", str(len(hypo_genes_not)), hypo_genes_not_mean_str, hypo_genes_not_stdev_str ) )
	output.append( ( "other", str(len(other)), other_mean_str, other_stdev_str ) )
	output.append( ( "other_not", str(len(other_not)), other_not_mean_str, other_not_stdev_str ) )

	for o in output:
		sizes.append( tuple(map(len, o)))

	c0 = 0
	c1 = 0
	c2 = 0
	c3 = 0
	for size in sizes:
		if size[0] > c0:
			c0 = size[0]
		if size[1] > c1:
			c1 = size[1]
		if size[2] > c2:
			c2 = size[2]
		if size[3] > c3:
			c3 = size[3]

	#		actually write to file
	for o,s in zip(output,sizes):
		ofd.write('\t')
		ofd.write(o[0] + ' ' * (c0 - s[0] + 3))
		ofd.write(o[1] + ' ' * (c1 - s[1] + 3))
		ofd.write(o[2] + ' ' * (c2 - s[2] + 3))
		ofd.write(o[3] + ' ' * (c3 - s[3] + 3))
		ofd.write('\n')

########
# MAIN #
########
if __name__ == "__main__":

	import sys
	import statistics as stats
		
	ifn, ofn = handleArgs(sys.argv, sys.stderr, sys.exit)

	group_name = '.'.join(ifn.strip().split('/')[-1].split('.')[:-1])

	with open(ofn, 'w') as ofd:

		# write the groupname title to the output
		ofd.write(group_name + '\n' + '=' * len(group_name) + '\n')

		# parse the input file and extract necessary information
		with open(ifn, 'r') as ifd:

			# skip past header line
			ifd.readline()

			# set some handy vars
			total_number_of_plasmids = 0
			plasmid_lengths = []
			all_inc_groups = {}
			all_group_structure_fields = []

			# loop through each plasmid_record (line) in the input file
			for plasmid_record in ifd:
				# increment the total num of plasmids (one plasmid exists per line)
				total_number_of_plasmids += 1

				# split the record into its 28 separate columns/fields
				fields = plasmid_record.rstrip('\n').rstrip('"').lstrip('"').split("\",\"")

				plasmid_accession = fields[0].strip('"')
				plasmid_length = int(fields[1].strip('"'))
				inc_groups = fields[28].strip('"').split(',')
				group_structure_fields = tuple(map(lambda field: int(field.strip('"')), (fields[1], fields[2], fields[4], fields[10], fields[12], fields[15], fields[21], fields[23], fields[25])))

				# capture length information
				plasmid_lengths.append(plasmid_length)

				# capture info about inc groups
				for inc_group in inc_groups:
					if inc_group not in all_inc_groups:
						all_inc_groups[inc_group] = []
					all_inc_groups[inc_group].append(plasmid_length)

				# capture info about group structure
				all_group_structure_fields.append(group_structure_fields)


		# write stuff to the output file
		#	total number of plasmids
		ofd.write("Total # of Plasmids: " + str(total_number_of_plasmids) + '\n')
		ofd.write('\n') # extra newline

		#	inc groups structure
		writeIncGroupsStructure(ofd, all_inc_groups)
		ofd.write('\n') # extra newline

		#	group plasmids size
		ofd.write("Plasmids Summary:\n")
		ofd.write("\t     Min: " + str(min(plasmid_lengths)) + '\n')
		ofd.write("\t     Max: " + str(max(plasmid_lengths)) + '\n')
		ofd.write("\t  Median: " + str(stats.median(plasmid_lengths)) + '\n')
		ofd.write("\t    Mean: " + "{0:.3f}".format(stats.mean(plasmid_lengths)) + '\n')
		ofd.write("\tSt. Dev.: " + "{0:.3f}\n".format(stats.stdev(plasmid_lengths)) if len(plasmid_lengths) > 1 else '0' + '\n')
		ofd.write('\n') # extra newline

		#	group structure
		writeGroupStructure(ofd, all_group_structure_fields)
		ofd.write('\n') # extra newline

		#	plasmid structure
		ofd.write("Plasmid Structure:\n")
		ofd.write("\tThis information is already reported in the CSV file: " + ifn.split('/')[-1] + '\n')
		ofd.write('\n') # extra newline




# 00 "Accession #"
# 01 "Plasmid Length"
# 02 "Antimicrobial Resistance CDS"
# 03 "Antimicrobial Resistance CDS %"
# 04 "Beta-lactimase CDS"
# 05 "Beta-lactimase CDS %"
# 06 "Beta-lactimase Special (Carbapenem*,IMP,KPC,NDM,VIM) Copy #"
# 07 "Beta-lactimase Special (Carbapenem*,IMP,KPC,NDM,VIM) Copy # % of Beta-lactimase"
# 08 "Beta-lactimase Special (Carbapenem*,IMP,KPC,NDM,VIM) Copy # % of Total"
# 09 "Beta-lactimase Special (Carbapenem*,IMP,KPC,NDM,VIM) Absent (Yes/No)"
# 10 "Plasmid Transfer CDS"
# 11 "Plasmid Transfer CDS %"
# 12 "Toxin/Antitoxin System CDS"
# 13 "Toxin/Antitoxin System CDS %"
# 14 "Toxin/Antitoxin System Present (Yes/No)"
# 15 "DNA Maintenance/Modification CDS"
# 16 "DNA Maintenance/Modification CDS %"
# 17 "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Copy #"
# 18 "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Copy # % of DNA Maintenance/Modifcation"
# 19 "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Copy # % of Total"
# 20 "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Present (Yes/No)"
# 21 "Mobile Genetic Elements CDS"
# 22 "Mobile Genetic Elements CDS %"
# 23 "Hypothetical Genes CDS"
# 24 "Hypothetical Genes CDS %"
# 25 "Other CDS"
# 26 "Other CDS %"
# 27 "Total CDS"
# 28 "Incompatibility Groups"

