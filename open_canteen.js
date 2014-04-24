

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

function validatePicUpload()
{
    var pic_addr = document.getElementById("pic_upload");
    if (pic_addr.value == "") {
        alert("No picture uploaded");
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
    
    var form = document.getElementById('add_comment_form');
    var reviewer_name = document.getElementById('_reviewer_name').value;
    var comment = document.getElementById('_comment').value;
    var rating = document.getElementById('_rating').value;
    var recommend = document.getElementById('_recommend').value;
    var dishname = document.getElementById('_dishname').value;
    
    // check that something other than whitespace is entered for name and comment
    if (!reviewer_name.match(/\S/)){ // if no name entered
        reviewer_name = "Anonymous";
    }
    if (!comment.match(/\S/)){ // if no comment left
        var leave_empty = confirm("Leave rating without a review?");
        if (!leave_empty){
            return;
        }
    }
     
    var confirmation_string = "Thanks " + reviewer_name + "!\nYou are about to leave the following review for " + dishname + ":\n\nRating: " + rating + "/5 \nBottom Line: " + recommend +"\nComments: " + comment + "\n\nAdd review?";
    var add_comment = confirm(confirmation_string);
    return add_comment;
}

// function to use for debugging
function do_print(msg)
{
    alert("print: " + msg);
}

