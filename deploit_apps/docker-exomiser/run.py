#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import argparse
import subprocess
import os
from pprint import pprint

try:
    import yaml
except:
    print('Please install python-yaml:\n\t$ sudo apt-get install python-yaml')
    exit(1)

DIR = '/exomiser/'
SYM_LINK = ['data', 'results']


CONFIG_PATH = DIR + 'auto_config.yml'
BASE_COMMAND = ['java', '-Xms2g', '-Xmx4g', '-jar', DIR + 'exomiser-cli-12.0.0.jar',
                '--analysis',
                CONFIG_PATH]

usage_help = """
Testing argparse.
"""

yaml_data = """
## Exomiser Analysis Template.
# These are all the possible options for running exomiser. Use this as a template for
# your own set-up.
---
analysis:
    vcf: ../SchaMar.vcf
    ped:
    # AUTOSOMAL_DOMINANT, AUTOSOMAL_RECESSIVE, X_RECESSIVE or UNDEFINED
    modeOfInheritance: AUTOSOMAL_DOMINANT
    #FULL, SPARSE or PASS_ONLY
    analysisMode: PASS_ONLY
    #RAW_SCORE or RANK_BASED
    geneScoreMode: RAW_SCORE
    hpoIds: ['HP:0000842','HP:0000842']
    #Possible frequencySources:
    #Thousand Genomes project http://www.1000genomes.org/
    #   THOUSAND_GENOMES,
    #ESP project http://evs.gs.washington.edu/EVS/
    #   ESP_AFRICAN_AMERICAN, ESP_EUROPEAN_AMERICAN, ESP_ALL,
    #ExAC project http://exac.broadinstitute.org/about
    #   EXAC_AFRICAN_INC_AFRICAN_AMERICAN, EXAC_AMERICAN,
    #   EXAC_SOUTH_ASIAN, EXAC_EAST_ASIAN,
    #   EXAC_FINNISH, EXAC_NON_FINNISH_EUROPEAN,
    #   EXAC_OTHER
    frequencySources: [
        THOUSAND_GENOMES,
        ESP_AFRICAN_AMERICAN, ESP_EUROPEAN_AMERICAN, ESP_ALL,
        EXAC_AFRICAN_INC_AFRICAN_AMERICAN, EXAC_AMERICAN,
        EXAC_SOUTH_ASIAN, EXAC_EAST_ASIAN,
        EXAC_FINNISH, EXAC_NON_FINNISH_EUROPEAN,
        EXAC_OTHER
        ]
    #Possible pathogenicitySources: POLYPHEN, MUTATION_TASTER, SIFT, CADD, REMM
    #REMM is trained on non-coding regulatory regions
    #*WARNING* if you enable CADD, ensure that you have downloaded and installed the CADD tabix files
    #and updated their location in the application.properties. Exomiser will not run without this.
    pathogenicitySources: [POLYPHEN, MUTATION_TASTER, SIFT, REMM]
    #this is the recommended order for a genome-sized analysis.
    #all steps are optional
    steps: [
        #intervalFilter: {interval: 'chr10:123256200-123256300'},
        #geneIdFilter: {geneIds: [12345, 34567, 98765]},
        hiPhivePrioritiser: {runParams: 'human,mouse,fish,ppi'},
        #running the prioritiser followed by a prioritflmstyScoreFilter will remove genes
        #which are least likely to contribute to the phenotype defined in hpoIds, this will
        #dramatically reduce the time and memory required to analyse a genome.
        # 0.501 is a good compromise to select good phenotype matches and the best protein-protein interactions hits from hiPhive
        priorityScoreFilter: {priorityType: HIPHIVE_PRIORITY, minPriorityScore: 0.501},
        variantEffectFilter: {remove: [SYNONYMOUS_VARIANT, INTRON_VARIANT, INTERGENIC_VARIANT, NON_CODING_TRANSCRIPT_INTRON_VARIANT, CODING_TRANSCRIPT_INTRON_VARIANT, CODING_TRANSCRIPT_INTRON_VARIANT]},
        #regulatoryFeatureFilter removes all non-regulatory non-coding variants over 20Kb from a known gene.
        regulatoryFeatureFilter: {},
        #knownVariantFilter: {}, #removes variants represented in the database
        frequencyFilter: {maxFrequency: 0.0001},
        pathogenicityFilter: {keepNonPathogenic: false},
        #inheritanceFilter and omimPrioritiser should always run AFTER all other filters have completed
        #they will analyse genes according to the specified modeOfInheritance above- UNDEFINED will not be analysed.
        inheritanceFilter: {},
        #omimPrioritiser isn't mandatory.
        omimPrioritiser: {}
        #Other prioritisers: Only combine omimPrioritiser with one of these.
        #Don't include any if you only want to filter the variants.
        #hiPhivePrioritiser: {},
        # or run hiPhive in benchmarking mode:
        #hiPhivePrioritiser: {diseaseId: 'OMIM:101600', candidateGeneSymbol: FGFR2, runParams: 'human,mouse,fish,ppi'},
        #phenixPrioritiser: {}
        #exomeWalkerPrioritiser: {seedGeneIds: [11111, 22222, 33333]}
    ]
outputOptions:
    outputPassVariantsOnly: false
    #numGenes options: 0 = all or specify a limit e.g. 500 for the first 500 results
    numGenes: 0
    #outputPrefix options: specify the path/filename without an extension and this will be added
    # according to the outputFormats option. If unspecified this will default to the following:
    # {exomiserDir}/results/input-vcf-name-exomiser-results.html
    # alternatively, specify a fully qualifed path only. e.g. /users/jules/exomes/analysis
    outputPrefix: AD_SchaMar
    #out-format options: HTML, TSV-GENE, TSV-VARIANT, VCF (default: HTML)
    outputFormats: [HTML, JSON, TSV_GENE, TSV_VARIANT, VCF]
"""

variantEffectFilters = {
    'CHROMOSOME',
    'CHROMOSOME_NUMBER_VARIATION',
    'CODING_SEQUENCE_VARIANT',
    'CODING_TRANSCRIPT_INTRON_VARIANT',
    'CODING_TRANSCRIPT_INTRON_VARIANT',
    'CODING_TRANSCRIPT_INTRON_VARIANT',
    'CODING_TRANSCRIPT_INTRON_VARIANT',
    'CODING_TRANSCRIPT_VARIANT',
    'COMPLEX_SUBSTITUTION',
    'CONSERVED_INTERGENIC_VARIANT',
    'CONSERVED_INTRON_VARIANT',
    'CONSERVED_INTRON_VARIANT',
    'CUSTOM',
    'DIRECT_TANDEM_DUPLICATION',
    'DISRUPTIVE_INFRAME_DELETION',
    'DISRUPTIVE_INFRAME_INSERTION',
    'DOWNSTREAM_GENE_VARIANT',
    'EXON_LOSS_VARIANT',
    'EXON_VARIANT',
    'FEATURE_TRUNCATION',
    'FIVE_PRIME_UTR_PREMATURE_START_CODON_GAIN_VARIANT',
    'FIVE_PRIME_UTR_TRUNCATION',
    'FIVE_PRIME_UTR_VARIANT',
    'FRAMESHIFT_ELONGATION',
    'FRAMESHIFT_TRUNCATION',
    'FRAMESHIFT_VARIANT',
    'GENE_VARIANT',
    'INFRAME_DELETION',
    'INFRAME_INSERTION',
    'INITIATOR_CODON_VARIANT',
    'INTERGENIC_REGION',
    'INTERGENIC_VARIANT',
    'INTERNAL_FEATURE_ELONGATION',
    'INTRAGENIC_VARIANT',
    'INTRON_VARIANT',
    'INTRON_VARIANT',
    'MIRNA',
    'MISSENSE_VARIANT',
    'MNV',
    'NON_CODING_TRANSCRIPT_EXON_VARIANT',
    'NON_CODING_TRANSCRIPT_INTRON_VARIANT',
    'NON_CODING_TRANSCRIPT_INTRON_VARIANT',
    'NON_CODING_TRANSCRIPT_VARIANT',
    'RARE_AMINO_ACID_VARIANT',
    'REGULATORY_REGION_VARIANT',
    'SEQUENCE_VARIANT',
    'SPLICE_ACCEPTOR_VARIANT',
    'SPLICE_DONOR_VARIANT',
    'SPLICE_REGION_VARIANT',
    'SPLICING_VARIANT',
    'START_LOST',
    'STOP_GAINED',
    'STOP_LOST',
    'STOP_RETAINED_VARIANT',
    'STRUCTURAL_VARIANT',
    'SYNONYMOUS_VARIANT',
    'SYNONYMOUS_VARIANT',
    'TF_BINDING_SITE_VARIANT',
    'THREE_PRIME_UTR_TRUNCATION',
    'THREE_PRIME_UTR_VARIANT',
    'TRANSCRIPT_ABLATION',
    'TRANSCRIPT_VARIANT',
    'UPSTREAM_GENE_VARIANT',
    '_SMALLEST_HIGH_IMPACT',
    '_SMALLEST_LOW_IMPACT',
    '_SMALLEST_MODERATE_IMPACT',
}

def get_base_command():
    return [i for i in BASE_COMMAND]

def parse_arguments():
    parser = argparse.ArgumentParser(description=usage_help, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--prioritiser',
                        choices=['hiphive', 'phive', 'phenix'])
    parser.add_argument('-I', choices=['AR', 'AD', 'X'])
    parser.add_argument('-F', type=int, metavar='1-100')
    parser.add_argument('--hpo-ids', action='store')
    parser.add_argument('-v', required=True, help='Path to .vcf file')
    parser.add_argument('--full-analysis', choices=['true', 'false'])
    parser.add_argument('--out-format', choices=['HTML'])
    parser.add_argument('--mode-of-inheritance',
                        choices=['AUTOSOMAL_DOMINANT', 'AUTOSOMAL_RECESSIVE',
                                 'X_RECESSIVE', 'UNDEFINED'],
                        help='Set mode of inheritance at line 9 in config file')
    parser.add_argument('-a', action='store_true', help='Sets analysisMode')
    parser.add_argument('-p', help='Path to .ped file')
    parser.add_argument('-c', help="If choosen sets hiPhivePrioritiser to: `{runParams: 'human,mouse,fish,ppi', candidateGeneSymbol: <entered value>}`")
    parser.add_argument('-d', help="If choosen sets hiPhivePrioritiser to: `{runParams: 'human,mouse,fish,ppi', diseaseId: 'OMIM:101600'}`")
    parser.add_argument('-f', nargs='+', choices=variantEffectFilters, help='variantEffectFilter parameter')
    parser.add_argument('-m', action='store_true', help='Make 3rd script run using X_RECESSIVE')
    parser.add_argument('--freq_ad', type=float, default=0.0001, help='maxFrequency for AUTOSOMAL_DOMINANT')
    parser.add_argument('--freq_ar', type=float, default=0.03, help='maxFrequency for AUTOSOMAL_RECESSIVE')
    parser.add_argument('--freq_xr', type=float, default=0.0003, help='maxFrequency for X_RECESSIVE')
    parser.add_argument('--config-path', help='Custom path to config file')
    parser.add_argument('--hpo', nargs='+', help='hpoIds')

    return parser.parse_args()

def make_full_command(base, args):
    if args.prioritiser:
        base.append('--prioritiser')
        base.append(args.prioritiser)
    if args.I:
        base.append('-I')
        base.append(args.I)
    if args.F:
        base.append('-F')
        base.append(str(args.F))
    if args.hpo_ids:
        base.append('--hpo-ids')
        base.append(args.hpo_ids)
    if args.v:
        base.append('-v')
        base.append(args.v)
    if args.full_analysis:
        base.append('--full-analysis')
        base.append(args.full_analysis)
    if args.out_format:
        base.append('--out-format')
        base.append(args.out_format)

    WORKD_DIR = os.getcwd()
    DATA_DIR = WORKD_DIR + '/data'
    base.append('--exomiser.data-directory='+DATA_DIR)

    return base

def build_conf(args, conf):
    conf = dict(conf)

    conf['analysis']['vcf'] = args.v

    if args.p:
        conf['analysis']['ped'] = args.p

    if args.a:
        conf['analysis']['analysisMode'] = 'FULL'
    else:
        conf['analysis']['analysisMode'] = 'PASS_ONLY'

    if args.mode_of_inheritance:
        conf['analysis']['modeOfInheritance'] = args.mode_of_inheritance

    if args.c:
        conf['analysis']['steps'][0]['hiPhivePrioritiser']['candidateGeneSymbol'] = args.c

    if args.d:
        conf['analysis']['steps'][0]['hiPhivePrioritiser']['diseaseId'] = args.d

    if args.f:
        conf['analysis']['steps'][2]['variantEffectFilter']['remove'] = list(set(args.f))

    if args.hpo:
        conf['analysis']['hpoIds'] = args.hpo

    input_name_no_ext = os.path.basename(args.v)
    input_name_no_ext = input_name_no_ext.split('.')[0]
    if args.run_mode == 1:
        conf['outputOptions']['outputPrefix'] = 'AD_{}'.format(input_name_no_ext)
        conf['analysis']['steps'][4]['frequencyFilter']['maxFrequency'] = args.freq_ad
    elif args.run_mode == 2:
        conf['outputOptions']['outputPrefix'] = 'AR_{}'.format(input_name_no_ext)
        conf['analysis']['steps'][4]['frequencyFilter']['maxFrequency'] = args.freq_ar
    elif args.run_mode == 3:
        conf['outputOptions']['outputPrefix'] = 'XR_{}'.format(input_name_no_ext)
        conf['analysis']['steps'][4]['frequencyFilter']['maxFrequency'] = args.freq_xr

    return conf

def write_config_file(args):
    config_path = args.config_path or CONFIG_PATH
    print('\nWriting to config file ' + config_path)
    conf = yaml.safe_load(yaml_data)
    with open(config_path, 'w') as f:
        new_conf = build_conf(args, conf)
        print('Using config:')
        pprint(new_conf)
        yaml.safe_dump(new_conf, f)

def run(args):
    write_config_file(args)

    #try:
    #    for i in SYM_LINK:
    #        os.symlink(DIR + i, i)
    #except:
    #    pass

    base_command = get_base_command()
    command = make_full_command(base_command, args)
    pcom = ''
    for i in command:
        pcom += i + ' '

    print('\nCalling: ' + pcom)
    subprocess.call(command)

    #os.unlink('./data')
    #for i in SYM_LINK:
    #    os.unlink(i)

def main():
    args = parse_arguments()
    args.run_mode = 0
    if  args.mode_of_inheritance is None:
        args.mode_of_inheritance = 'AUTOSOMAL_DOMINANT'
        args.run_mode = 1
        run(args)
        args.mode_of_inheritance = 'AUTOSOMAL_RECESSIVE'
        args.run_mode = 2
        run(args)
        if args.m:
            args.mode_of_inheritance = 'X_RECESSIVE'
            args.run_mode = 3
            run(args)
    else:
        run(args)

def test_build_conf():
    class Args():
        v = 'file.vcf'
        p = 'file.ped'
        a = False
        mode_of_inheritance = 'some mode'
        c = 'candidate'
        d = 'diseaseId'
        f = ['a', 'b']
        hpo = ['hpo0', 'hpo1']
        run_mode = 0
    conf = yaml.safe_load(yaml_data)
    build_conf(Args(), conf)
    args2 = Args()
    args2.a = True
    build_conf(args2, conf)
    args = Args()
    args.run_mode = 1
    build_conf(args2, conf)
    args.run_mode = 2
    build_conf(args2, conf)

if __name__ == '__main__':
    main()