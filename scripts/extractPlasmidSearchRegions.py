
# ========= #
# FUNCTIONS #
# ========= #

def handleArgs():
	import sys

	if len(sys.argv) != 4:
		sys.stderr.write("\n\tERROR: You must provide 3 arguments\n\t\t1- plasmid accession\n\t\t2- output search regions dir\n\t\t3- input gb dir\n\n")
		sys.exit(1)
	
	plasmid_accession = sys.argv[1]
	output_search_regions_dir = sys.argv[2].rstrip('/')
	input_gb_dir = sys.argv[3].rstrip('/')

	return plasmid_accession, output_search_regions_dir, input_gb_dir

def parseGbFile(input_gb_fn, output_search_regions_fn, output_gb_fn):

	with open (output_search_regions_fn, 'w') as osrd:
		with open(output_gb_fn, 'w') as ogbd:
			red = "\033[0;31m"
			green = "\033[0;32m"
			blue = "\033[0;34m"
			no_color = "\033[0m"

			with open(input_gb_fn, 'r') as ifd:
				section_names = ( "assembly_gap", "CDS", "gene", "misc_difference", "misc_feature", "misc_recomb", "mobile_element", "ncRNA", "operon", "oriT", "primer_bind", "protein_bind", "regulatory", "repeat_region", "rep_origin", "sig_peptide", "source", "tRNA" )
				subsection_names_of_interest = ( "function", "gene", "note", "product" )

				# skip from LOCUS to FEATURES
				line = ifd.readline() # grab the first line ("LOCUS")
				while line.rstrip('\n').lstrip(' ').split(' ')[0] != "FEATURES":
					ogbd.write(line)
					line = ifd.readline()

				# write then skip past FEATURES
				ogbd.write(line)
				line = ifd.readline()

				# skip any lines necessary until CDS or ORIGIN is found
				tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]

				while tag_word != "ORIGIN" and tag_word != "CDS":
					ogbd.write(line)
					line = ifd.readline()
					tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]

				# First time: found ORIGIN or CDS. If ORIGIN, we're done. If CDS, read through each CDS region, until ORIGIN.
				# thereafter: found ORIGIN or CDS or other section name. If ORIGIN, we're done. If CDS, read through each CDS region, until ORIGIN. If section name, skip till ORIGIN or next CDS.
				while tag_word != "ORIGIN":
					
					# first time: this loop will be skipped. Thereafter, if a section name (other than CDS), skip to next CDS or ORIGIN.
					while tag_word != "ORIGIN" and tag_word != "CDS":
						ogbd.write(line)
						line = ifd.readline()
						tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]

					if tag_word == "CDS":
						# write the CDS line
						osrd.write(line)
						ogbd.write(blue + line + no_color)
					else: # if tag_word == "ORIGIN":
						break
					
					# skip past the CDS line (guaranteed to now have a CDS line)
					line = ifd.readline()
					tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]

					# read through important data and stop at end of CDS (marked by next CDS or ORIGIN or other section name)
					# first time: guaranteed inside a CDS region. Note that a CDS line is NEVER *immediately* followed by another section name line.
					# thereafter: It could be anything between the CDS and ORIGIN.
					# note: the following are the *only* times where a section name is on a line *immediately* following a line with another section name:
					#	ACCESSION     | line num   | section name + line
					#	--------------|------------|------------------------------------------
					#	KX839207.gb	26	     source          1..299858
					#	KX868553.gb	27	     source          1..12506
					#	
					#	KY494864.gb	974	     primer_bind     68554..68573
					#	KY494864.gb	975	     misc_feature    68605..68636
					#	
					#	KY494864.gb	5353	     rep_origin      404440..404503
					#	KY494864.gb	5354	     CDS             404657..405295
					#	
					#	MF168945.gb	303	     rep_origin      complement(18641..19572)
					#	MF168945.gb	304	     CDS             complement(19601..20614)
					#	
					#	MF344574.gb	370	     mobile_element  19505..21706
					#	MF344574.gb	371	     misc_feature    complement(19505..19795)
					#	
					#while tag_word != "ORIGIN" and tag_word != "CDS":
					while tag_word != "ORIGIN" and tag_word not in section_names:
						if line.rstrip('\n').lstrip(' ')[0] == '/': # it is a CDS subsection headerline
							subsection_name = line.strip().split('=')[0].lstrip('/').lower()
							subsection = '='.join(line.strip().split('=')[1:])
							if subsection_name in subsection_names_of_interest: # the subsection is one we care to look in
								osrd.write(line)
								ogbd.write(green + line + no_color)

								if subsection[0] == '"' and subsection[-1] != '"': # the subsection spans multiple lines
								
									line = ifd.readline()
									tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]
									while line.rstrip('\n')[-1] != '"': # keep searching to find the end of the subsection of interest
										osrd.write(line)
										ogbd.write(green + line + no_color)
										line = ifd.readline()
										tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]
									osrd.write(line)
									ogbd.write(green + line + no_color)
								
								line = ifd.readline()
								tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]
							else: # the subsection is not one we care to look in
								#if len(subsection) < 1:
								#	print("subsection len == 0")
								#	print(line)
								#	print(subsection_name)
								#	print(subsection)
								# simple version that works, but doesn't write it all in red
								#ogbd.write(line)
								#line = ifd.readline()
								#tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]

								# uneccesary version that actually makes it write it all in red
								ogbd.write(red + line + no_color)
								if len(subsection) and subsection[0] == '"' and subsection[-1] != '"': # the subsection spans multiple lines
									line = ifd.readline()
									tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]
									while line.rstrip('\n')[-1] != '"': # keep searching to find the end of the subsection of interest
										ogbd.write(red + line + no_color)
										line = ifd.readline()
										tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]
									ogbd.write(red + line + no_color)
								line = ifd.readline()
								tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]

						else: # it is not a CDS subsection headerline
							ogbd.write(line)
							line = ifd.readline()
							tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]
								
				# NOTE: the remainder of the file contains the sequence data
				ogbd.write(line) # write the ORIGIN
				ogbd.write(ifd.read()) # write the rest of the file (i.e., the sequence data)

# ==== #
# MAIN #
# ==== #

if __name__ == "__main__":

	import sys
	
	# handle args
	plasmid_accession, output_search_regions_dir, input_gb_dir = handleArgs()

	# set some helpful vars
	osrn = output_search_regions_dir + '/' + plasmid_accession + "_searchRegions.txt"
	ogbn = output_search_regions_dir + '/' + plasmid_accession + "_searchRegions.gb"
	igbn = input_gb_dir + '/' + plasmid_accession + ".gb"

	# 	get CDS info (Antimicrobial Resistance CDS (%) ... Total CDS)
	parseGbFile(igbn, osrn, ogbn)

	# exit
	sys.exit(0)

