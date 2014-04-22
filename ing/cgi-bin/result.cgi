#!/usr/bin/perl -w

use strict;
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

my @food_type = param('food_type');
my $canteen = param('canteen');
my $food_name = param('food_name');

# First read metadata into an array


# Check metadata comparing entered search keys














print header,
    start_html('Open Canteen:result'),
    h1('Open Canteen!'),
    hr,
    "Selected Food Types: @food_type",
    p(),
    "Selected Canteen: $canteen",
    p(),
    "Name of Food: $food_name",
    p(),
    a({-href=>'/~kchangaa'}, "Go back to the main page."),
    end_html;


