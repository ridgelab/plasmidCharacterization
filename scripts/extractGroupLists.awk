#! /bin/awk -f
BEGIN {
	FS="[ ]+";
	accession="";
	ofn="";
}

{
	if (NR == 1)
	{
		ofn = gensub(/^(.+)\.gb$/, "\\1", "-1", gensub(/^.*\//, "", "-1", FILENAME)) ".list";
	}
	
	if ($1 == "LOCUS")
	{
		accession = $2;
		print accession >> ofn;
	}
}

END {
	print "done extracting accessions from " FILENAME;
}
