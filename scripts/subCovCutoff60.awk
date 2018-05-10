#! /bin/awk -f

# NOTE that the blastn output is a customized format 6. It will be
# tab-separated and have the following columns:
#
#	1      2      3      4      5      6      7    8      9    10     11   12     13   14   15
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send qseq sseq
#
# After this is run, it will have a new column (scov, col 14) and will look like this:
#
#	1      2      3      4      5      6      7      8    9    10     11   12     13   14    15   16
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send scov qseq sseq
#

BEGIN {
	FS="\t";
	OFS="\t";
	ORS="\n";
	count=0;
}

{
	# 4 = length, 11 = slen, scov = length / slen
	scov = $4 / $11;
	if (scov >= 0.6)
	{
		count += 1

		# keep 1-13, add new column, keep 14-15 (will become 15-16)
		for (i = 1; i <= 13; i++)
		{
			printf "%s", $i OFS;
		}
		
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
