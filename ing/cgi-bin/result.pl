#!/usr/bin/perl -w

use strict;
use CGI ':standard';
use <meta charset="utf-8">;
#use HTTP::Request::Common;
$cgi = CGI->new();
$cgi->header(-type=>"text/html");

@food_type = param('food_type');
@canteen = param('canteen');

print header,
    start_html('Open Canteen:result'),
    h1('Open Canteen!'),
    hr,
    "1111: $food_type",
    "2222: $canteen",
    a({-href=>'/'}, "Go back to the main page."),
    end_html;
