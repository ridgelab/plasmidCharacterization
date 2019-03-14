import sys

def processMultiHits(mh):
	# return early if mh is empty (shouldn't be necessary)
	if len(mh) == 0:
		return []

	# set some helpful variables
	qseqid = mh[0][0]
	sseqid = mh[0][1]
	qlen = int(mh[0][6])
	slen = int(mh[0][10])

	qfilter = [False] * qlen
	sfilter = [False] * slen

	# scan through recording qcov and scov by position in the q&s filters
	for h in mh:
		hqs = int(h[7])
		hqe = int(h[8])
		hss = int(h[11])
		hse = int(h[12])

		qs = hqs
		qe = hqe
		if hqs > hqe:
			qs = hqe
			qe = hqs

		ss = hss
		se = hse
		if hss > hse:
			ss = hse
			se = hss

		for i in range(qs - 1, qe, 1):
			qfilter[i] = True

		for i in range(ss - 1, se, 1):
			sfilter[i] = True

	# calculate coverage
	qcount = sum(qfilter)
	scount = sum(sfilter)
	qcov = qcount / float(qlen)
	scov = scount / float(slen)

	# return the additional identical plasmids
	additional_identical_plasmid = None
	if qcov >= 0.98 and scov >= 0.98:
		additional_identical_plasmid = sseqid

	return additional_identical_plasmid, qcount, qlen, qcov, scount, slen, scov # additinal...plasmid= either one sseqid or None

if __name__ == "__main__":
	
	if len(sys.argv) != 4:
		sys.stderr.write("ERROR: Incorrect args.\n\t1- input blast results tsv file.\n\t2- output ident plasmids list file.\n\t3- output coverage info tsv file.\n\n")
		sys.exit(1)
	
	ifn = sys.argv[1] # input file name
	olfn = sys.argv[2] # output list file name
	ocifn = sys.argv[3] # output coverage info filename

	identical_plasmids = []
	records = []

	# process the input
	with open(ifn, 'r') as ifd:
		line = ifd.readline()
		fields = line.rstrip('\n').split('\t')

		while line != '':
			multi_hits = [] # 2d array: all the lines (sets of fields) that associate with a pairwise sequence blast

			qseqid = fields[0]
			sseqid = fields[1]
			sseqid_of_interest = str(sseqid)

			if qseqid == sseqid:
				line = ifd.readline()
				fields = line.rstrip('\n').split('\t')
				continue

			while line != '' and sseqid == sseqid_of_interest:
				multi_hits.append(fields)
				line = ifd.readline()
				fields = line.rstrip('\n').split('\t')
				if line != '':
					qseqid = fields[0]
					sseqid = fields[1]

			addtl_ident_plasmid, qcount, qlen, qcov, scount, slen, scov = processMultiHits(multi_hits)
			if addtl_ident_plasmid: # the item isn't empty
				identical_plasmids.append(addtl_ident_plasmid)
				records.append((qseqid, qcount, qlen, qcov, addtl_ident_plasmid, scount, slen, scov))

	# write the output
	with open(olfn, 'w') as olfd:
		with open(ocifn, 'w') as ocifd:
			print("qseqid", "qcount", "qlen", "qcov", "sseqid", "scount", "slen", "scov", sep='\t', file=ocifd) # write the header
			if identical_plasmids: # if it's not an empty list
				print('\n'.join(sorted(identical_plasmids)), file=olfd)
				for record in records:
					print(*record, sep='\t', file=ocifd)
	

	sys.exit(0)

# NOTE that the blastn output is a customized format 6. It will be
# tab-separated and have the following columns:
#
#	1      2      3      4      5      6      7    8      9    10     11   12     13   14   15
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send qseq sseq
#
