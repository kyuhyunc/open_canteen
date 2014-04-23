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
    popup_menu(-name=>'ingredient', -values=>['Beef','Pork','Chicken','Duck','Fish','Vegetable','Else']),
  p,
  "Which Canteen :",
    popup_menu(-name=>'canteen', -values=>['canteen1','canteen2']),
  p,
  "Any Comment? :",
    textfield(-name=>'comment', -default=>'optional'),
  p,
  submit('Upload'), reset('reset'),
  end_form,
  hr;
  if (param()) {
    my $name = param('name');
    my $type = param('type');
    my $ingredient = param('ingredient');
    my $canteen = param('canteen');
    my $comment = param('comment');
    
    open (metadata, '>>./db/metadata.txt');
    print metadata "100 / $name / $type / $canteen / $ingredient\n";
  }
print end_html();