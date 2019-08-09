
import sys
import re

def getColors(fn):
	
	colors = {}

	with open(fn, 'r') as fd:
		for line in fd:
			fields = line.strip().split('\t')
			group = fields[0]
			color = fields[1]
			colors[group] = color
	
	return colors

def getTree(fn):
	tree = ''
	with open(fn, 'r') as fd:
		tree = fd.readline().strip()
		line = fd.readline()
		if line != '':
			print("ERROR: the tree file had more than one line", file=sys.stderr)
			sys.exit(1)
	return tree

def getLabels(tree):
	return set(re.findall(r'"([^"]+)"', tree))

def getGroups(fns):
	groups = {}

	for fn in fns:
		group = fn.strip().split('/')[-1].split(".list")[0]
		accs = []
		with open(fn, 'r') as fd:
			accs = set(list(map(lambda x: x.strip(), fd.readlines())))
		groups[group] = accs
	
	return groups

def getTaxaColor(label, colors, groups):
	taxa = label.strip().split(',')[0]
	for group in groups:
		if taxa in groups[group]:
			return colors[group]
	return "505050" # grey (this should not end up being used)

def writeTaxaBlock(ofd, colors, labels, groups):
	ofd.write("begin taxa;\n")
	ofd.write("\tdimensions ntax=" + str(len(labels)) + ";\n\ttaxlabels\n")
	for label in sorted(list(labels)):
		ofd.write("\t'" + label + "'[&!color=#" + getTaxaColor(label, colors, groups) + "]\n")
	ofd.write(";\nend;\n")

def writeTreesBlock(ofd, tree):
	ofd.write("begin trees;\n")
	ofd.write("\ttree tree_1 = [&R] ")
	ofd.write(tree.replace('"', "'"))
	ofd.write("\nend;\n")

def makeColoredNexus(nexus_fn, colors, tree, labels, groups):
	with open(nexus_fn, 'w') as ofd:
		ofd.write("#NEXUS\n")
		writeTaxaBlock(ofd, colors, labels, groups)
		ofd.write('\n')
		writeTreesBlock(ofd, tree)
		ofd.write('\n')


if __name__ == "__main__":

	nexus_fn = sys.argv[1] # output file
	colors_fn = sys.argv[2] # input color associations (between group name and color)
	newick_fn = sys.argv[3] # input newick tree
	groups_lists_fns = sys.argv[4:] # input group lists (lists of accessions in the groups)

	colors = getColors(colors_fn)
	tree = getTree(newick_fn)
	labels = getLabels(tree)
	groups = getGroups(groups_lists_fns)

	#print(colors, file=sys.stderr)
	#print(tree, file=sys.stderr)
	#print(labels, file=sys.stderr)
	#print(groups, file=sys.stderr)

	makeColoredNexus(nexus_fn, colors, tree, labels, groups)

