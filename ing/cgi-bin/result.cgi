#!/usr/bin/perl -w

use strict;
use constant { true => 1, false => 0 };
use CGI qw(:all);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

my @food_type = param('food_type');
my $canteen = param('canteen');
my $food_name = param('food_name');

my $metadata; # variable to save metadata.txt in db directory
my @table; # table to store data from metadata
my $table_rows = 0; # number of rows in metadata
my $err_flag1 = false; # to check if metadata file has opened succesfully

# First read metadata into an array
open($metadata, "./db/metadata.txt") or ($err_flag1 = true);

foreach my $line (<$metadata>) {
    chomp($line);
    if($line =~ m@^[#\s].*@) { next; } # don't read if it is commented line or empty line
    elsif($line =~ m@^[\d].*@) { # read line if starting with a number
        my @new_row = split(/ \/ /, $line); # split the line by " / "
        push @table, [@new_row];
        $table_rows ++;
    }
}

#print "!!!" + $err_flag1 + "\n";

# Check metadata comparing entered search keys

print header,
#    qq(<script language="JavaScript" src="../open_canteen.js"></script>),
    start_html(
        -title => 'Open Canteen:result1',
        -script => {-src => '../open_canteen.js'},
        -onLoad => "do_alert($err_flag1); do_print($table_rows)"
    ),
    h1('Open Canteen!'),
    hr,
    "Selected Food Types: @food_type",
    p(),
    "Selected Canteen: $canteen",
    p(),
    "Name of Food: $food_name",
    p();

print
    a({-href=>'/~kchangaa'}, "Go back to the main page."),
    br;
    end_html;






