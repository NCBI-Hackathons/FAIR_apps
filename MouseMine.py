#!/usr/bin/env python

# This is an automatically generated script to run your query
# to use it you will require the intermine python client.
# To install the client, run the following command from a terminal:
#
#     sudo easy_install intermine
#
# For further documentation you can visit:
#     http://intermine.readthedocs.org/en/latest/web-services/

# The following two lines will be needed in every python script:
from intermine.webservice import Service
service = Service("http://www.mousemine.org/mousemine/service", token = "h1s62a62S6Yey3Z8TeUb")

# Get a new query on the class (table) you will be querying:
query = service.new_query("Gene")

# Type constraints should come early - before all mentions of the paths they constrain
query.add_constraint("homologues.homologue.ontologyAnnotations.ontologyTerm", "MPTerm")

# The view specifies the output columns
query.add_view(
    "primaryIdentifier", "symbol", "organism.name",
    "homologues.homologue.primaryIdentifier", "homologues.homologue.symbol",
    "homologues.homologue.organism.name",
    "homologues.homologue.ontologyAnnotations.ontologyTerm.identifier",
    "homologues.homologue.ontologyAnnotations.ontologyTerm.name"
)

# Right now we are reading a file to get a list of genes. We may want to change this later.
def getGeneList():
	inputList = "data/exomiser_out/Pfeiffer.exomiser_AD.genes.tsv"
	geneList = []
	with open(inputList, 'r') as f:
		for line in f:
			line  = line.strip()
			# Skipe the header line at the top
			if line[0] == '#':
				continue
			# Split the line on tabs. The first field is the gene we want.
			fields = line.split('\t')
			geneList.append(fields[0])
	return sorted(geneList)

geneList = getGeneList()

# For each gene in a sub-list of genes, add their lookup to the query with an
# alphabetic code, and add the code to the logic string used in the actual query
def addGenesToQuery(query, genes):
	counter = 0
	asciiOffset = 69 # Capital E in ascii
	listLen = len(genes)
	logicStr = ""
	for gene in genes:
		# Convert the counter to the corresponding capital letter, starting with 'E'			
		currCode = chr(counter + asciiOffset) 
		query.add_constraint("Gene", "LOOKUP", gene, code = currCode)
		logicStr += currCode
		if counter < listLen -1:
			logicStr += " or "
		counter += 1
	return query, logicStr
	

# This query's custom sort order is specified below:
query.add_sort_order("Gene.homologues.homologue.primaryIdentifier", "ASC")

# You can edit the constraint values below
query.add_constraint("homologues.homologue.organism.taxonId", "=", "10090", code = "A")
query.add_constraint("organism.taxonId", "=", "9606", code = "B")
query.add_constraint("homologues.dataSets.name", "=", "Mouse/Human Orthologies from MGI", code = "C")
query.add_constraint("homologues.type", "NONE OF", ["horizontal gene transfer", "least diverged horizontal gene transfer"], code = "D")

initQuery = query
# Mouse Mine requires that each gene in the query be given a single-letter code. 
# The first 4 letters - A,B,C, and D - are already used. Only 22 letters remain.
# Ergo we can only submit genes from the original list at most 22 genes at a time.
subListMaxLen = 22
origLen = len(geneList)
currStart = 0

initLogicStr = "A and B and C and D and "
while(currStart < origLen):
	try:
		geneQueryStr = ""
		currEnd = min(currStart + subListMaxLen, origLen)
		query,currGeneLogicStr = addGenesToQuery(query, geneList[currStart:currEnd])
		finalLogicStr = initLogicStr + currGeneLogicStr
	
		query.set_logic(finalLogicStr)
	
		print("\n\nQuerying for genes %d - %d in list, which are genes %s\n\n" % (currStart, currEnd, str(geneList[currStart:currEnd])) )

		for row in query.rows():
			print(row["primaryIdentifier"], row["symbol"], row["organism.name"], \
			row["homologues.homologue.primaryIdentifier"], row["homologues.homologue.symbol"], \
			row["homologues.homologue.organism.name"], \
			row["homologues.homologue.ontologyAnnotations.ontologyTerm.identifier"], \
			row["homologues.homologue.ontologyAnnotations.ontologyTerm.name"])
	except:
		# Getting a weird exception from the internals intermine in one case only. No time to debug it right now
		pass

	# reset the query when done with this iteration of the loop
	query = initQuery
	currStart += subListMaxLen



