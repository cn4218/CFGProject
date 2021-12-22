//localStorage.setItem("Test", [1,2,3,4])

//localStorage.setItem("products_list", JSON.stringify([]))

var button_state = [true,true,true,true,true] ; //initially we want to include all ingredients 
    var export_info = {
        "filter": "unordered", //Assumtion if nothing selected
        "data": {}   
    };
    
var products_list_result = null 
localStorage.setItem("bool", false)


function show_active(item_id){
    document.getElementById("Home").className = "nav-link";
    document.getElementById("Results").className = "nav-link";
    document.getElementById("Wishlist").className = "nav-link";
    document.getElementById("Profile").className = "nav-link";
    document.getElementById("Log-out").className = "nav-link";
    


    document.getElementById(item_id).className = "nav-link active";

   
}
    
function toggle_record_state(icon_id, button_id, num){ 
    `When you want to include an ingredient in your search you leave the button next to that ingredinet input as green
    If you don't want to include an ingredient in you search then click on the button and it changes to red 
    
    The computer needs a way of knowing which ingredients you want included/not included in your search and so a list called 
    button_state is constantly updated with a boolean (true or false ) on each toggle between the red and green button 
    where true = include and false = don't include ingredient. 
    `
    var element = document.getElementById(icon_id);
    
    if (element.classList[1] == "fa-times"){  
        document.getElementById(icon_id).className = "fas fa-check";
        document.getElementById(button_id).style.backgroundColor = "rgb(12, 177, 12)";
        button_state[num-1] = true; 
        console.log(button_state);
    }
    else{
        document.getElementById(icon_id).className = "fas fa-times";
        document.getElementById(button_id).style.backgroundColor = "red";  
        button_state[num-1] = false ;
        console.log(button_state);
    }
}


function record_filter(filter_id){
    `The user is given the option to decide the nature of the search they are about 
    to conduct. They can choose either an ordered or unordered search and their choice 
    is recorded in a dictionary that will later be sent to the backend to process`

    document.querySelectorAll(".dropdown-item").forEach(function(element) {
        element.style.backgroundColor= "white";
        
    });
    let element = document.getElementById(filter_id);
    element.style.backgroundColor= "grey"; 
    filter_str = element.innerHTML;
    console.log(filter_str);
    export_info["filter"] = filter_str;
    
}
function format_info(){ 
    `This function is called in the send_info() function which is activated when a 
    user presses the search button. It takes all the contents from all 5 input fields 
    and creates a tuple of the content and the corresponding boolean element from the button_state list.
    A dictionary is then created and returned with the numbers 1 -> 5 as keys and their corresponding 
    values the user entered. 
    `
    var input_ingredient_dict = {}; //becomes a dict with tuples values
    for (let i = 0; i < 5; i++) {
        id_str = "input" + (i + 1);
        let el = document.getElementById(id_str);
        tup = [el.value,button_state[i]]
        idx_str = (i + 1).toString() 
        input_ingredient_dict[idx_str] = tup
        
    }
    return input_ingredient_dict
    

}

function send_info(){
    ``    
    var data_dict = format_info()
    var num_empty_ingredients = 0

    for (key in data_dict) {
        ingredient = (data_dict[key])[0]
        if (ingredient.trim() == ""){
            num_empty_ingredients += 1
        }
    }
    if (num_empty_ingredients == 5){
        console.log("No inputs")
        return 
    }
    export_info["data"] = data_dict
    console.log(export_info)
    
    // make sure export_info["data"] isn't empty before you send 
    
    post_data = {
        method: 'POST',
        
        headers: {'Content-Type': 'application/json',},
        
        body: JSON.stringify(export_info)

    }

    fetch("http://127.0.0.1:5001/Search", post_data) //add exception handling later.should redirect to a new page 
        .then( function(response){ 
            console.log(response);
            response.text().then(function(text){ 
                console.log(text)
                products_list_result_or_string = text ;
             //   console.log(products_list_result);

                // const file_system = require('fs');
                // file_system.writeFile(
                //     "exchange_results.json",
                //     JSON.stringify(products_list_result),
                //     function ()
                //     )
                // sessionStorage.setItem("Products",JSON.stringify(products_list_result));

                //call a function that populates the results html page first, then redirect to it 
                //later on, make sure the navigation bar is still there for when you want to to go back or move to another
                // page 

                //if we are here, it means we successfully received results 
                //this will send a boolean true which results_func.js will retrieve 
                //Once it has used it for its purposes, it will set it back to false 
                localStorage.setItem("bool", true)
                

                
                

            
            });

            
        }) //check if this is correct syntax for url endpoints 
        .catch((error) => {
            console.log("There is probably a network. Check that app.py is running on the backend please")
            console.log(error)
          });

}

