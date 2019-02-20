#! /bin/awk -f

BEGIN {
	FS="\t";
	RS="\n";
	OFS="\t";
	ORS="\n";

	seq_tech = "NA";
	num_techs = "NA";
	num_short = "NA";
	num_long = "NA";
	num_illumina = "NA";
	num_454 = "NA";
	num_abi = "NA";
	num_sanger = "NA";
	num_torrent = "NA";
	num_pacbio = "NA";
	num_nanopore = "NA";

}

/^[ ]+Sequencing Technology :: / {

	#seq_tech = substr($0, match ($0, / :: /) + 4);
	sub(/^[ ]+Sequencing Technology :: /, "", $0);
	seq_tech = $0;
	sub(/ +$/, "", seq_tech);

	# grab the next line
	getline;

	while ( $0 !~ /::/ && $0 !~ /##/ )
	{
		# remove leading whitespace
		sub(/^[ ]+/, "", $0);

		# append remaining string to seq_tech
		seq_tech = seq_tech " " $0;
		
		# grab the next line
		getline;
	}
	sub(/ +$/, "", seq_tech);
	sub(/; /, ",", seq_tech);

	split(tolower(seq_tech), seq_techs_lc, ",");

	num_techs = 0;
	num_short = 0;
	num_long = 0;
	num_illumina = 0;
	num_454 = 0;
	num_abi = 0;
	num_sanger = 0;
	num_torrent = 0;
	num_pacbio = 0;
	num_nanopore = 0;

	for (key in seq_techs_lc)
	{
		if ( seq_techs_lc[key] ~ /illumina/)
		{
			num_illumina += 1;
		}
		else if ( seq_techs_lc[key] ~ /454/)
		{
			num_454 += 1;
		}
		else if ( seq_techs_lc[key] ~ /abi/)
		{
			num_abi += 1;
		}
		else if ( seq_techs_lc[key] ~ /sanger/)
		{
			num_sanger += 1;
		}
		else if ( seq_techs_lc[key] ~ /torrent/)
		{
			num_torrent += 1;
		}
		else if ( seq_techs_lc[key] ~ /pacbio/ || seq_techs_lc[key] ~ /pacific/ )
		{
			num_pacbio += 1;
		}
		else if ( seq_techs_lc[key] ~ /nanopore/ || seq_techs_lc[key] ~ /minion/ )
		{
			num_nanopore += 1;
		}
	}

	num_long = num_pacbio + num_nanopore;
	num_short = num_illumina + num_454 + num_abi + num_sanger + num_torrent;
	num_techs = num_long + num_short;

	exit 0;
}

END {
	print seq_tech, num_techs, num_short, num_long, num_illumina, num_454, num_abi, num_sanger, num_torrent, num_pacbio, num_nanopore;
}
