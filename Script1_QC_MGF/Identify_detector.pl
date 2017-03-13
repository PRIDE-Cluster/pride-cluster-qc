

use strict;
use warnings;

open ( my $has_seq, '>', 'identify_sequences.txt' ) or die $!;
open ( my $no_seq, '>', 'unidentify_sequence.txt' ) or die $!;
my $seq_count = 0;
my $no_seq_count = 0;

local $/ = 'END:';


while ( <> ) {if ( m/SEQ/ ) {
        $seq_count++;
        select $has_seq;
        }
        else {
        $no_seq_count++;
        select $no_seq;
        }
#print current block to selected filehandle. 
        print;
}
print "SEQ: $seq_count\n";
print "No SEQ: $no_seq_count\n";

