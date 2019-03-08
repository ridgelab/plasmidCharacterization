
import sys
from pathlib import Path

def buildInitialIdenticalPlasmidsDict(input_identical_plasmids_path, input_identical_plasmids_suffix):
	init_ident_plasmids = {}
	location = Path(input_identical_plasmids_path)

	for f in location.glob("*" + input_identical_plasmids_suffix):
		accession = f.parts[-1].rstrip(input_identical_plasmids_suffix)

		if not accession in init_ident_plasmids:
			init_ident_plasmids[accession] = set()

		with f.open() as ifd:
			for line in ifd:
				ident_accession = line.strip()

				if not ident_accession in init_ident_plasmids:
					init_ident_plasmids[ident_accession] = set()

				init_ident_plasmids[accession].add(ident_accession)	
				init_ident_plasmids[ident_accession].add(accession)	
	
	return init_ident_plasmids

def buildInitialCoverageInfoArray(input_coverage_info_path, input_coverage_info_suffix):
	init_cov_info = []
	location = Path(input_coverage_info_path)

	for f in location.glob("*" + input_coverage_info_suffix):
		with f.open() as ifd:
			ifd.readline() # skip past header line
			for line in ifd:
				fields = line.rstrip('\n').split('\t')
				init_cov_info.append(fields)

	return init_cov_info

def covInfoElemsAreIdent(e1, e2):
	for x1,x2 in zip(e1,e2):
		if not x1 == x2:
			return False
	return True

def covInfoElemsAreRecip(e1, e2):
	re2 = e2[4:] + e2[:4]
	return covInfoElemsAreIdent(e1, re2)

def inArray(e, arr):
	for x in arr:
		if covInfoElemsAreIdent(x,e):
			return True
	return False

def reciprocateCoverageInfoArray(cov_info):
	recip = []
	
	for e in cov_info:
		re = e[4:] + e[:4]
		if not inArray(e, recip):
			recip.append(e)
		if not inArray(re, recip):
			recip.append(re)
	
	return recip

def fixIdentPlasmidsWithRecipCovInfo(identical_plasmids, coverage_info):
	for e in coverage_info:
		qseqid = e[0]
		sseqid = e[4]

		if not qseqid in identical_plasmids:
			identical_plasmids[qseqid] = set()

		if not sseqid in identical_plasmids:
			identical_plasmids[sseqid] = set()

		identical_plasmids[qseqid].add(sseqid)
		identical_plasmids[sseqid].add(qseqid)
	
	return

def writeCoverageInfo(coverage_info, output_coverage_info_path, output_coverage_info_suffix):
	
	# write the header line out to each file
	for e in coverage_info:
		qseqid = e[0]
		with open(output_coverage_info_path + "/" + qseqid + output_coverage_info_suffix, 'w') as ofd:
			ofd.write("qseqid\tqcount\tqlen\tqcov\tsseqid\tscount\tslen\tscov\n")
	
	# write the remaining lines out to the files
	for e in coverage_info:
		qseqid = e[0]
		with open(output_coverage_info_path + "/" + qseqid + output_coverage_info_suffix, 'a') as ofd:
			ofd.write('\t'.join(e) + '\n')
	
	return

def writeIdenticalPlasmids(identical_plasmids, output_identical_plasmids_path, output_identical_plasmids_suffix):
	for accession in identical_plasmids:
		with open(output_identical_plasmids_path + '/' + accession + output_identical_plasmids_suffix, 'w') as ofd:
			if len(identical_plasmids[accession]):
				ofd.write('\n'.join(sorted(list(identical_plasmids[accession]))) + '\n')
	
	return

if __name__ == "__main__":
	
	if len(sys.argv) != 7:
		sys.stderr.write("ERROR: Incorrect args.\n\t1- coverage info path\n\t2- identical plasmids path\n\t3- input coverage info suffix\n\t4- output coverage info suffix\n\t5- input identical plasmid suffix\n\t6- output identical plasmid suffix\n\n")
		sys.exit(1)
	
	icip = sys.argv[1] # coverage info path 
	iipp = sys.argv[2] # identical plasmids path
	icis = sys.argv[3] # input coverage info suffix (_identicalPlasmids.list)
	ocis = sys.argv[4] # output coverage info suffix (_identicalPlasmids_concordant.list)
	iips = sys.argv[5] # input identical plasmids suffix (_covInfo.tsv)
	oips = sys.argv[6] # output identical plasmids suffix (_covInfo_concordant.tsv)

	# build intial identical plasmids dictionary
	identical_plasmids = buildInitialIdenticalPlasmidsDict(iipp, iips)

	# build initial coverage info array
	coverage_info = buildInitialCoverageInfoArray(icip, icis)

	# reciprocate coverage info array
	coverage_info = reciprocateCoverageInfoArray(coverage_info)

	# fix identical plasmids dictionary based on reciprocal coverage info
	fixIdentPlasmidsWithRecipCovInfo(identical_plasmids, coverage_info)

	# write coverage info
	writeCoverageInfo(coverage_info, icip, ocis)

	# write identical plasmids
	writeIdenticalPlasmids(identical_plasmids, iipp, oips)

	# exit
	sys.exit(0)

# coverage info columns
# 0      1      2    3    4      5      6    7  
# qseqid qcount qlen qcov sseqid scount slen scov

