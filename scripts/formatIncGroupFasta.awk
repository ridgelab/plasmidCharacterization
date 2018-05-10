#! /bin/awk -f

{
	if ( $0 ~ /^>.+$/ ) {
		
		if ( NR != 1 ) {
			printf "\n";
		}

		if ( $0 ~ /^>Inc.+$/ ) {
			print $0;
		}
		else {
			printf "%s%s\n", ">Inc", substr($0, 2);
		}
	}
	else {
		printf "%s", $0;
	}
}

END {
	printf "\n";
}
