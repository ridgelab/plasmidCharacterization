#! /bin/awk -f

# NOTE that the blastn output is a customized format 6. It had scov added as
# column 14. It will be tab-separated and have the following columns:
#
#	1      2      3      4      5      6      7      8    9    10     11   12     13   14    15   16
#	qseqid sseqid pident length evalue qframe qlen qstart qend sframe slen sstart send scov qseq sseq
#
# After this is run, it will have a new column (family, col 3) and will look like this:
#
#	1      2      3      4      5      6      7      8    9      10   11     12   13     14   15   16   17
#	qseqid sseqid family pident length evalue qframe qlen qstart qend sframe slen sstart send scov qseq sseq
#

BEGIN {
	FS="\t";
	OFS="\t";
	ORS="\n";
}

{
	# 2 = subject_id, keep 1-2, add new column, keep 3-16 (will become 4-17)
	for (i = 1; i <= 2; i++)
	{
		printf "%s", $i OFS;
	}
	
	printf "%s", gensub(/^([^(_]+).*$/, "\\1", "-1", $2) OFS;

	for (i = 3; i <= NF; i++)
	{
		printf "%s", $i (i == NF ? ORS : OFS);
	}
}

