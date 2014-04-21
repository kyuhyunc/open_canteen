#!/usr/bin/perl

use CGI ':standard';

print header,
  start_html('index_html'),
   h1('Open Canteen!'),
   hr,
   img({-src=>'./intro.jpg'}),
   hr,
print_canteen_type();
print_main_type();
print end_html;

#check condition
print "$canteen_type";
print "$main_type";
sub print_canteen_type {
    if (param) {
  $canteen_type = 'any' if param('any');   
	$canteen_type = 'meat' if param('meat');
	$canteen_type = 'fish' if param('fish');
	$canteen_type = 'chicken' if param('chicken');
	$canteen_type = 'vegetarian' if param('vegetarian');
    }
}

sub print_main_type {
    print start_form,
    "Which ingredient?: ",
    checkbox(-name=>'any',-checked=>1),
    checkbox(-name=>'meat',-checked=>1),
    checkbox(-name=>'fish',-checked=>1),
    checkbox(-name=>'chicken',-checked=>1),
    checkbox(-name=>'vegetarian',-checked=>1),
    p(),
    "Which canteen?: ",
    radio_group(-name=>'type',
                -values=>['canteen1','canteen2']),
    p(),
    reset(-name=>'Reset'),
    submit(-name=>'Set'),
    end_form;
}