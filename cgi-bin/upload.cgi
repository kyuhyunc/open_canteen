#!/usr/bin/perl -w
# upload food page

use strict;
use constant { true => 1, false => 0 };
use CGI qw(:all);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

my $cgi = new CGI;

# get all values from the front page
my $name = param('food_name_');
my $type = param('food_type_');
my $main_ingredient = param('ingredient_');
my $canteen = param('canteen_');
my $ingredients = param('ingredients_');

my $metadata; # variable to save metadata.txt in db directory
my $table_rows = 0; # number of rows in metadata

# First read metadata into an array
open($metadata, "./db/metadata.txt");

foreach my $line (<$metadata>) {
    chomp($line);
    if($line =~ m@^[#\s].*@) { next; } # don't read if it is commented line or empty line
    elsif($line =~ m@^[\d].*@) { # read line if starting with a number
        $table_rows ++;
    }
}
    
    open (metadata, '>>./db/metadata.txt');
    print metadata "$table_rows / $name / $type / $canteen / $ingredient\n";
    close (metadata);
    
    open (new_food, ">./db/foods/$table_rows.txt");
    print new_food "$name | $type | $canteen | $main_ingredient\n";
    print new_food "$keywords\n";
    print new_food "$ingredients\n";
    print new_food "\n";
    print new_food "0\n";
    close (new_food);
  }
print end_html();
