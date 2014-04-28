

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
   
//    $("table tr").click(function() {
//    $("table tr").css("background", "#fff"); //reset to original color
//    $(this).css("background", "#fo0"); //apply the new color
//    });

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

function show_detail(id, index)
{
    //alert(document.getElementById('detail_info').value + " / " +id);
    document.getElementById('detail_info').value = id;
    document.getElementById('selected_row').value = index;
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
    var rating_radio = document.getElementsByName('_rating');
    var recommend_radio = document.getElementsByName('_recommend');
    var dishname = document.getElementsByName('food_name')[0].value;
    
    
    if (!comment){
        alert("Please enter a comment");
        return false;
    }
    
    if (!reviewer_name){
        var anon = confirm("Leave review anonymously?");
        if (anon) {
//            reviewer_name = "Anonymous";
            document.getElementById('_reviewer_name').value = "Anonymous";
        }
        else return false;
    }
    
    
    var rating = 0;
    for (var i=0; i < rating_radio.length; i++){
      if (rating_radio[i].checked)
        {
        rating = rating_radio[i].value;
        }
    }
    
    var recommendation = "";
    for (var i=0; i < recommend_radio.length; i++){
      if (recommend_radio[i].checked)
        {
        recommendation = recommend_radio[i].value;
        }
    }
    
    var confirmation_string = "Thanks " + reviewer_name + "!\nYou are about to leave the following review for " + dishname + ":\n\nRating: " + rating + "/5 \nBottom Line: " + recommendation +"\nComments: " + comment + "\n\nAdd review?";
    var add_comment = confirm(confirmation_string);
    
    return add_comment;
}

// function to use for debugging
function do_print(msg)
{
    alert("print: " + msg);
}

function commentSubmit() 
{
    //document.getElementById("_comment").value = "";
    
    //document.forms["add_comment_form"].submit();
    //document.forms["add_comment_form"].reset();

    if(add_comment()) {
        //document.forms["add_comment_form"].submit();
        //document.forms["add_comment_form"].reset();
        
        document.getElementById("add_comment_form").submit();
        //document.getElementById("add_comment_form").reset();

        //document.getElementById("_comment").value = "";
        //document.getElementById("_reviewer_name").value = "";
    }
    else {
        //alert("Comment has not been submitted");
    }
}

function clearForm()
{
    document.getElementById("_comment").value = "";
    document.getElementById("_reviewer_name").value = "";
}

function chg_row_color(index)
{
    // reset row color
    var table = document.getElementById("metadata_table");    
    var rows = table.getElementsByTagName("tr"); 
    //if(index != null) { 
        for(var i = 0; i < rows.length; i++) {
            if(i==(index+1)) {
                rows[i].className = "selected_row";
            }
            else {
                rows[i].className = "plain_row";
            }
        }  
    //}
}
