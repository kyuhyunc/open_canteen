#!/usr/bin/perl -w

use strict;
use constant { true => 1, false => 0 };
use CGI qw(:all);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

my @food_type = param('food_type');
my $ingredient = param('ingredient');
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
# 1. Check food name condition: column2
if($food_name !~ m/^[\s].*/) { # if input is not a blank or not starting with blank
    for(my $i=0; $i<$table_rows; $i++) {
        if($table[$i][1] !~ m/$food_name/) {
            splice(@table, $i, 1);
            $i--; $table_rows--;
        }
    }
} 
# 2. Check canteen condition: column4
if($canteen ne "any") {
    for(my $i=0; $i<$table_rows; $i++) {
        if($table[$i][3] ne $canteen) {
            splice(@table, $i, 1);
            $i--; $table_rows--;
        }
    }
}
# 3. Check food type condition: column3
if($food_type[0] ne "any") {
    for(my $i=0; $i<$table_rows; $i++) {
        my $flag = false;
        for(my $j=0; $j<scalar @food_type; $j++) {
            if($table[$i][2] eq $food_type[$j]) { $flag = true; } 
        }
        if($flag eq false) {
            splice(@table, $i, 1);
            $i--; $table_rows--;
        }
    }   
}
# 4. Check ingredient condition: column5
if($ingredient ne "any") {
    for(my $i=0; $i<$table_rows; $i++) {
        if($table[$i][4] ne $ingredient) {
            splice(@table, $i, 1);
            $i--; $table_rows--;
        }
    }        
}

print header,
#    qq(<script language="JavaScript" src="../open_canteen.js"></script>),
    start_html(
        -title => 'Open Canteen:result1',
        -script => {-src => '../open_canteen.js'},
        -onLoad => "do_alert($err_flag1); do_print($table_rows)"
#        -onLoad => "do_alert($err_flag1)"
    ),
    h1('Open Canteen!'),
    hr,
    "Selected Food Types: @food_type",
    p(),
    "Selected Main Ingredient: $ingredient",
    p(),
    "Selected Canteen: $canteen",
    p(),
    "Name of Food: $food_name",
    hr;

print
    a({-href=>'/~kchangaa'}, "Go back to the main page."),
    br;
    end_html;






