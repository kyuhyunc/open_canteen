// The load function for the SVG document
function load(evt) {
    // Set the root node to the global variable
    svgdoc = evt.target.ownerDocument;
}

// Check if inputs have been selected/entered properly
function validateForm()
{
    var food_type = svgdoc.getElementsByName("food_type");
    var ingredient = svgdoc.getElementsByName("ingredient");
    var canteen = svgdoc.getElementsByName("canteen");
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

// check if metadata text file has been loaded succesfully
function do_alert(err_flag)
{
    if (err_flag == 1) {
        alert("Error has occured. Going back to the front page");
        window.history.back();
    }
}

// function to use for debugging
function do_print(msg)
{
    alert(msg);
}