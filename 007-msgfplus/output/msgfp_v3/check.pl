#!c:/perl/bin/perl.exe
#
use strict;

open(IN, "KO_Rpick_Merged_I_.tsv") or die "can't open file"; 
my %new=(); 
my $e=0; 
my $t=20; 
my $line=<IN>;
while ($line=<IN>)
{
	chomp($line);
	my @line=split('\t',$line); 
	my $pep=$line[8];
	my $q=$line[15];
	$pep=~s/L/I/g; 
	while ($pep=~s/(.*)([\+]+)([0-9]+\.+[0-9]+)([A-Z]*\.[A-Z]*)//)
	{
		$pep="$1$4";
	}
	
	my $PEP=""; 
	if ($pep=~s/^([A-Z]*\-*)\.([A-Z]+)\.([A-Z]*\-*)//) #F.IMPVEDVFSISGR.G
	{
		$PEP=$2; 
	}
	else
	{
		print "error with peptide $pep\n"
; 	}
	if ($t<10)
	{
		print "PEP = $PEP\nQ = $q\n";
		$t++; 
	}
	$PEP=~s/\r\n\s\t\m\015//ge;
	if ($q<0.0001)
	{
		$new{$PEP}=1; 
	}
	else
	{
		$e++; 
	}
}
close IN; 
close OUT; 

my %old=(); 
open(IN, "Ralstonia_pickettii.blib.peptides_I.txt") or die "can't open file"; 
while (my $line=<IN>)
{
	chomp($line);
	$line=~s/L/I/g; 
	$line=~s/\r\n\s\m\t\015//ge;
	$old{$line}=1; 
	if ($t<30)
	{
		print "$line\n"; 
		$t++;
	}
}
close IN; 

open (OUT, ">KO_Rpick_Merged_qfilter_0.0001.txt") or die "can't open file"; 
open (NEW, ">only_new.txt") or die "can't open file"; 
open (OLD, ">only_old.txt") or die "can't open file"; 
my $n=0; 
my $y=keys(%new);
foreach my $key (keys %new)
{
	print OUT "$key\n"; 
	if ($old{$key}=~/\w/)
	{
		$n++; 
		print "$key\n";
		delete($old{$key});
	}
	else
	{
		print NEW "$key\n"; 
	}
}
close NEW; 
close OUT; 

foreach my $key (keys %old)
{
	print OLD "$key\n";
}

close OLD; 
print "number of pep overlaps between new and old = $n\nnumber of peps passing q filter = $y\n"; 