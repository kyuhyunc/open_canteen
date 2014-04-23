#!/usr/bin/perl -w

use strict;
use warnings;
use constant { true => 1, false => 0 };
use CGI qw(:all);
use CGI::Carp qw(fatalsToBrowser); #redirect error messages to browser
use Switch;

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
    h4('Click a row to see the detail information'),
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

    print h3('Detail Information');
        my $dishname = "$table[$display_flag][1]";
        my $file = "../db/foods/$display_flag.txt";
        
        my @comments = ();
        my @keywords = ();
        my @ingredients = ();
        
        
        my $dishtype = "";
        my $canteen = "";
        my $mainingredient = "";
        my $img_url = "";
        my $keywords ="";
        my $ingredients = "";
        my $avg_rating = 0;
            
        if (-e $file){ # if the file exists
            
            
            my $line_num = 0;                    
            
            # info about the text file
            my $dishname_line = 1;
            my $img_url_line = 4;
            my $ingredients_line = 3;
            my $keywords_line = 2;
            my $ratings_line = 5;


            open(READFILE, '<', $file);
                
                while(my $line = <READFILE>){
                    $line_num++;
                    chomp $line;
                    switch($line_num){
                        case ($dishname_line){
                            my @raw_main_info = split('\s?\|\s?', $line);
                            
                            $dishname = $raw_main_info[0];
                            $dishtype = $raw_main_info[1];
                            $canteen = $raw_main_info[2];
                            $mainingredient = $raw_main_info[3];
                        }
                        case ($img_url_line){
                            $img_url = $line;
                        }
                        case ($ingredients_line){
                            $ingredients = $line;
                            @ingredients = split(',', $line);
                            
                        }
                        case ($keywords_line){
                            $keywords = $line;
                            @keywords = split(',', $line);
                        }
                        case ($ratings_line){
                            $avg_rating = $line;
                        }
                        else{ # past all the food details
                            push @comments, $line;
                        }
                    }
                }
            close(READFILE);
            
            my $num_comments = @comments;
            
            print "<p> $dishname </p>";
            print "<p> User rating: $avg_rating / 5  from  $num_comments reviews. </p>";
            print "<p> Dish type: $dishtype </p>";
            print "<p> Location: $canteen </p>";
            print "<p> Main ingredient: $mainingredient </p>";
            
            # now display all the comments to the screen
            print "<div> <h5> Comments: </h5>";
            print "<ol id=\"list_of_comments\">";
            for (my $i = 0; $i < $num_comments; $i++){
                #extract the data from the flat file
                my @raw_comment = split('\s?\|\s?', $comments[$i]);
                my $comment = $raw_comment[0];
                my $rating = $raw_comment[1];
                my $recommend = $raw_comment[2];
                my $reviewer = $raw_comment[2];
                
                print "<li class=\"review\">";
                    print "<p class=\"rating\"> Rating: $rating / 5 </p>";
                    #print "<p class=\"recommended\"> Bottom line: $recommend </p>";
                    print "<p class=\"comment\"> $comment </p>";
                    print "<p class=\"reviewer_name\"> - Review by $reviewer </p>";
                    print "<hr/>";
                print "</li>";
            }
            print "</ol> </div>";
            
            
            print hr;
        
            print h4('Add a comment'),
            start_form(-name => 'add_comment_form'),
                    "Your name: ", textfield(-name => '_name', -value => 'anon'),
                p,
                    "Please rate this dish: ",
                p,
                    radio_group(-name => '_rating', -values => ['1', '2', '3', '4', '5'], -default => '3'),
                p,
                    "Would you recommend? ",
                p,
                    radio_group(-name => '_recommend', -values => ['Must try', 'Just ok', 'Skip it'], -default => 'Just ok'),
                p,

                    "Comments: ",
                p,
                    textarea(-name => '_comment', -value => 'yum!', -cols => 40, -rows => 4),
                p,
                submit(-name=> '_submit', -value => 'Post Comment', -onClick => "alert('yay');"),
            end_form,
            hr;
            
            if (param('_submit')){
                my $reviewer = param('_name');
                my $recommended = param('_recommend');
                my $rating = param('_rating');
                my $comment = param('_comment');

                # add newest comment to list
                my $new_comment_line = "$comment | $rating | $recommended | $reviewer";
                push @comments, $new_comment_line;

                my $num_comments = @comments;
                $avg_rating = $avg_rating; # re-calculate average rating

                # re-create data file, with new comment and updated average rating
                open(OUTFILE, '>', $file);
                    print OUTFILE "$dishname\n";
                    print OUTFILE "$img_url\n";
                    print OUTFILE "$ingredients\n";
                    print OUTFILE "$keywords\n";
                    print OUTFILE "$avg_rating\n";
                    for (my $j = 0; $j < $num_comments; $j++){
                        print OUTFILE "$comments[$j]\n";
                    }
                    print "success";
                close(OUTFILE);

                }       
            
        
        }
        else { # if error opening file
            print "<p> Could not open $file </p>";
            print "<p> $dishname is not in our database! <a href=\"../index.html#upload\"> Create new dish? </a> </p>";
        }
}

print a({-href=>'../'}, "Go back to the main page."),
    br;
    $cgi->end_div(),
    $cgi->end_div(),
    end_html;
