#! /bin/awk -f

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

BEGIN {
	FS="\t";
	OFS="\t";
	ORS="\n";
	count=0;
}

{
	# 4 = length, 7 = qlen, 11 = slen, qcov = length / qlen, scov = length / slen
	qcov = $4 / $7;
	scov = $4 / $11;
	if (qcov >= 0.98 && scov >= 0.98)
	{
		count += 1

		# keep 1-13, add new columns, keep 14-15 (will become 16-17)
		for (i = 1; i <= 13; i++)
		{
			printf "%s", $i OFS;
		}
		
		printf "%f", qcov OFS;
		printf "%f", scov OFS;

		for (i = 14; i <= NF; i++)
		{
			printf "%s", $i (i == NF ? ORS : OFS);
		}
	}
}

END {
	print FILENAME ": " count > "/dev/stderr";
}
