#! /bin/awk -f
BEGIN {
	FS = "[ ]+";
	origin_found = 0; # false
}

{
	if (origin_found)
	{
		sub(/ *[0-9]+ /, "", $0);
		gsub(/ +/, "", $0);
		printf toupper($0);
	}
	else if ($1 == "ORIGIN")
	{
		origin_found = 1; # true
		
		print ">" gensub(/^(.+)\.gb$/, "\\1", "-1", gensub(/^.*\//, "", "-1", FILENAME));
	}
}

END {
	printf "\n";
	print "done extracting ORIGIN seq from " FILENAME " to fasta" > "/dev/stderr";
}
