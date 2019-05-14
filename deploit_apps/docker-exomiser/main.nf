#!/usr/bin/env nextflow

import groovy.json.*

/*
========================================================================================
                         lifebit-ai/exomiser
========================================================================================
 lifebit-ai/exomiser Exomiser pipeline.
 #### Homepage / Documentation
 https://github.com/lifebit-ai/exomiser
----------------------------------------------------------------------------------------
*/

params.vcf = "s3://hackathon-fair-exomiser/job-sample/Pfeiffer.vcf"
params.hpo = "HP:0001156','HP:0001363','HP:0011304','HP:0010055'"
params.exomiser_data = "${baseDir}/exomiser_data"

/*--------------------------------------------------
  Check input parameters
---------------------------------------------------*/

if(params.vcf) {
   Channel
      .fromPath( "${params.vcf}" )
      .ifEmpty { exit 1, "VCF file: ${params.vcf} not found"}
      .set { vcfChannel }
} else {
  exit 1, "please specify VCF file with --vcf parameter"
}

if(params.exomiser_data) {
   Channel
      .fromPath( "${params.exomiser_data}" )
      .ifEmpty { exit 1, "Exomiser data directory: ${params.vcf} not found"}
      .set { exomiserDataChannel }
} else {
  exit 1, "please specify Exomiser data directory with --exomiser_data parameter"
}

if(params.hpo) {
   Channel
      .from( "${params.hpo}" )
      .set { hpoChannel }
} else {
  exit 1, "please specify list of HPO IDs with --hpo parameter"
}

/*--------------------------------------------------
  Run containarised Exomiser
---------------------------------------------------*/

process exomiser {
  container 'lifebitai/exomiser'
  tag "${vcf}"
  publishDir 'results', mode: 'copy'

  input:
  file(vcf) from vcfChannel
  file('data') from exomiserDataChannel

  output:
  set file("*.html"), file("*.tsv"), file("*.vcf"), file("*.json") into sampleImputed

  script:
  """
  run.py -v $vcf
  """
}
