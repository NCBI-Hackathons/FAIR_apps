# FAIR_apps
## FAIR Data in -> FAIR Application run -> FAIR Data out.
 
  Today is a Learning exercise – and many are coming from many different angles – if we achieve even a portion of this ambitious objective we will have done a lot!
 
   The learning objectives for this hackathon I have gathered from folks is as follows:

  1. Learning about FAIR Applications – what does it mean and how does it happen?  FAIR Data In, FAIR Applications, FAIR data out and moving forward
  2. Learning about containers
  3. Learning about workflows

## The set up:
 
The concept is we want to connect the mouse models to human disease.
 
This is an idealized scenario, and for pedagogical principles, we are going through the exercise of the round robin of data from mouse to application to data from human.   We may or may not succeed in actually connecting the dots, but that may not matter for this exercise.
 
The exact details of this question are to be suggestive and not necessarily conclusive as the best way to go about this problem, but the goal is to be as useful and pragmatic as possible as we wrap our heads around what are the most important things about FAIR that we need to concern ourselves with.
 
## Data set:

  Please find attached the data (and I will be depositing these in github as our starting point).   
 
  Beginning with phenotype measures collected from a study, Chesler3, details were downloaded as json files from the phenome.jax.org using the RESTFul API.  The measures for that study are detailed in the table that was downloaded as well, measures.csv and details for the study are found in studies.csv.
 
  The attached R script reads this data in and merges the Chesler3 data with the measurements details.
 
## The idea:
  Beginning with mouse data, data from a specific mouse strain, subject to specific conditions, what are the measurements, the phenotypes that tell us about that mouse in this particular experiment.   With this gene set use Geneweaver to find the homology to human gene sets.
 
  The idea is to identify a mouse strain that has contrasting phenotypes for a syndrome of interest.
 
  * Making, keeping the data in FAIR:
  
  Mouse gene list
 
  * Making, keeping the application FAIR:
  
  Geneweaver
 
  * Making, keeping the data out FAIR:
  
  Human gene list
 
  Beginning with human data, a new exome is obtained for an individual with a disease, and the exomiser is used to obtain a prioritized list of pathogenic regulatory variants in Mendialian disease.  From these, a gene list could be derived. 
 
## Discussion:
Testing the data that are going into an application regarding whether that data adheres to the principles of FAIR, as determined by the FAIRShake application we will be introduced to today – Testing the application for its FAIRness

The path from mouse to human is the path we want to walk.
 
The path takes us from the Mouse Phenotype Database (MPD =phenome.jax.org) data with the mouse strains data for specific experiments.
 
From the mouse strain, we see the genes that are differentiated, affected with the strain.
With the genes, we can look at the pathway and we get  
 
Please find attached the studies that are available from the Mouse Phenotype Database, studies.csv
And we have the measurements that we can get from the
 
## Data Sources:

  https://phenome.jax.org/downloads
 
  https://phenome.jax.org/about/api
 
  https://phenome.jax.org/about/termsofuse
  https://osp.od.nih.gov/scientific-sharing/policies/
  https://phenome.jax.org/about/citing
 
## Background:

  * Ontoforce with their tool DisQover
  * Lifebit.ai with their tool deploit
  * Databiology with their integrated platform.
 
## Here are some details about containers: 

  https://biocontainers.pro/#/
 
  http://biocontainers-edu.biocontainers.pro/en/latest/best_practices.html
 
  http://biocontainers-edu.biocontainers.pro/en/latest/best_practices.html
  https://www.sylabs.io/2018/10/whitepaper-containerized-genomic-workflows-with-singularity-part-1/
  https://www.sylabs.io/2018/11/whitepaper-containerized-genomic-workflows-with-singularity-part-2/
  https://www.sylabs.io/2018/11/whitepaper-containerized-genomic-workflows-with-singularity-part-3/
 
  https://github.com/nf-core
 
## All applications and data will be given a FAIRShake
  https://fairshake.cloud/
 
