
# ========= #
# FUNCTIONS #
# ========= #

def handleArgs():
	import sys

	if len(sys.argv) != 3:
		sys.stderr.write("\n\tERROR: You must provide 2 arguments\n\t\t1- input blast results cov60 fam\n\t\t2- output blast results file\n\n")
		sys.exit(1)
	
	input_br = sys.argv[1]
	output_br = sys.argv[2]

	return input_br, output_br

# ==== #
# MAIN #
# ==== #

if __name__ == "__main__":

	import sys
	
	# handle args
	ibrfn, obrfn= handleArgs()

	# set some handy vars
	records = [] # each line
	per_ids = [] # percent identities (the 4th column)

	with open(ibrfn, 'r') as ifd:
		for line in ifd:
			records.append(line)
			per_ids.append(float(line.rstrip('\n').split('\t')[3]))
		
	# figure out which ones to keep
	keep = []

	max_per_id = max(per_ids) if len(records) > 0 else 0.0

	for i,per_id in enumerate(per_ids):
		if abs(max_per_id - per_id) <= 1.0:
			keep.append(i)

	# write output
	with open (obrfn, 'w') as ofd:
		for i in keep:
			ofd.write(records[i])

	# exit
	sys.exit(0)

