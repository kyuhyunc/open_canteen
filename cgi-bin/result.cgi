#!/usr/bin/perl -w

use strict;
use constant { true => 1, false => 0 };
use CGI qw(:all);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

my $cgi = new CGI;

my @food_type = param('food_type');
my $ingredient = param('ingredient');
my $canteen = param('canteen');
my $food_name = param('food_name');

my $metadata; # variable to save metadata.txt in db directory
my @table; # table to store data from metadata
my $table_rows = 0; # number of rows in metadata
my $err_flag = false; # to check if metadata file has opened succesfully

# First read metadata into an array
open ($metadata, "../db/metadata.txt") or ($err_flag = true);

foreach my $line (<$metadata>) {
    chomp($line);
    if($line =~ m@^[#\s].*@) { next; } # don't read if it is commented line or empty line
    elsif($line =~ m@^[\d].*@) { # read line if starting with a number
        my @new_row = split(/ \| /, $line); # split the line by " / "
        push @table, [@new_row];
        $table_rows ++;
    }
}

close $metadata;

#print "!!!" + $err_flag + "\n";

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
        -title=>'Open Canteen:result',
        -script=>{-src=>'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js'},
        #-script=>{-src=>'../open_canteen.js'},
        #-link=>{'src' => '../open_canteen.css'},
        #-style=>{-src => '../open_canteen.css'},
        #-onLoad=>"do_alert($err_flag); do_print($table_rows)"
        #-base=>'_parent',
        -target=>'_top',
        -onLoad=>"do_alert($err_flag)"
    );

print "<script language=\"JavaScript\" src=\"../open_canteen.js\"></script>";

print $cgi->Link({-rel=>'stylesheet', -type=>'text/css', -href=>'../open_canteen.css'}),
    
    $cgi->start_div({-id=>'container'}),
    $cgi->start_div({-id=>'content'}),
    $cgi->div({-id=>'header'}, h1('Open Canteen!'));
        
print $cgi->start_fieldset(),
    $cgi->start_legend(),
    $cgi->start_strong(),
    "Selected Keys",
    $cgi->end_strong(),
    $cgi->end_legend(),
    $cgi->start_table({-width=>"100%"}),
    $cgi->start_Tr({-align=>'CENTER', -valign=>'TOP'}),
    th(['Food Types', 'Main Ingredient', 'Canteen', 'Name of Food']),
    $cgi->end_Tr();

for(my $i=0; $i<scalar @food_type; $i++) {
    if($i==0) {
        print $cgi->start_Tr(),
            td({-align=>'CENTER', -valign=>'TOP'}, [$food_type[$i], $ingredient, $canteen, $food_name]),
            $cgi->end_Tr();
        if($food_type[0] eq "any") {
            last;
        }
    }
    else {
        print $cgi->start_Tr(), 
            td({-align=>'CENTER', -valign=>'TOP'}, [$food_type[$i], "", "", ""]),
            $cgi->end_Tr();
    }
} 
 
print $cgi->end_table(),
    $cgi->end_fieldset();

# print out filtered metadata
print h3('List of Foods Based on Search Keys'),
    #$cgi->start_table({-border=>'', -class=>'fixed'}),
    $cgi->start_table({-border=>'', width=>"100%"}),
    #caption({-align=>'LEFT'}, strong('List of Foods Based on Search Keys')),
    $cgi->start_Tr({-align=>'CENTER', -valign=>'TOP'}),
    th(['ID Number', 'Name', 'Type', 'Canteen Location', 'Main Ingredient']),
    $cgi->end_Tr();

for(my $i=0; $i<$table_rows; $i++) {
    print $cgi->start_Tr({-onClick=>"show_detail($table[$i][0])"}),
        td({-align=>'CENTER', -valign=>'TOP'}, [$table[$i][0], $table[$i][1], $table[$i][2], $table[$i][3], $table[$i][4]]),
        $cgi->end_Tr();
}

print $cgi->end_table(),
    br,
    "Click a row to see the detail information",
    p(), hr; 

# print out detail information of selected foo# print out detail information of selected foodd
my $display_flag = param('detail_info'); #flag variable for displaying detail information of clicked food in the table
if($display_flag eq '') {
    print start_form({-id=>'display'}),
        hidden(-name=>'detail_info', -id=>'detail_info', -value=>undef),
        hidden(-name=>'food_type', -id=>'temp_food_type', -value=>@food_type),
        hidden(-name=>'ingredient', -id=>'temp_ingredient', -value=>$ingredient),
        hidden(-name=>'canteen', -id=>'temp_canteen', -value=>$canteen),
        hidden(-name=>'food_name', -id=>'temp_food_name', -value=>$food_name),
        end_form;
}
elsif($display_flag =~ m/^[\d]*/) {
    print start_form({-id=>'display'}),
        hidden(-name=>'detail_info', -id=>'detail_info', -value=>$display_flag),
        hidden(-name=>'food_type', -id=>'temp_food_type', -value=>@food_type),
        hidden(-name=>'ingredient', -id=>'temp_ingredient', -value=>$ingredient),
        hidden(-name=>'canteen', -id=>'temp_canteen', -value=>$canteen),
        hidden(-name=>'food_name', -id=>'temp_food_name', -value=>$food_name),
        end_form;

    print h3('Detail Information'),
        "$display_flag",
        p(), hr;
}

print a({-href=>'/~kchangaa'}, "Go back to the main page."),
    br;
    $cgi->end_div(),
    $cgi->end_div(),
    end_html;
