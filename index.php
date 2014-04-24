<?php
    $flag = $_GET["flag"];
?>

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">  
    <title>Open Canteen:main</title>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script language="JavaScript" src="open_canteen.js"></script>
    <link rel="stylesheet" type="text/css" href="open_canteen.css"/>
</head>

<?php echo ($flag != NULL) ? '<body onload="check_redirect($flag)">' : '<body>'?>
    <div id="container">
        <div id="content">
            <div id="header">
                <h1>Open Canteen!</h1>
            </div> 
            <form id="search_keys" action="cgi-bin/result.cgi" method="GET" onsubmit="return validateForm()">
                <fieldset class="fieldset_front">
                    <legend><strong>Food Type</strong></legend>     
                    <div class="input_form"><input type="checkbox" name="food_type" id="any" value="any" checked="checked"/>Any</div>
                    <div class="input_form"><input type="checkbox" name="food_type" id="soup_noodle" value="soup_noodle"/>Soup Noodle</div>
                    <div class="input_form"><input type="checkbox" name="food_type" id="fried_noodle" value="fried_noodle"/>Fried Noodle</div>
                    <div class="input_form"><input type="checkbox" name="food_type" id="rice" value="rice"/>Rice</div>
                    <div class="input_form"><input type="checkbox" name="food_type" id="fried_rice" value="fried_rice"/>Fried Rice</div>
                    <div class="input_form"><input type="checkbox" name="food_type" id="congee" value="congee"/>Congee</div>
                    <div class="input_form"><input type="checkbox" name="food_type" id="curry" value="curry"/>Curry</div>
                    <div class="input_form"><input type="checkbox" name="food_type" id="dish" value="dish"/>Dish</div>
                    <div class="input_form"><input type="checkbox" name="food_type" id="steak" value="steak"/>Steak</div>
                </fieldset>
                <fieldset class="fieldset_front">
                    <legend><strong>Main Ingredient</strong></legend>
                    <div class="input_form"><input type="radio" name="ingredient" id="any" value="any" checked="checked"/>Any</div>
                    <div class="input_form"><input type="radio" name="ingredient" id="beef" value="beef"/>Beef</div>
                    <div class="input_form"><input type="radio" name="ingredient" id="pork" value="pork"/>Pork</div>
                    <div class="input_form"><input type="radio" name="ingredient" id="chicken" value="chicken"/>Chicken</div>
                    <div class="input_form"><input type="radio" name="ingredient" id="duck" value="duck"/>Duck</div>
                    <div class="input_form"><input type="radio" name="ingredient" id="fish" value="fish"/>Fish</div>
                    <div class="input_form"><input type="radio" name="ingredient" id="vegetable" value="vegetable"/>Vegatable</div>
                    <div class="input_form"><input type="radio" name="ingredient" id="else" value="else"/>Else</div>
                </fieldset>
                <div>
                    <fieldset class="fieldset_front" style="display:inline;width:300px">
                        <legend><strong>Which Canteen?</strong></legend>
                        <div class="input_form"><input type="radio" name="canteen" id="any" value="any" checked="checked"/>Any</div>
                        <div class="input_form"><input type="radio" name="canteen" id="canteen1" value="canteen1"/>Canteen1</div>
                        <div class="input_form"><input type="radio" name="canteen" id="canteen2" value="canteen2"/>Canteen2</div>
                    </fieldset>
                    <fieldset class="fieldset_front" style="display:inline">
                        <legend><strong>Food Name</strong> (optional)</legend>
                        <div class="input_form">
                            <input type="text" name="food_name" id="food_name" value=""/>
                        </div>
                    </fieldset>
                </div>
                <br/>
                <div class="button"/>
                    <input class="button" type="submit" value="submit"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <input class="button" type="reset" value="reset"/>
                </div>
            </form>
            <hr/>
            <h2 style="margin-bottom: 0px;"><a id="upload-link" href="#upload">upload food</a></h2>
            <h3 id="upload_description" style="color:darkblue;text-align:center;font-size:18px">click "upload food" to add a new food!</h3>
            <div id="upload" class="hidden">
              <form id="upload" action="cgi-bin/upload.cgi" method="POST" onsubmit="return validateUpload()" enctype="multipart/form-data">
                    <fieldset class="fieldset_front">
                        <div class="input_fieldset">
                            <fieldset class="input_fieldset"><legend>Food Type</legend>
                            <select name="food_type_" id="food_type_">
                                <option value="soup_noodle">Soup Noodle</option>
                                <option value="fried_noodle">Fried Noodle</option>
                                <option value="rice">Rice</option>
                                <option value="fried_rice">Fried Rice</option>
                                <option value="congee">Congee</option>
                                <option value="curry">Curry</option>
                                <option value="dish">Dish</option>
                                <option value="Steak">Steak</option>
                                <option value="else">Else</option>
                            </select></fieldset>
                            <fieldset class="input_fieldset"><legend>Main Ingredient</legend>
                            <select name="ingredient_" id="ingredient_">
                                <option value="beef">Beef</option>
                                <option value="pork">Pork</option>
                                <option value="chicken">Chicken</option>
                                <option value="duck">Duck</option>
                                <option value="fish">Fish</option>
                                <option value="vegatable">Vegatable</option>
                                <option value="else">Else</option>
                            </select></fieldset> 
                            <fieldset class="input_fieldset"><legend>Canteen</legend>
                                <div class="input_form"><input type="radio" name="canteen_" id="canteen1_" value="canteen1" checked="checked"/>Canteen1</div>
                                <div class="input_form"><input type="radio" name="canteen_" id="canteen2_" value="canteen2"/>Canteen2</div>
                            </fieldset>
                        </div>
                        <br/>
                        <div>
                            <fieldset class="input_fieldset">
                                <legend>Food Name</legend>
                                <div class="input_form">
                                    <input type="text" name="food_name_" id="food_name_" value=""/>
                                </div>
                            </fieldset>
                            <fieldset class="input_fieldset">
                                <legend>Ingredients (optional)</legend>
                                <div class="input_form">
                                    <input type="text" name="ingredients_" id="ingredients_" value=""/>
                                </div>
                            </fieldset>
                            <fieldset class="input_fieldset">
                                <legend>Picture (optional)</legend>
                                <div class="input_form">
                                    <input type="file" name="photo"/>
                                </div>
                            </fieldset>
                        </div>
                        <br/>
                        <div class="button"/>
                            <input class="button" type="submit" value="upload"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            <input class="button" type="reset" value="reset"/>
                        </div>
                    </fieldset>
                </form>
            </div>
        </div>
    </div>
<body>

</html>
