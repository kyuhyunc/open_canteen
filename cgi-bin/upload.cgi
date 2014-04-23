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
my $pic_addr = param('');

my $metadata; # variable to save metadata.txt in db directory
my $new_food; # variable to create "id".txt file
my $table_rows = 0; # number of rows in metadata

# First count current rows in metadata.txt
open ($metadata, "../db/metadata.txt");

foreach my $line (<$metadata>) {
    chomp($line);
    if($line =~ m@^[#\s].*@) { next; } # don't read if it is commented line or empty line
    elsif($line =~ m@^[\d].*@) { # read line if starting with a number
        $table_rows ++;
    }
}
close $metadata;

# Open metadata.txt to append the new row
open ($metadata, ">>../db/metadata.txt");
print $metadata "\n$table_rows | $name | $type | $canteen | $ingredients";

close $metadata;

# Create new txt file in foods folder
open ($new_food, ">../db/foods/$table_rows.txt");
print $new_food "$name | $type | $canteen | $main_ingredient\n";
print $new_food "$ingredients\n";
print $new_food "\n";
print $new_food "0\n";
close $new_food;

print header,
    start_html();
print "<META http-equiv=\"refresh\" content=\"0;URL=http://ihome.ust.hk/~kchangaa\">";
print "hello world";
print end_html();
