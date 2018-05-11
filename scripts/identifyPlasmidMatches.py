
# ========= #
# FUNCTIONS #
# ========= #

def handleArgs():
	import sys

	if len(sys.argv) != 4:
		sys.stderr.write("\n\tERROR: You must provide 3 arguments\n\t\t1- plasmid accession\n\t\t2- input search regions  dir\n\t\t3- output matches dir\n\n")
		sys.exit(1)
	
	plasmid_accession = sys.argv[1]
	input_search_regions_dir = sys.argv[2].rstrip('/')
	output_matches_dir = sys.argv[3].rstrip('/')

	return plasmid_accession, input_search_regions_dir, output_matches_dir

def writeLineToMatchesFile(matches_fd, ignored, categories, search_term, cds_search_region):
	matches_fd.write(str(ignored)  + '\t' + ','.join(categories) + '\t' + search_term + '\t' + convertCDSsearchRegionToOneLineStr(cds_search_region) + '\n')

def ignoreCDS(cds_search_region, matches_fd):
	key_terms = [ r"truncated", r"interrupted", r"partial", r"disrupted", 
		r"intron", r"kl\.pn\.i3", r"se\.ma\.[\s]", r"morpho", 
		r"repeat region", r"patho", r"ncrna", r"imperfect",
		r"non[ -]?functional", r"is(?:[a-z]{2}|)[0-9]{2,4}" ]

	return searchCdsRegionForKeyTerms(cds_search_region, key_terms, matches_fd, True, ["Ignored"])

def betaLactSpecialCopyNum(cds_search_region, matches_fd):
	#key_terms = [ r"[^-]ndm", r"(?:imp$|[^-]imp[^ab])", r"[^-]vim", r"[^-]kpc", r"carbapenem[^\s]" ] 
	#key_terms = [ r"[^-]ndm", r"(?:imp$|[^-]imp[^abc])", r"[^-]vim", r"[^-]kpc", r"carbapenem[^\s]" ] 
	#key_terms = [ r"(?:^ndm|[ a]ndm)", r"(?:imp$|^imp[^abc]|[ a]imp[^abc])", r"(?:^vim|[ a]vim)", r"(?:^kpc|[ a]kpc)", r"carbapenem[^\s]" ] 
	key_terms = [ r"(?:^|[^b-z])ndm", r"(?:^|[^b-z])imp(?:$|[^abc])", r"(?:^|[^b-z])vim", r"(?:^|[^b-z])kpc", r"carbapenem[^\s]" ] 

	return searchCdsRegionForKeyTerms(cds_search_region, key_terms, matches_fd, False, ["Antimicrobial Resistance", "Beta-lactimase", "Beta-lactimase Special"])

def betaLactSearch(cds_search_region, matches_fd):
	if not betaLactSpecialCopyNum(cds_search_region, matches_fd):

		key_terms = [ r"(?:^|[^p])bla", r"beta[ -]lactim[^\s]", r"(?:^|[^p])oxa-", 
			r"(?:^|[^p])dha-", r"(?:^|[^p])sfo-", r"(?:^|[^p])shv-", r"(?:^|[^p])tem-", 
			r"(?:^|[^p])ctx-", r"(?:^|[^p])ampr", r"(?:^|[^p])cmy-", r"oxacillin[^\s]", 
			r"penicillin[^\s]", r"cephalosporin[^\s]" ]

		return searchCdsRegionForKeyTerms(cds_search_region, key_terms, matches_fd, False, ["Antimicrobial Resistance", "Beta-lactimase"])
	else:
		return True

def antimicrobResistSearch(cds_search_region, matches_fd):
	if not betaLactSearch(cds_search_region, matches_fd):

		key_terms = [ r"aac", r"aad", r"aph", r"arr-", 
			r"resistance", r"aminoglyco[^\s]", r"streptomycin", r"chloramphenicol", 
			r"cme[abc]", r"catr", r"multidrug", r"efflux pump", 
			r"mercur[^\s]", r"teller[^\s]", r"arsen[^\s]", r"qace", 
			r"macrolide", r"mph", r"silver", r"copper", 
			r"flor", r"ter[abcfw-z](?:$|[^a-z])", r"fluoroquino[^\s]", r"bleomycin", 
			r"tetr(?:$|[^a]|acycline)", r"pco[a-ers]", r"ars[a-dhr]", r"sil[abcefprs]", 
			r"(?:sulfonamide|trimethoprim|nickel)[ -]resistant", r"(?:[^a-z]|^)folp(?:$|[^a-z])", 
			r"(?:[^a-z]|^)sul[12](?:$|[^a-z])", r"(?:[^a-z]|^)dfra(?:$|[^a-z])", 
			r"(?:[^a-z]|^)ncr[a-c,y](?:$|[^a-z])", r"(?:[^a-z]|^)nirb(?:$|[^a-z])", r"rifamp(?:in|icin)" ]
		
		return searchCdsRegionForKeyTerms(cds_search_region, key_terms, matches_fd, False, ["Antimicrobial Resistance"])
	else:
		return True

def plasmidTransferSearch(cds_search_region, matches_fd):
	key_terms = [ r"conjuga[^\s]", r"pili[^\s]", r"pilus", r"type[ -]iv", 
		r"secretion system", r"fertility inhibition", r"tivb[^\s]", r"icm[^\s]", 
		r"tra[a-rtuwxy](?:$|[^a-z])", r"trb[a-gilm]", r"mob[a-e]", r"fino", 
		r"vir[^ugo\s]", r"pilx" ]

	return searchCdsRegionForKeyTerms(cds_search_region, key_terms, matches_fd, False, ["Plasmid Transfer"])

def toxinSearch(cds_search_region, matches_fd):
	key_terms = [ r"(?:^|[^a-z]|anti)toxi[^\s]", r"stb[de]", r"hig[ab]", r"cbta", 
		r"rel[be]", r"hica", r"yafo", r"ccd[ab]", 
		r"abrb", r"par[de]", r"pem[ik]", r"hokg" ]

	return searchCdsRegionForKeyTerms(cds_search_region, key_terms, matches_fd, False, ["Toxin System"])

def dnaMaintSpecialCopyNum(cds_search_region, matches_fd):
	key_terms = [ r"muc[ab]", "umu[cd]", "polymerase" ]

	return searchCdsRegionForKeyTerms(cds_search_region, key_terms, matches_fd, False, ["DNA Maintenance", "DNA Maintenance Special"])

def dnaMaintSearch(cds_search_region, matches_fd):
	if not dnaMaintSpecialCopyNum(cds_search_region, matches_fd):

		key_terms = [ r"methylase", r"single-strand binding protein", r"ssb", r"topb", 
			r"replication protein", r"kfra", r"kor[ab]", r"trfa", 
			r"helicase", r"dna", r"chromosome", r"entry exclusion", 
			r"eex", r"exca", r"nucleoti[^\s]", r"topoisomerase", 
			r"integrase", r"(?<!ser_|ine )recombinase", r"replication", r"nuclease", 
			r"relaxase", r"plasmid", r"ruma", r"repa", 
			r"uvr[^\s]", r"par[ab]", r"vag[cd]" ]
			# removed: r"ruva"

		return searchCdsRegionForKeyTerms(cds_search_region, key_terms, matches_fd, False, ["DNA Maintenance"])
	else:
		return True

def mobileGeneticElementsSearch(cds_search_region, matches_fd):
	key_terms = [ r"transpos[^\s]", r"reverse transcriptase", r"tnp", 
		r"ist[ab](?:$|[^a-z0-9])", r"resolvase", "urf2" ]

	return searchCdsRegionForKeyTerms(cds_search_region, key_terms, matches_fd, False, ["Mobile Genetic Elements"])

def hypotheticalGenesSearch(cds_search_region, matches_fd):
	key_terms = [ r"hypothetical", r"domain[ -]containing", r"uncharacterized protein", r"unknown function" ]

	return searchCdsRegionForKeyTerms(cds_search_region, key_terms, matches_fd, False, ["Hypothetical Genes"])

def convertCDSsearchRegionToOneLineStr(cds_search_region):
	return "\\n".join(list(map(lambda x: x.replace('\t', "\\t").replace('\n', ""), cds_search_region)))

def searchCDSRegion(cds_search_region, matches_fd):
	# make cds_search_region all lowercase
	cds_search_region = list(map(lambda x: x.lower(), cds_search_region)) # make all the search regions lowercase
	
	if not ignoreCDS(cds_search_region, matches_fd):
		if not antimicrobResistSearch(cds_search_region, matches_fd):
			if not plasmidTransferSearch(cds_search_region, matches_fd):
				if not toxinSearch(cds_search_region, matches_fd):
					if not dnaMaintSearch(cds_search_region, matches_fd):
						if not mobileGeneticElementsSearch(cds_search_region, matches_fd):
							if not hypotheticalGenesSearch(cds_search_region, matches_fd):
								writeLineToMatchesFile(matches_fd, False, ["Other"], "NA", cds_search_region)
								#matches_fd.write("False\tOther\tNA\t" + convertCDSsearchRegionToOneLineStr(cds_search_region) + '\n')

def searchCdsRegionForKeyTerms(cds_search_region, key_terms, matches_fd, ignored, categories):
	import re

	for search_sub_region in cds_search_region:
		for key_term in key_terms:
			if re.search(key_term, search_sub_region) is not None:
				writeLineToMatchesFile(matches_fd, ignored, categories, key_term, cds_search_region)
				return True
	
	return False


def parseSearchRegionFile(input_sr_fn, matches_fn):
	import re

	with open(input_sr_fn, 'r') as ifd:
		with open(matches_fn, 'w') as mfd:
			mfd.write("Ignored (True/False)\tCategories (c1[,c2,...,cN])\tSearch Term\tCDS Region\n")

			cds_search_region = []

			# All data is important. Read through all CDS regions separately and search through them.
			# Each CDS region begins with CDS and ends with another CDS record or the end of file

			# grab first line (always a CDS line)
			line = ifd.readline()
			tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]
			cds_search_region.append(line)
		
			# grab the next line
			line = ifd.readline()
			tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]
			while line != "":
				while line != "" and tag_word != "CDS":
					cds_search_region.append(line)
					line = ifd.readline()
					tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]
						
				# search the region
				searchCDSRegion(cds_search_region, mfd)
				cds_search_region = []
			
				# grab the next line
				cds_search_region.append(line)
				line = ifd.readline()
				tag_word = line.rstrip('\n').lstrip(' ').split(' ')[0]

# ==== #
# MAIN #
# ==== #

if __name__ == "__main__":

	import sys
	
	# handle args
	plasmid_accession, input_search_regions_dir, output_matches_dir = handleArgs()

	# set some helpful vars
	isrn = input_search_regions_dir + '/' + plasmid_accession + "_searchRegions.txt"
	mfn = output_matches_dir + '/' + plasmid_accession + "_matches.tsv"

	# search the search regions file for matches
	parseSearchRegionFile(isrn, mfn)
	
	# exit
	sys.exit(0)

