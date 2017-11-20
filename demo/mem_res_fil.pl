#!/usr/bin/perl-w;
use strict;
use Getopt::Long;
my $lim=5;
my $qua=5;
my $splice=0.1;
GetOptions(
	'lim|l=i' => \$lim,
    'qua|q=i' => \$qua,
    'splice|s=s' => \$splice,
);
my($infile, $outfile, $logfile) = @ARGV;
my($tot, %cou, %inf, %res);
open (IN,$infile)||die"$!\n";
while (<IN>) {
	next if /^@/;
	chomp;
	my @spl = split(/\t/, $_);
	if ($spl[5] =~ /\*/) {
		$inf{$spl[0]} = 'Unm';
		next;
	}
	if ($spl[1] > 2000) {
		$res{Mul} += 1;
		next;
    }
	my($nhs, $len, $nmi) = (0, 0, 0);
	while ($spl[5] =~ /(\d+)[HS]/g) {
		$nhs += $1;
	}
	while ($spl[5] =~ /(\d+)[MISH]/g) {
		$len += $1;
       # print "####$len\n";
	}
	if ($spl[12] =~ /MD:.:(.+)/) {
		my $mid = $1;
		while ($spl[5] =~ /(\d+)D/g) {
			$mid =~ s/\^[ATCG]{$1}//;
		}
		$mid =~ s/\d+//g;
		$nmi = length($mid);
	}elsif ($spl[13] =~ /MD:.:(.+)/) {
		my $mid = $1;
		while ($spl[5] =~ /(\d+)D/g) {
			$mid =~ s/\^[ATCG]{$1}//;
		}
		$mid =~ s/\d+//g;
		$nmi = length($mid);
	}
	if (($nhs/$len) > $splice) {
		$inf{$spl[0]} = 'Spl';
	}elsif ($spl[4] < $qua) {
		$inf{$spl[0]} = 'Low';
	}elsif ($nmi > $lim) {
		$inf{$spl[0]} = 'Too';
	}
}
open (IN,$infile)||die"$!\n";
open (OUT, '>', $outfile)||die"$!\n";
open (LOG, '>', $logfile)||die"$!\n";
while (<IN>) {
	if (/^@/) {
		print OUT "$_";
		next;
	}
	chomp;
	my $out = $_;
	my @spl = split(/\t/, $_);
	next if $spl[1] > 2000;
	$tot += 1;
	if ($inf{$spl[0]} eq 'Unm') {
		$res{Unm} += 1;
	}elsif ($inf{$spl[0]} eq 'Spl') {
		$res{Spl} += 1;
	}elsif ($inf{$spl[0]} eq 'Low') {
		$res{Low} += 1;
	}elsif ($inf{$spl[0]} eq 'Too') {
		$res{Too} += 1;
	}else {
		$res{Pas} += 1;
		print OUT "$out\n";
	}
}
$res{Unm} += 0;
$res{Spl} += 0;
$res{Low} += 0;
$res{Too} += 0;
$res{Pas} += 0;
printf LOG ("Total_reads\t$tot\t100%\nPass_filter\t$res{Pas}\t%.2f%%\nUnmapped\t$res{Unm}\t%.2f%%\nMultiple_mapped\t$res{Mul}\t%.2f%%\nSplice\t$res{Spl}\t%.2f%%\nLow_map_quality\t$res{Low}\t%.2f%%\nToo_much_mismatch\t$res{Too}\t%.2f%%\n",$res{Pas}/$tot*100,$res{Unm}/$tot*100,$res{Mul}/$tot*100,$res{Spl}/$tot*100,$res{Low}/$tot*100,$res{Too}/$tot*100);
close LOG;
close OUT;
