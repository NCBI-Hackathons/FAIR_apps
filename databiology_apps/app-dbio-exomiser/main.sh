#!/bin/bash
set -euo pipefail
# Exomiser entrypoint
# Juan Caballero <juan.caballero@databiology.com>
# (C) Databiology 2019

SCRATCH=/scratch
INPUTDIR=/scratch/input
RESULTDIR=/scratch/results
WORKDIR=/scratch/work
EXOMISERDIR=/opt/databiology/apps/exomiser
EXOMISERDATA=/ref/exomiser

# Functions
falseexit () {
   echo "Application failed: $1"
   exit 1
}

HOST=$(jq -r '.hostbase' "$SCRATCH/dbe.json")

# Check if we are possibly running in parallel mode
MULTIINPUT=$(jq -r '.["WRAPPERCREATOR"] .groupby' "$SCRATCH/parameters.json")

# Define max memory to use
MEM=$( free -g | head -2 | tail -n 1 | perl -ne 'print $1 if (/(\d+)/)' )
MEM="$MEM""g"

# NP=$(nproc)

# Creating WORKDIR
if [ ! -d "$WORKDIR" ]; then mkdir -p $WORKDIR; fi
cd "$WORKDIR" || falseexit "Cannot change dir to $WORKDIR"

# Link reference data
ln -s "$EXOMISERDATA"/* "$EXOMISERDIR/data/"

# Read parameters from parameters.json
CONFIG=''

# CONFIG analysis
GENOME=$(jq -r '.["APPLICATION"] .genome' $SCRATCH/parameters.json)
if [ "$GENOME" != "null" ]; then CONFIG="  genomeAssembly: $GENOME"; fi

HPOLIST=''
HPO=$(jq -r '.["APPLICATION"] .hpo' $SCRATCH/parameters.json)
if [ "$HPO" != "null" ]
then
    for H in $HPO
    do
        HPOLIST="$HPOLIST '$H',"
    done
    HPOLIST=$( echo "$HPOLIST" | perl -pe "s/^\s+//; s/,$//" )
fi

METAHPO=$(jq -r '.["APPLICATION"] .metahpo' $SCRATCH/parameters.json)
if [ "$METAHPO" == "true" ]
then
    HPO=$( perl -lane 'print $1 if (/(HP:\d+)/)' $SCRATCH/resources.json | sort | uniq | perl -pe 's/\n/ /g' | perl -pe 's/ $//' )
    for H in $HPO
    do
        HPOLIST="$HPOLIST '$H',"
    done
    HPOLIST=$( echo "$HPOLIST" | perl -pe "s/^\s+//; s/,$//" )
fi
CONFIG="$CONFIG\n  hpoIds: [$HPOLIST]"

INHER=$(jq -r '.["APPLICATION"] .inheritance' $SCRATCH/parameters.json)
if [ "$INHER" != "null" ]; then CONFIG="$CONFIG\n  inheritanceModes: {$INHER}"; else CONFIG="$CONFIG\n  inheritanceModes: {}"; fi

ANALYSIS=$(jq -r '.["APPLICATION"] .analysis' $SCRATCH/parameters.json)
if [ "$ANALYSIS" != "null" ]; then CONFIG="$CONFIG\n  analysisMode: $ANALYSIS"; fi

POPFREQ=$(jq -r '.["APPLICATION"] .popfreq' $SCRATCH/parameters.json)
if [ "$POPFREQ" != "null" ]; then CONFIG="$CONFIG\n  frequencySources: [$POPFREQ]"; fi

PATHSOURCE=$(jq -r '.["APPLICATION"] .pathsource' $SCRATCH/parameters.json)
if [ "$PATHSOURCE" != "null" ]; then CONFIG="$CONFIG\n  pathogenicitySources: [$PATHSOURCE]"; fi

# CONFIG steps
CONFIG="$CONFIG\n  steps: ["

INTERVAL=$(jq -r '.["APPLICATION"] .interval' $SCRATCH/parameters.json)
if [ "$INTERVAL" != "null" ]; then CONFIG="$CONFIG\n    intervalFilter: {interval: '$INTERVAL'},"; fi

GENES=$(jq -r '.["APPLICATION"] .genes' $SCRATCH/parameters.json)
if [ "$GENES" != "null" ]
then
    GENLIST=''
    for G in $GENES
    do
        GENLIST="$GENLIST '$G',"
    done
    GENLIST=$( echo "$GENLIST" | perl -pe "s/^\s+//; s/,$//" )
    CONFIG="$CONFIG\n    genePanelFilter: {geneSymbols: [$GENLIST]},"
fi

MINQUAL=$(jq -r '.["APPLICATION"] .minqual' $SCRATCH/parameters.json)
if [ "$MINQUAL" != "null" ]; then CONFIG="$CONFIG\n    qualityFilter: {minQuality: $MINQUAL},"; fi

VARFILTER=$(jq -r '.["APPLICATION"] .varfilter' $SCRATCH/parameters.json)
if [ "$VARFILTER" != "null" ]; then CONFIG="$CONFIG\n    variantEffectFilter: {remove: [$VARFILTER]},"; fi

MAXFREQ=$(jq -r '.["APPLICATION"] .maxfreq' $SCRATCH/parameters.json)
if [ "$MAXFREQ" != "null" ]; then CONFIG="$CONFIG\n    frequencyFilter: {maxFrequency: $MAXFREQ},"; fi

REGFILTER=$(jq -r '.["APPLICATION"] .regfilter' $SCRATCH/parameters.json)
if [ "$REGFILTER" == "true" ]; then CONFIG="$CONFIG\n    regulatoryFeatureFilter: {},"; fi

KNOWN=$(jq -r '.["APPLICATION"] .knownvar' $SCRATCH/parameters.json)
if [ "$KNOWN" == "true" ]; then CONFIG="$CONFIG\n    knownVariantFilter: {},"; fi

NOPAT=$(jq -r '.["APPLICATION"] .keepnopath' $SCRATCH/parameters.json)
if [ "$NOPAT" == "true" ]; then CONFIG="$CONFIG\n    pathogenicityFilter: {keepNonPathogenic: true},"; fi

INHFILTER=$(jq -r '.["APPLICATION"] .inhfilter' $SCRATCH/parameters.json)
if [ "$INHFILTER" == "true" ]; then CONFIG="$CONFIG\n    inheritanceFilter: {},"; fi

OMIMPRIOR=$(jq -r '.["APPLICATION"] .omimprior' $SCRATCH/parameters.json)
if [ "$OMIMPRIOR" == "true" ]; then CONFIG="$CONFIG\n    omimPrioritiser: {},"; fi

METPARAM=$(jq -r '.["APPLICATION"] .methodparam' $SCRATCH/parameters.json)
if [ "$METPARAM" == "null" ]; then METPARAM=''; fi

METHOD=$(jq -r '.["APPLICATION"] .method' $SCRATCH/parameters.json)
case "$METHOD" in
    phenix)
        CONFIG="$CONFIG\n    phenixPrioritiser: {$METPARAM},"
    ;;
    hiPhive)
        CONFIG="$CONFIG\n    hiPhivePrioritiser: {$METPARAM},"
    ;;
    phive)
        CONFIG="$CONFIG\n    phivePrioritiser: {$METPARAM},"
    ;;
    exomeWalker)
        CONFIG="$CONFIG\n    exomeWalkerPrioritiser: {$METPARAM},"
    ;;
esac

PRIORFILTER=$(jq -r '.["APPLICATION"] .priorscore' $SCRATCH/parameters.json)
if [ "$PRIORFILTER" != "null" ]; then CONFIG="$CONFIG\n    priorityScoreFilter: {$PRIORFILTER},"; fi

# Remove last comma
CONFIG=$( echo "$CONFIG" | perl -pe "s/,$/\n  ]/" )

## CONFIG output
CONFIG="$CONFIG\noutputOptions:"

PASS=$(jq -r '.["APPLICATION"] .pass' $SCRATCH/parameters.json)
if [ "$PASS" == "true" ]; then CONFIG="$CONFIG\n  outputPassVariantsOnly: true"; else CONFIG="$CONFIG\n  outputPassVariantsOnly: false"; fi

NUM=$(jq -r '.["APPLICATION"] .num' $SCRATCH/parameters.json)
if [ "$NUM" != "null" ]; then CONFIG="$CONFIG\n  numGenes: $NUM"; else CONFIG="$CONFIG\n  numGenes: 0"; fi

FORMAT=$(jq -r '.["APPLICATION"] .format' $SCRATCH/parameters.json)
if [ "$FORMAT" != "null" ]; then CONFIG="$CONFIG\n  outputFormats: [$FORMAT]"; else CONFIG="$CONFIG\n  outputFormats: [HTML]"; fi

PREFIX=$(jq -r '.["APPLICATION"] .outname' $SCRATCH/parameters.json)

PED=$(jq -r '.["APPLICATION"] .pedanalysis' $SCRATCH/parameters.json)

OUTVCF=$(jq -r '.["APPLICATION"] .mergedvcf' $SCRATCH/parameters.json)
if [ "$OUTVCF" == "null" ]; then OUTVCF="combined"; fi

if [ "$PED" == "true" ]
then
    echo "using Pedigree analysis"

    CMD="/usr/local/bin/json2ped.pl /scratch/resources.json resources.ped"
    echo "$CMD"
    bash -c "$CMD" || falseexit

    echo "================= PED FILE =================="
    cat resources.ped
    echo "============================================="

    VCFFILES=' '
    while read -r VCF
    do
        ln -s "$VCF" "$WORKDIR/"
        if [ -f "$VCF.tbi" ]
        then
            echo "found $VCF / $VCF.tbi"
            ln -s "$VCF.tbi" "$WORKDIR/"
        else
            VCF=$(basename "$VCF")
            echo "indexing $WORKDIR/$VCF"
            CMD="tabix $WORKDIR/$VCF"
            echo "$CMD"
            bash -c "$CMD" || falseexit
        fi
        VCF=$(basename "$VCF")
        VCFFILES="$VCFFILES $VCF"
    done < <(find "$INPUTDIR" -name "*.vcf.gz")

    CMD="bcftools merge -O v -o $OUTVCF $VCFFILES"
    echo "$CMD"
    $CMD || falseexit

    rm ./*.vcf*

    mv "$OUTVCF" "$OUTVCF.vcf"
else
    while read -r VCFGZ
    do
        echo "Uncompresing $VCFGZ"
        VCF=$(basename "$VCFGZ" .gz)
        gunzip -c "$VCFGZ" > "$WORKDIR/$VCF"
    done < <(find "$INPUTDIR" -name "*vcf.gz")

    while read -r VCF
    do
        echo "found $VCF"
        ln -s "$VCF" "$WORKDIR/$(basename $VCF)"
    done < <(find "$INPUTDIR" -name "*vcf")
fi

PROC=0
for VCF in *.vcf
do
    if [ -e "$VCF" ]
    then
        if [ "$PREFIX" == "null" ]
        then
            OUT=$(basename "$VCF" .vcf)
        else
            OUT="$PREFIX-"$(basename "$VCF" .vcf)
        fi

        if [ "$MULTIINPUT" != "null" ]
        then # in this case we cannot be sure if there is another file with identical name
            OUT="${OUT}-${RANDOM}"
        else
            if [ -e "${WORKDIR}/${OUT}.exomiser.html" ]
            then # file already exists
                OUT="${OUT}-${RANDOM}"
            fi
        fi

        PED="resources.ped";
        if [ -e "$PED" ]; then PED="ped: $PED"; else PED="ped: "; fi

        OUTFILE="outputPrefix: $WORKDIR/$OUT.exomiser"
        echo "writing configuration for $OUT"
        {
            echo "---"
            echo "analysis:"
            echo "  vcf: $WORKDIR/$VCF"
            echo "  $PED"
            echo "  proband: "
            echo -e "$CONFIG"
            echo "  $OUTFILE"
        } > "$OUT.yml"

        CMD="java -Xms2g -Xmx$MEM -jar $EXOMISERDIR/exomiser-cli.jar --analysis $WORKDIR/$OUT.yml"
        echo "$CMD"
        bash -c "$CMD" || falseexit
        mv "$OUT.yml" "$RESULTDIR"
    fi
    #rm "$VCF"
    PROC=1
done

if [ "$PROC" == "0" ]
then
    falseexit "No inputs detected"
fi

mv $WORKDIR/* $RESULTDIR

cd $RESULTDIR
cp $SCRATCH/parameters.json .
cp $SCRATCH/workunit.json .
cp $SCRATCH/dbe.json .
rm *.vcf
