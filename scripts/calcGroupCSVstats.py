
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

def writeSequencingTechnologies(ofd, all_seq_tech_fields):
	
	output = []
	sizes = []
	
	header1 = ("Sequencing", "Num", "Occurances per", "Percent Total", "Percent Known")
	header2 = ("Technology", "Plasmids", "Plasmid", "Plasmids", "Plasmids")

	output.append(header1)
	sizes.append(tuple(map(len, output[-1])))
	output.append(header2)
	sizes.append(tuple(map(len, output[-1])))

	known_seq_tech_fields = [seq_tech_fields for seq_tech_fields in all_seq_tech_fields if seq_tech_fields[0] != "NA"]
	total_plasmids = len(all_seq_tech_fields)
	known_plasmids = len(known_seq_tech_fields)
	unknown_plasmids = total_plasmids - known_plasmids


	output.append(("Known", str(known_plasmids), "NA", "{0:.3f}".format(known_plasmids / total_plasmids * 100), "{0:.3f}".format(100.0)))
	sizes.append(tuple(map(len, output[-1])))
	output.append(("Unknown", str(unknown_plasmids), "NA", "{0:.3f}".format(unknown_plasmids / total_plasmids * 100), "{0:.3f}".format(0.0)))
	sizes.append(tuple(map(len, output[-1])))

	# convert the numbers from strs to ints
	for i,fields in enumerate(known_seq_tech_fields):
		for j,field in enumerate(fields):
			if j > 0:
				known_seq_tech_fields[i][j] = int(field)

	indices = { "Illumina": 4, "Roche 454": 5, "ABI Solid": 6,
		"Sanger": 7, "Ion Torrent": 8, "PacBio": 9, 
		"ONT": 10, "Short": 2, "Long": 3, "Total": 1}

	if known_plasmids > 0:

		for key in [ "Illumina", "Roche 454", "ABI Solid", "Sanger", "Ion Torrent", "PacBio", "ONT", "Short", "Long" ]:
			counts = [fields[indices[key]] for fields in known_seq_tech_fields]
			count = sum(counts)
			plasmids = sum(list(map(int, map(bool, counts))))

			if plasmids == 0:
				output.append((key, "0", "NA", "{0:.3f}".format(0.0), "{0:.3f}".format(0.0)))
				sizes.append(tuple(map(len, output[-1])))
			else: 
				output.append((key, str(plasmids), "{0:.3f}".format(count / plasmids), "{0:.3f}".format(plasmids / total_plasmids * 100), "{0:.3f}".format(plasmids / known_plasmids * 100)))
				sizes.append(tuple(map(len, output[-1])))

		title = "Multiple Short"
		counts = [fields[indices["Short"]] for fields in known_seq_tech_fields if fields[indices["Short"]] > 1]
		count = sum(counts)
		plasmids = sum(list(map(int, map(bool, counts))))
		if plasmids == 0:
			output.append((title, "0", "NA", "{0:.3f}".format(0.0), "{0:.3f}".format(0.0)))
			sizes.append(tuple(map(len, output[-1])))
		else: 
			output.append((title, str(plasmids), "{0:.3f}".format(count / plasmids), "{0:.3f}".format(plasmids / total_plasmids * 100), "{0:.3f}".format(plasmids / known_plasmids * 100)))
			sizes.append(tuple(map(len, output[-1])))

		title = "Multiple Long"
		counts = [fields[indices["Long"]] for fields in known_seq_tech_fields if fields[indices["Long"]] > 1]
		count = sum(counts)
		plasmids = sum(list(map(int, map(bool, counts))))
		if plasmids == 0:
			output.append((title, "0", "NA", "0.0", "0.0"))
			sizes.append(tuple(map(len, output[-1])))
		else: 
			output.append((title, str(plasmids), "{0:.3f}".format(count / plasmids), "{0:.3f}".format(plasmids / total_plasmids * 100), "{0:.3f}".format(plasmids / known_plasmids * 100)))
			sizes.append(tuple(map(len, output[-1])))

		title = "Short Only"
		counts = [fields[indices["Short"]] for fields in known_seq_tech_fields if fields[indices["Long"]] == 0]
		count = sum(counts)
		plasmids = sum(list(map(int, map(bool, counts))))
		if plasmids == 0:
			output.append((title, "0", "NA", "0.0", "0.0"))
			sizes.append(tuple(map(len, output[-1])))
		else: 
			output.append((title, str(plasmids), "{0:.3f}".format(count / plasmids), "{0:.3f}".format(plasmids / total_plasmids * 100), "{0:.3f}".format(plasmids / known_plasmids * 100)))
			sizes.append(tuple(map(len, output[-1])))

		title = "Long Only"
		counts = [fields[indices["Long"]] for fields in known_seq_tech_fields if fields[indices["Short"]] == 0]
		count = sum(counts)
		plasmids = sum(list(map(int, map(bool, counts))))
		if plasmids == 0:
			output.append((title, "0", "NA", "0.0", "0.0"))
			sizes.append(tuple(map(len, output[-1])))
		else: 
			output.append((title, str(plasmids), "{0:.3f}".format(count / plasmids), "{0:.3f}".format(plasmids / total_plasmids * 100), "{0:.3f}".format(plasmids / known_plasmids * 100)))
			sizes.append(tuple(map(len, output[-1])))

		title = "Short & Long"
		counts = [ fields[indices["Total"]] for fields in known_seq_tech_fields if fields[indices["Short"]] > 0 and fields[indices["Long"]] > 0 ]
		count = sum(counts)
		plasmids = sum(list(map(int, map(bool, counts))))
		if plasmids == 0:
			output.append((title, "0", "NA", "0.0", "0.0"))
			sizes.append(tuple(map(len, output[-1])))
		else: 
			output.append((title, str(plasmids), "{0:.3f}".format(count / plasmids), "{0:.3f}".format(plasmids / total_plasmids * 100), "{0:.3f}".format(plasmids / known_plasmids * 100)))
			sizes.append(tuple(map(len, output[-1])))

		c0 = 0
		c1 = 0
		c2 = 0
		c3 = 0
		c4 = 0
		for size in sizes:
			if size[0] > c0:
				c0 = size[0]
			if size[1] > c1:
				c1 = size[1]
			if size[2] > c2:
				c2 = size[2]
			if size[3] > c3:
				c3 = size[3]
			if size[4] > c4:
				c4 = size[4]
		
		ofd.write("Sequencing Technologies:\n")
		for o,s in zip(output,sizes):
			ofd.write('\t')
			ofd.write(o[0] + ' ' * (c0 - s[0] + 3))
			ofd.write(o[1] + ' ' * (c1 - s[1] + 3))
			ofd.write(o[2] + ' ' * (c2 - s[2] + 3))
			ofd.write(o[3] + ' ' * (c3 - s[3] + 3))
			ofd.write(o[4] + ' ' * (c4 - s[4] + 3))
			ofd.write('\n')
	else:
		ofd.write("Sequencing Technologies: uknown\n")


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
			all_seq_tech_fields = []

			# loop through each plasmid_record (line) in the input file
			for plasmid_record in ifd:
				# increment the total num of plasmids (one plasmid exists per line)
				total_number_of_plasmids += 1

				# split the record into its 44 separate columns/fields
				fields = plasmid_record.rstrip('\n').rstrip('"').lstrip('"').split("\",\"")

				plasmid_accession = fields[0].strip('"')
				seq_tech_fields = list(map(lambda field: field.strip('"'), fields[6:17]))
				plasmid_length = int(fields[17].strip('"'))
				inc_groups = fields[44].strip('"').split(',')
				group_structure_fields = tuple(map(lambda field: int(field.strip('"')), (fields[17], fields[18], fields[20], fields[26], fields[28], fields[31], fields[37], fields[39], fields[41])))

				# capture length information
				plasmid_lengths.append(plasmid_length)

				# capture info about inc groups
				for inc_group in inc_groups:
					if inc_group not in all_inc_groups:
						all_inc_groups[inc_group] = []
					all_inc_groups[inc_group].append(plasmid_length)

				# capture info about group structure
				all_group_structure_fields.append(group_structure_fields)

				# capture info about sequencing technologies
				all_seq_tech_fields.append(seq_tech_fields)


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

		#	Sequencing Technologies
		writeSequencingTechnologies(ofd, all_seq_tech_fields)
		ofd.write('\n') # extra newline


# 00 "Accession #"
# 01 "Identical Plasmids"
# 02 "Source: Organism"
# 03 "Source: Isolation Source"
# 04 "Source: Country"
# 05 "Source: Collection Date"
# 06 "Sequencing Technologies"
# 07 "Sequencing Technologies Count"
# 08 "Short Read Count"
# 09 "Long Read Count"
# 10 "Illumina Count"
# 11 "Roche 454 Count"
# 12 "ABI Solid Count"
# 13 "Sanger Count"
# 14 "Ion Torrent Count"
# 15 "PacBio Count"
# 16 "ONT Count"
# 17 "Plasmid Length"
# 18 "Antimicrobial Resistance CDS"
# 19 "Antimicrobial Resistance CDS %"
# 20 "Beta-lactimase CDS"
# 21 "Beta-lactimase CDS %"
# 22 "Beta-lactimase Special (Carbapenem*,IMP,KPC,NDM,VIM) Copy #"
# 23 "Beta-lactimase Special (Carbapenem*,IMP,KPC,NDM,VIM) Copy # % of Beta-lactimase"
# 24 "Beta-lactimase Special (Carbapenem*,IMP,KPC,NDM,VIM) Copy # % of Total"
# 25 "Beta-lactimase Special (Carbapenem*,IMP,KPC,NDM,VIM) Absent (Yes/No)"
# 26 "Plasmid Transfer CDS"
# 27 "Plasmid Transfer CDS %"
# 28 "Toxin/Antitoxin System CDS"
# 29 "Toxin/Antitoxin System CDS %"
# 30 "Toxin/Antitoxin System Present (Yes/No)"
# 31 "DNA Maintenance/Modification CDS"
# 32 "DNA Maintenance/Modification CDS %"
# 33 "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Copy #"
# 34 "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Copy # % of DNA Maintenance/Modifcation"
# 35 "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Copy # % of Total"
# 36 "DNA Maintenance/Modification Special (mucA,mucB,polymerase,umuC,umuD) Present (Yes/No)"
# 37 "Mobile Genetic Elements CDS"
# 38 "Mobile Genetic Elements CDS %"
# 39 "Hypothetical Genes CDS"
# 40 "Hypothetical Genes CDS %"
# 41 "Other CDS"
# 42 "Other CDS %"
# 43 "Total CDS"
# 44 "Incompatibility Groups"

