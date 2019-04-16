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
service = Service("http://www.mousemine.org/mousemine/service", token = "<INSERT YOUR MOUSEMINE ACCOUNT'S DEV KEY>")

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

# This query's custom sort order is specified below:
query.add_sort_order("Gene.homologues.homologue.primaryIdentifier", "ASC")

# You can edit the constraint values below
query.add_constraint("homologues.homologue.organism.taxonId", "=", "10090", code = "J")
query.add_constraint("organism.taxonId", "=", "9606", code = "D")
query.add_constraint("homologues.dataSets.name", "=", "Mouse/Human Orthologies from MGI", code = "B")
query.add_constraint("homologues.type", "NONE OF", ["horizontal gene transfer", "least diverged horizontal gene transfer"], code = "C")
query.add_constraint("Gene", "LOOKUP", "EGFR", code = "A")
query.add_constraint("Gene", "LOOKUP", "Brca1", code = "E")

# Uncomment and edit the code below to specify your own custom logic:
query.set_logic("A or E and D and J and B and C")

for row in query.rows():
    print(row["primaryIdentifier"], row["symbol"], row["organism.name"], \
        row["homologues.homologue.primaryIdentifier"], row["homologues.homologue.symbol"], \
        row["homologues.homologue.organism.name"], \
        row["homologues.homologue.ontologyAnnotations.ontologyTerm.identifier"], \
        row["homologues.homologue.ontologyAnnotations.ontologyTerm.name"])