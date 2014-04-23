

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

function add_comment(){
    // validate form first
    var reviewer_name = document.getElementsByName("_name")[0].value;
    var comment = document.getElementsByName("_comment")[0].value;
    
    // check that something other than whitespace is entered for name and comment
    var name_entered = reviewer_name.match(/\S/);
    var comment_entered = comment.match(/\S/);
    
    if (!name_entered){
        var leave_empty = confirm("No name entered. Leave review anonymously?");
        if (!leave_empty){
            return;
        }
    }
    if (!comment_entered){
        var leave_empty = confirm("Leave rating without a review?");
        if (!leave_empty){
            return;
        }
    }
     
    // add new comment
    var add_comment = confirm("Add rating?");
    if (add_comment){
        document.getElementById("add_comment_form");
    }
    return add_comment;
}

// function to use for debugging
function do_print(msg)
{
    alert(msg);
}

