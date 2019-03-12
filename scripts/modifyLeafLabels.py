
import sys
import re

# ========= #
# FUNCTIONS #
# ========= #

def handleArgs():
	import sys

	if len(sys.argv) != 4:
		sys.stderr.write("\n\tERROR: You must provide 3 arguments\n\t\t1- input source info tsv\n\t\t2- input orig tree\n\t\t3- output orig tree\n\n")
		sys.exit(1)
	
	input_source_info_fn = sys.argv[1]
	input_tree_fn = sys.argv[2]
	output_tree_fn = sys.argv[3]

	return input_source_info_fn, input_tree_fn, output_tree_fn

# ==== #
# MAIN #
# ==== #

if __name__ == "__main__":
	
	# handle args
	isif, itf, otf = handleArgs()

	# read input source info
	source_info = {}
	with open(isif, 'r') as ifd:
		ifd.readline() # skip header line
		for line in ifd:
			fields = line.rstrip('\n').split('\t')

			accession = fields[0].strip('"')
			organism = fields[1].strip('"')
			iso_source = fields[2].strip('"')
			country = fields[3].strip('"').split(':')[0]
			collection_date = fields[4].strip('"')

			val = [accession]
			if country != "NA":
				val.append(country)
			val.append(organism)

			source_info[accession] = '"' + ','.join(val) + '"'
	
	# read input tree
	tree = ''
	with open(itf, 'r') as ifd:
		tree = ifd.read()

	# modify tree to output tree
	for old_ident in source_info:
		new_ident = source_info[old_ident]
		search = old_ident + r"([^A-Za-z0-9])"
		repl = new_ident + r"\1"
		tree = re.sub(search, repl, tree)

	# write output tree
	with open(otf, 'w') as ofd:
		ofd.write(tree)
	
	sys.exit(0)

