#! /bin/awk -f

BEGIN {
	FS="\t";
	RS="\n";
	OFS="\t";
	ORS="\n";

	organism = "NA";
	isolation = "NA";
	country = "NA";
	collection_date = "NA";
}

/^[ ]+\/organism=/ {

	organism = substr($0, match ($0, /=/) + 1);
	while ( $0 !~ /"$/ )
	{
		# grab the next line
		getline;

		# remove leading whitespace
		sub(/^[ ]+/, "", $0);

		# append remaining string to organism
		organism = organism " " $0;
	}
	sub(/^"/, "", organism)
	sub(/"$/, "", organism)
}

/^[ ]+\/isolation_source=/ {

	isolation = substr($0, match ($0, /=/) + 1);
	while ( $0 !~ /"$/ )
	{
		# grab the next line
		getline;

		# remove leading whitespace
		sub(/^[ ]+/, "", $0);

		# append remaining string to isolation
		isolation = isolation " " $0;
	}
	sub(/^"/, "", isolation)
	sub(/"$/, "", isolation)
}

/^[ ]+\/country=/ {

	country = substr($0, match ($0, /=/) + 1);
	while ( $0 !~ /"$/ )
	{
		# grab the next line
		getline;

		# remove leading whitespace
		sub(/^[ ]+/, "", $0);

		# append remaining string to country
		country = country " " $0;
	}
	sub(/^"/, "", country)
	sub(/"$/, "", country)
}

/^[ ]+\/collection_date=/ {

	collection_date = substr($0, match ($0, /=/) + 1);
	while ( $0 !~ /"$/ )
	{
		# grab the next line
		getline;

		# remove leading whitespace
		sub(/^[ ]+/, "", $0);

		# append remaining string to collection_date
		collection_date = collection_date " " $0;
	}
	sub(/^"/, "", collection_date)
	sub(/"$/, "", collection_date)
}

END {
	print organism, isolation, country, collection_date;
}
