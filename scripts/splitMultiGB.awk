#! /bin/awk -f
BEGIN {
	FS="[ ]+";
	accession="";
	ofn="";
}

{
	if ($0 == "//" || $0 == "")
	{
		accession = "";
		ofn = "";
	}
	else if ($1 == "LOCUS")
	{
		accession = $2;
		ofn = accession ".gb";
		#print "accession: " accession
		#print "ofn: " ofn
		print $0 > ofn;
	}
	else
	{
		print $0 >> ofn;
	}
}

END {
	print "done splitting " FILENAME " by accession";
}
