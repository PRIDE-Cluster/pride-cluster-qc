#!/usr/bin/perl
use warnings; use strict;
#This script remove duplicated spectrum from file input. 
# Run the script: Perl deplucate_remover.pl [Name of the file]
# This script generate and output called total.norepeat.clustering

my %seen; 
my $count = 0; 
my $output;

open STDOUT, '>', "total.norepeat.clustering" or die "Can't create filehandle: $!";
while (  <> ) {
	s/;+/;/g;
	next if ( m/spectrum=(\d+)/ and $seen{$1}++ );
	if ( m/==Cluster==/ ) { 
		open ( $output, ">", "temp".$count++ ) or die $!; 
		select $output;
	}
	s/;+/;/g;
	print;
}
	close STDOUT
