# NOTE that the blastn output is a customized format 6. It will be
# tab-separated and have the following columns:
#
#	1      2      3      4      5      6      7    8      9    10     11   12     13   14   15
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send qseq sseq
#
# After this is run, it will have two new columns (qcov & scov, cols 14 & 15) and will look like this:
#
#	1      2      3      4      5      6      7      8    9    10     11   12     13   14   15   16   17
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send qcov scov qseq sseq
#

import sys

def getModifiedLine(original_fields, query_coverage, subject_coverage):
	return '\t'.join(original_fields[:14]) + '\t' + str(query_coverage) + '\t' + str(subject_coverage) + '\t' + '\t'.join(original_fields[14:]))

def processMultiHits(mh):
	# 4 = length, 7 = qlen, 11 = slen, qcov = length / qlen, scov = length / slen

	if len(mh) == 0:
		return

	qlen = int(mh[1][7])
	slen = int(mh[1][11])

	qfilter = [False] * qlen
	sfilter = [False] * slen


	
	

if __name__ == "__main__":
	
	if len(sys.argv) != 2:
		sys.stderr.write("ERROR: Incorrect args. 1- input blast results tsv file.\n")
		sys.exit(1)
	
	ifn = sys.argv[1]

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
				continue

			while line != '' and sseqid == sseqid_of_interest:
				multi_hits.append(fields)
				line = ifd.readline()
				fields = line.rstrip('\n').split('\t')
				qseqid = fields[0]
				sseqid = fields[1]

			processMultiHits(multi_hits)


	


# NOTE that the blastn output is a customized format 6. It will be
# tab-separated and have the following columns:
#
#	1      2      3      4      5      6      7    8      9    10     11   12     13   14   15
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send qseq sseq
#
# After this is run, it will have two new columns (qcov & scov, cols 14 & 15) and will look like this:
#
#	1      2      3      4      5      6      7      8    9    10     11   12     13   14   15   16   17
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send qcov scov qseq sseq
#
