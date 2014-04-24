#!/usr/bin/perl -w

use strict;
use warnings;
use constant { true => 1, false => 0 };
use CGI qw(:all);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser); #redirect error messages to browser
use Switch;
use File::Basename;

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

# UPLOAD / UPDATE PICTURE
my $pic_addr = param('pic_upload');

# picture related..
if ($pic_addr ne "") {
    my ($file_name, $file_path, $file_extension) = fileparse ($pic_addr, '\..*');
    my $upload_dir = "../db/images";
    my $upload_filehandle = $cgi->upload('pic_upload'); # actually holding the picture

    my $UPLOADFILE; # variable to create an actual picture file

    # save pic_addr based on id number of a food
    my $pic_name;
    my $pic_num = param('detail_info');
    $pic_name = $pic_num.$file_extension;

    # create the picture file into the target directory
    chmod 0777, $upload_dir or ($err_flag = true); # change permission of image folder to upload the file

    `rm ../db/images/$pic_num.*`; # delete existing file

    open ($UPLOADFILE, ">$upload_dir/$pic_name") or ($err_flag = true);
    binmode $UPLOADFILE;

    while (<$upload_filehandle>) {
      print $UPLOADFILE $_;
    }
    close $UPLOADFILE;
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
        -onLoad=>"do_alert($err_flag);" 
    );

print "<script language=\"JavaScript\" src=\"../open_canteen.js\"></script>";

print $cgi->Link({-rel=>'stylesheet', -type=>'text/css', -href=>'../open_canteen.css'}),
    
    $cgi->start_div({-id=>'container'}),
    $cgi->start_div({-id=>'content'}),
    $cgi->start_div({-id=>'header'}),
    a({-href=>'../'}, "<h1>Open Canteen!</h1>"),
    $cgi->end_div();
 
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

my $this_page = self_url;

# print out detail information of selected food
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

    print $cgi->start_div({-id => 'detail', name => $display_flag}, h3('Detail Information'));
        my $dishname = "$table[$display_flag][1]";
        my $file = "../db/foods/$display_flag.txt";
        
        my @comments = ();
        # my @keywords = ();
        my @ingredients = ();
        
        my $img_url = "../db/images/no_pic.jpg"; # default
        # get picture from image folder: any typle of picture
        my $dir = '../db/images';
        opendir(DIR, $dir) or die $!;
        while (my $file = readdir(DIR)) {
            # We only want files
            next unless (-f "$dir/$file");
            
            # We only want files
            # Use a regular expression to find files ending in any suffix 
            next unless ($file =~ m/^$display_flag\./);
            
            # We only want files
            $img_url = $file;
            $img_url = $dir . "/" . $img_url;
            last; 
        }
        closedir DIR;
        
        # my $keywords ="";
        my $ingredients = "";
        my $avg_rating = 0;
        
        my @raw_main_info = ();
            
        if (-e $file){ # if the file exists
            
            
            my $line_num = 0;                    
            
            # text file format information
            my $dishname_line = 1;
            my $ingredients_line = 2;


            my $temp_type = "";
            my $temp_canteen = "";
            my $temp_main_ingredient = "";
            
            open(READFILE, '<', $file) || die;
                while(my $line = <READFILE>){
                    $line_num++;
                    chomp $line;
                    switch($line_num){
                        case ($dishname_line){
                            @raw_main_info = split('\s?\|\s?', "$line"); # deal with this stuff later
                            $temp_type = $raw_main_info[1];
                            $temp_canteen = $raw_main_info[2];
                            $temp_main_ingredient = $raw_main_info[3];
                        }
                        case ($ingredients_line){
                            $ingredients = "$line";
                            @ingredients = split(',', $line);
                            
                        }
                        else{ # past all the food details
                            push @comments, "$line";
                            my @raw_comment = split('\s?\|\s?', "$line");
                            my $rating = $raw_comment[1];
                            $avg_rating += $rating;
                        }
                    }
                }
            close(READFILE);
            
                
                
            my $num_comments = @comments;
            
            print $cgi->start_div({-id => 'basic_information'});
            print "<p class=\"food_name\"> $dishname </p>";
            if (-e $img_url){
                print "<img src=\"$img_url\" class=\"dish_img\"/>";
            }

            print $cgi->start_fieldset({-class=>'input_fieldset'}); 
            if ($num_comments > 0){
                $avg_rating /= $num_comments;
                my $avg = sprintf("%.2f", $avg_rating);
                print p({-class=>'basic_info_element' -id=>'avg_rating'}, 'User rating: ', $avg, '/ 5  from  ', $num_comments,' reviews.');
            }
            else{
                print p({-class=>'basic_info_element' -id=>'avg_rating'}, 'User rating: No ratings available! Be the first to leave your review below');

            }
            print "<p class=\"basic_info_element\"> Dish type: $temp_type </p>";
            print "<p class=\"basic_info_element\"> Location: $temp_canteen </p>";
            print "<p class=\"basic_info_element\"> Main ingredient: $temp_main_ingredient </p>";
            print $cgi->end_fieldset();
            print "<form id=\"upload\" method=\"POST\" onsubmit=\"return validatePicUpload()\" enctype=\"multipart/form-data\">";
            print hidden(-name =>'_id', -value => $display_flag),
                hidden(-name =>'_file', -value => $file),
                hidden(-name =>'_dishname', -value => $dishname),
                hidden(-name =>'_results_url', -value => $this_page),
                hidden(-name=>'detail_info', -id=>'detail_info', -value=>$display_flag),
                hidden(-name=>'food_type', -id=>'temp_food_type', -value=>@food_type),
                hidden(-name=>'ingredient', -id=>'temp_ingredient', -value=>$ingredient),
                hidden(-name=>'canteen', -id=>'temp_canteen', -value=>$canteen),
                hidden(-name=>'food_name', -id=>'temp_food_name', -value=>$food_name);
            print "<fieldset class=\"input_fieldset\"><legend style=\"font-size:15px\">Upload/Update Picture</legend>";
            print "<input id=\"pic_upload\" type=\"file\" name=\"pic_upload\"/>";
            print "<input id=\"pic_submit\" type=\"submit\" value=\"submit\"/>";
            print "</fieldset>";
            print "</form>";
            print $cgi->end_div(), hr;
                
       
            print $cgi->start_div({-id=>'add_comment'});
                print h4('Add a comment');
            
                print $cgi->start_form(-id => 'add_comment_form', -name => 'add_comment_form', -onSubmit => "return add_comment()"),
                
                    # the information to reload the detailed page
                    hidden(-name=>'detail_info', -id=>'detail_info', -value=>$display_flag),
                    hidden(-name=>'food_type', -id=>'temp_food_type', -value=>@food_type),
                    hidden(-name=>'ingredient', -id=>'temp_ingredient', -value=>$ingredient),
                    hidden(-name=>'canteen', -id=>'temp_canteen', -value=>$canteen),
                    hidden(-name=>'food_name', -id=>'temp_food_name', -value=>$food_name),
                    
                    p,
                        "Please rate this dish: ",
                    p,
                        $cgi->radio_group(-id => '_rating', -name => '_rating', -values => ['1', '2', '3', '4', '5']),
                    p,
                        "Would you recommend? ",
                    p,
                        $cgi->radio_group(-id => '_recommend', -name => '_recommend', -values => ['Must try', 'Just ok', 'Skip it'], -default => 'Just ok'),
                    p,

                        "Comments: ",
                    p,
                        $cgi->textarea(-id => '_comment', -name => '_comment', -value => 'yum!', -cols => 40, -rows => 4, -onClick => "this.value=\"\""),
                    p,
                        "Your name: ", 
                        $cgi->textfield(-id => '_reviewer_name', -name => '_reviewer_name', -value => '', -onClick => "this.value=\"\""),
                    p,
                        $cgi->submit(-id => '_submit', -name=> '_submit', -value => 'Post Comment');
                        
                        
                    # recalculate average rating if the user submits a new review
                    $avg_rating = (($avg_rating * $num_comments) + param('_rating'))/ ($num_comments+1);
                    
                    print $cgi->hidden(-name=>'_avg_rating', -id=>'_avg_rating', -value=>$avg_rating);
                
                    print $cgi->end_form,
                hr;
            print $cgi->end_div();
            
            # now display all the comments to the screen
            
            print $cgi->start_div({-id=>'comments'}),
                h5('Comments and Reviews'),
                "<ol id=\"comments_list\">";
                
                for (my $i = 0; $i < $num_comments; $i++){
                    #extract the data from the flat file
                    my @raw_comment = split('\s?\|\s?', $comments[$i]);
                    my $comment = $raw_comment[0];
                    my $rating = $raw_comment[1];
                    my $reviewer = $raw_comment[2];
                    my $recommend = $raw_comment[3] || 0; # our data files don't all have this field due to format change
                    
                    if ($recommend){
                        print li( {-class=>'review'}, 
                            p({-class=>'rating'}, 'Rating: ', $rating, '/5'),
                            p({-class=>'recommended'}, 'Bottom Line ', $recommend),
                            p({-class=>'comment'}, $comment),
                            p({-class=>'reviewer_name'}, '- Review by ', $reviewer),
                            hr
                        );
                    }
                    else{
                        print li( {-class=>'review'}, 
                            p({-class=>'rating'}, 'Rating: ', $rating, '/5'),
                            p({-class=>'comment'}, $comment),
                            p({-class=>'reviewer_name'}, '- Review by ', $reviewer),
                            hr
                        );
                    }
                } # end for loop for comments
            
                # add new comment to file on submit
                if ($cgi->param('_submit')){
                    
                    my $reviewer = $cgi->param('_reviewer_name') || "Anonymous";
                    my $recommended = $cgi->param('_recommend');
                    my $rating = $cgi->param('_rating');
                    my $comment = $cgi->param('_comment');

                    # add newest comment to list
                    my $new_comment_line = "$comment | $rating | $reviewer | $recommended";
                    push @comments, $new_comment_line;

                    # re-create data file, with new comment and updated average rating
                    open(OUTFILE, '>', $file) || die;
                        print OUTFILE "$dishname | $temp_type | $temp_canteen | $temp_main_ingredient \n";
                        print OUTFILE "$ingredients\n";
                        for (my $j = 0; $j < $num_comments + 1; $j++){
                            print OUTFILE "$comments[$j]\n";
                            # print "$comments[$j]";
                        }
                    close(OUTFILE);
                    
                    # print newest comment to display on browser
                     print li({-class=>'review'}, 
                            p({-class=>'rating'}, 'Rating: ', $rating, '/5'),
                            p({-class=>'recommended'}, 'Bottom Line ', $recommended),
                            p({-class=>'comment'}, $comment),
                            p({-class=>'reviewer_name'}, '- Review by ', $reviewer),
                            hr
                        );
                    
                
                }
                
                print "</ol>";
            $cgi->end_div(); #end "comments" div
            
        }
        else { # if error opening file
            print "<p> Could not open $file </p>";
            print "<p> $dishname is not in our database! <a href=\"../index.html#upload\"> Create new dish? </a> </p>";
        }
        
    $cgi->end_div(); #end detail div
        
}

print a({-href=>'../'}, "Go back to the main page."),
    br;
    $cgi->end_div(),
    $cgi->end_div(),
    end_html;
