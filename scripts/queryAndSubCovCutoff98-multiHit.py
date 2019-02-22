# NOTE that the blastn output is a customized format 6. It will be
# tab-separated and have the following columns:
#
#	1      2      3      4      5      6      7    8      9    10     11   12     13   14   15
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send qseq sseq
#
import sys

def processMultiHits(mh):
	# return early if mh is empty (shouldn't be necessary)
	if len(mh) == 0:
		return []

	# set some helpful variables
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
	qcov = sum(qfilter) / float(qlen)
	scov = sum(sfilter) / float(slen)

	# return the additional identical plasmids
	additional_identical_plasmids = []
	if qcov >= 0.98 and scov >= 0.98:
		additional_identical_plasmids.append(sseqid)

	return additional_identical_plasmids # either a list with one item or an empty list

if __name__ == "__main__":
	
	if len(sys.argv) != 2:
		sys.stderr.write("ERROR: Incorrect args. 1- input blast results tsv file.\n")
		sys.exit(1)
	
	ifn = sys.argv[1]

	identical_plasmids = []

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

			identical_plasmids.extend(processMultiHits(multi_hits))
	
	if identical_plasmids: # if it's not an empty list
		print('\n'.join(sorted(identical_plasmids)))
	
	sys.exit(0)

# NOTE that the blastn output is a customized format 6. It will be
# tab-separated and have the following columns:
#
#	1      2      3      4      5      6      7    8      9    10     11   12     13   14   15
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send qseq sseq
#
