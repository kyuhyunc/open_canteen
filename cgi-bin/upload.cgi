#!/usr/bin/perl -w
# upload food page

use strict;
use constant { true => 1, false => 0 };
use CGI qw(:all);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use File::Basename;

my $cgi = new CGI;

# get all values from the front page
my $upload_dir = "../images";
my $name = param('food_name_');
my $type = param('food_type_');
my $main_ingredient = param('ingredient_');
my $canteen = param('canteen_');
my $ingredients = param('ingredients_');
my $pic_addr = $cgi->param('photo');
my ($file_name, $file_path, $file_extension) = fileparse ($pic_addr, '..*');
$pic_addr = $file_name.$file_extension;
my $metadata; # variable to save metadata.txt in db directory
my $new_food; # variable to create "id".txt file
my $table_rows = 0; # number of rows in metadata
my $upload_filehandle = $cgi->upload("photo");

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
print $new_food "$upload_dir/$pic_addr\n";
print $new_food "0\n";
close $new_food;

open (UPLOADFILE, ">$upload_dir/$pic_addr") or die "$!";
binmode UPLOADFILE;

while (<$upload_filehandle>) {
  print UPLOADFILE;
}

print header,
    start_html();
print "<META http-equiv=\"refresh\" content=\"0;URL=../\">";
print end_html();
