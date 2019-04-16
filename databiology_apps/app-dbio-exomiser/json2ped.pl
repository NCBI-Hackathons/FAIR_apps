#!/usr/bin/perl

# convert resource.json to ped file
# Juan Caballero <juan.caballero@databiology.com>
# (C) Databiology Inc. 2017

use strict;
use warnings;
use autodie;
use JSON::Parse 'json_file_to_perl';

$ARGV[1] or die "use json2ped.pl resources.json output.ped\n";
my $json_file = shift @ARGV;
my $out_file  = shift @ARGV;

my ($sample, $fam, $ind, $fat, $mot, $sex, $phen);

my $refh = json_file_to_perl($json_file);

my %ped = ();
my %ind = ();
foreach my $item ( @{ $refh } ) {
	$sample = "NA";
    if (defined $item->{'extract'}->{'sample'}->{'name'}) {
        $sample = $item->{'extract'}->{'sample'}->{'name'};		
	}
	next if ($sample eq "NA");
	
	$ind = "NA";
    if (defined $item->{'extract'}->{'sample'}->{'individualid'}) {
        $ind = $item->{'extract'}->{'sample'}->{'individualid'};		
	}
	
    $sex = 0;
    if (defined $item->{'extract'}->{'sample'}->{'sex'}->{'name'}) {
        my $sex_v = lc $item->{'extract'}->{'sample'}->{'sex'}->{'name'};
		if    ($sex_v eq 'female') { $sex = 2; }
		elsif ($sex_v eq   'male') { $sex = 1; }
    }
    
    $phen  = 0;
    if (defined $item->{'extract'}->{'sample'}->{'diseasestate'}->{'name'}) {
        my $phen_v = lc $item->{'extract'}->{'sample'}->{'diseasestate'}->{'name'};
		if    ($phen_v eq 'affected') { $phen = 2; }
		elsif (($phen_v eq 'unaffected') or ($phen_v eq 'non affected')) { $phen = 1; }
    }
	
	$fam = "NA";
	$fat = "NA";
	$mot = "NA";
	
	foreach my $custom ( @{ $item->{'extract'}->{'sample'}->{'customattribute'} } ) {
		my $cname = lc $custom->{'name'};
		if    ($cname eq 'familyid') { $fam = $custom->{'value'}; }
		elsif ($cname eq 'fatherid') { $fat = $custom->{'value'}; }
		elsif ($cname eq 'motherid') { $mot = $custom->{'value'}; }
	}
	
    $ped{$sample}{ 'sex'} = $sex;
    $ped{$sample}{ 'fam'} = $fam;
    $ped{$sample}{ 'fat'} = $fat;
    $ped{$sample}{ 'mot'} = $mot;
    $ped{$sample}{'phen'} = $phen;
    $ind{$ind} = $sample;
}

open (my $out, ">", $out_file);
print $out "#FamilyId\tIndividualId\tFatherId\tMotherId\tSex\tPhenotype\n";

foreach $sample (keys %ped) {
	$fam  = 0;
	$fat  = 0;
	$mot  = 0;
	$sex  = 0;
	$phen = 0;
	
	$fam  = $ped{$sample}{ 'fam'} if (defined $ped{$sample}{ 'fam'});
	$sex  = $ped{$sample}{ 'sex'} if (defined $ped{$sample}{ 'sex'});
	$phen = $ped{$sample}{'phen'} if (defined $ped{$sample}{'phen'});
	
	$fat  = $ind{ $ped{$sample}{'fat'} } if (defined $ind{ $ped{$sample}{'fat'} });
	$mot  = $ind{ $ped{$sample}{'mot'} } if (defined $ind{ $ped{$sample}{'mot'} });
	
	$fat = 0 if ($fat eq "NA");
	$mot = 0 if ($mot eq "NA");
	
	print $out join "\t", $fam, $sample, $fat, $mot, $sex, $phen;
	print $out "\n";
}
close $out;
