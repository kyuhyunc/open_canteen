

$(document).ready( function() {
    // Expand upload form
    $('#upload-link').click( function() {
        $('#upload').toggle('slow');
        $('#upload_description').toggle('slow');
        return false;
    });

    // Expand detail information area
    $('#display-link').click( function() {
        $('#display').toggle('slow');
        return false;
    });
    
});

// Check if inputs have been selected/entered properly
function validateForm()
{
    var food_type = document.getElementsByName("food_type");
    var ingredient = document.getElementsByName("ingredient");
    var canteen = document.getElementsByName("canteen");
    var err_flag1 = true;
    var err_flag2 = true;
    var err_flag3 = true;
    
    for (var i=0; i<food_type.length; i++) {
        if(food_type[i].checked == true) err_flag1 = false;
    }

    for (var i=0; i<ingredient.length; i++) {
        if(ingredient[i].checked == true) err_flag2 = false;
    }

    for (var i=0; i<canteen.length; i++) {
        if(canteen[i].checked == true) err_flag3 = false;
    }

    if (err_flag1 || err_flag2 || err_flag3) {
        alert("Food type, Main Ingredient and Canteen must be selected");
        return false;
    }
}

function validateUpload()
{
    var food_name = document.getElementsByName("food_name_");
    if (food_name[0].value == "") {
        alert("Food name is missing");
        return false;
    }    
}

// check if metadata text file has been loaded succesfully
function do_alert(err_flag)
{
    if (err_flag == 1) {
        alert("Error has occured. Going back to the front page");
        window.history.back();
    }
}

function show_detail(id)
{
    //alert(document.getElementById('detail_info').value + " / " +id);
    document.getElementById('detail_info').value = id;
    document.forms["display"].submit();   
 
    return true;
}

function check_redirect(flag) {
    if(flag==true) {
        document.getElementById('upload').setAttribute("display", "block");
        document.getElementById('upload_description').setAttribute("display", "none");
    }
    else {
        document.getElementById('upload').setAttribute("display", "hidden");
        document.getElementById('upload_description').setAttribute("display", "block");
    }
}

function add_comment(){
    alert("hi");
    // validate form first
    var form = document.getElementById('add_comment_form');
    var reviewer_name = document.getElementsByName("_reviewer_name")[0].value;
    var comment = document.getElementsByName("_comment")[0].value;
    var rating = document.getElementsByName("_rating")[0].value;
    var recommend = document.getElementsByName("_recommend")[0].value;
    var dishname = document.getElementsByName("_dishname")[0].value;
    var avg_rating = document.getElementsByName("_avg_rating")[0].value;
    var num_comments = document.getElementsByName("_num_comments")[0].value;
    
    alert(comment);
    // check that something other than whitespace is entered for name and comment
    var name_entered = reviewer_name.match(/\S/);
    var comment_entered = comment.match(/\S/);
    
    if (!name_entered){
        reviewer_name = "Anonymous";
    }
    if (!comment_entered){
        var leave_empty = confirm("Leave rating without a review?");
        if (!leave_empty){
            return;
        }
    }
     
    var confirmation_string = "Thanks " + reviewer_name + "!\nYou are about to leave the following review for " + dishname + ":\n\nRating: " + rating + "/5 \nBottom Line: " + recommend +"\nComments: " + comment + "\n\nAdd review?";
    var add_comment = confirm(confirmation_string);
    if (add_comment){
        // avg_rating = ((avg_rating * num_comments) + rating)/ (num_comments+1);
        // document.getElementById("avg_rating").innerHTML = "User rating: "+ avg_rating + "/ 5  from "+ num_comments + " reviews.";
        // var id = document.getElementsByName("_id")[0].value;
        // var url = document.getElementsByName("_results_url")[0].value;
        //show_detail(id);
        //window.location.replace(url);
        
        // var comments_list = document.getElementById('comments_list');
        // var new_comment_node = document.createElement('li');
        // new_comment_node.setAttribute("class", "review");
        
        // var content = "<p class=\"rating\"> Rating: " + rating  + "/ 5 </p>";
        // content = content.concat("<p class=\"recommended\"> Bottom line: " + recommend + "</p>");
        // content = content.concat("<p class=\"comment\"> " + comment + " </p>");
        // content = content.concat("<p class=\"reviewer_name\"> - Review by " + reviewer_name + " </p>");
        // content = content.concat("<hr/>");
        // content = content.concat("</li>");
        
        // new_comment_node.innerHTML = content;
        // comments_list.appendChild(new_comment_node);
    }

    return add_comment;
}

// function to use for debugging
function do_print(msg)
{
    alert(msg);
}

