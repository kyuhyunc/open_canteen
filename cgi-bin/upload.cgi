#!/usr/local/bin/perl5 -w
# upload food page

use CGI qw(:standard);

print header();
print start_html(-title=>'Upload'),
  h1('Upload'),
  hr,
  start_form,
  "Food Name :", 
    textfield(-name=>'name', -default=>'food name'),
  p,
  "Food Type :", 
    popup_menu(-name=>'type', -values=>['Soup Noodle','Fried Noodle','Rice','Fried Rice',
    'Congee','Curry','Dish','Steak','Else']),
  p,
  "Main Ingredient :",
    popup_menu(-name=>'main_ingredient', -values=>['Beef','Pork','Chicken','Duck','Fish','Vegetable','Else']),
  p,
  "Which Canteen :",
    popup_menu(-name=>'canteen', -values=>['canteen1','canteen2']),
  p,
  "Keywords :",
    textfield(-name=>'keywords', -default=>'keyword1,keyword2,...'),
  p,
  "ingredients :",
    textfield(-name=>'ingredients', -default=>'ingredient1,ingredient2,...'),
  submit('Upload'), reset('reset'),
  end_form,
  hr;
  if (param()) {
    my $name = param('name');
    my $type = param('type');
    my $main_ingredient = param('main_ingredient');
    my $canteen = param('canteen');
    my $keywords = param('keywords');
    my $ingredients = param('ingredients');
    
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