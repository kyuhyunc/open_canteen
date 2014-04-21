#!/usr/bin/perl -w

use strict;
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

#use HTTP::Request::Common qw(POST);
#use LWP::UserAgent;

#use HTTP::Request::Common;
#my $cgi = new CGI;
#$cgi->header(-type=>"text/html");

my @food_type = param('food_type');
my $canteen = param('canteen');

print header,
    start_html('Open Canteen:result'),
    h1('Open Canteen!'),
    hr,
    "Selected Food Types: @food_type",
    p(),
    "Selected Canteen: $canteen",
    p(),
    a({-href=>'/~kchangaa'}, "Go back to the main page."),
    end_html;
