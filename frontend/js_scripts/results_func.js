
// setTimeout(function(){ 
//     var output = localStorage.getItem("products_list");
//     console.log(JSON.parse(output)); //works perfectly. Just need to find a better solution that setTimeOUT
    
// }, 30000);

//An alternative would be to search for a string at regular intervals 
// var input_bool = false; //initially 

// console.log(localStorage.getItem("bool"))
// setTimeout(function(){ 
//     var input_bool = localStorage.getItem("bool");
//     console.log(input_bool) //type string
   
  
// }, 30000);








function show_active(item_id){
    document.getElementById("Home").className = "nav-link";
    document.getElementById("Results").className = "nav-link";
    document.getElementById("Wishlist").className = "nav-link";
    document.getElementById("Profile").className = "nav-link";
    document.getElementById("Log-out").className = "nav-link";
    


    document.getElementById(item_id).className = "nav-link active";

   
}



function format_div(result,num){
    //make sure the keys match up and are correct 
    //Also if we don't use all the attributes in the end, make sure to only send relevant ones
    product_name = result["product_name"];
    product_id = result["productID"];
    brand = result["brands"];
    quantity = result["quantity"];
    ingredient_list = result["ingredients_list"];
   
    



   div_string = `
    <div class="float-container">
        <div class="float-child first-box">
            <div class="product-item">
            
            <br>
            <h4 style="color:rgb(245,49,99,0.7)"> ${product_name}</h4>
            <span style="color:rgb(245,49,99,0.6)"><b>ProductID:</b></span>
            <span>${product_id}</span> 
            <br> 
            <span style="color:rgb(245,49,99,0.6)"><b> Brand:</b></span>
            <span>${brand}</span>
            <br>
            <span style="color:rgb(245,49,99,0.6)"><b> Quantity:</b></span>
            <span> ${quantity}</span>
            <br>
            <span style="color:rgb(245,49,99,0.6)"><b> Ingredient List:</b></span>
            <br>
            <span>${ingredient_list}
            </span>
          </div>
        </div>
 
    </div>
    
    `
   // console.log(div_string);
    return div_string 


}

// result = {
//         "ProductID": '2', //make sure this part is hidden when I receive it 
//         "ProductName": 'Soin + - peau à boutons',
//         "Quantity": '150 ml',
//         "Brand": 'La vie est à Nous',
//         "Ingredients": "aqua, illite, propylene glycol. kaolin, montmorillonite, titanium dioxide, parfum. sodium polyacrylate, calcite, sodium acrylate / sodium acryloyldimethyl taurate copolymer, polysorbate 80, phenoxyethanol, isohexadecane, disodium cocoamphodiacetate, magnesium aluminum silicate, xanthan gum, disodium edta, citric acid, caprylyl glycol, alcohol denat,  polysorbate 20, melaleuca alternifolia leaf extract"

//     }




// functon that loops through the list of results and uses the format to create the string 
// you will insert into the html 
// have to check and make sure the string isn't empty on the backend, if it is, it 
// has to send an error message somehow 

function add_results(results_list){
    len = results_list.length;
    results_string = "";
    for (let i = 0; i < len; i++) {
        product_dict = results_list[i];
        results_string += format_div(product_dict,i+1);

    }
  //  console.log(results_string)
    document.getElementById("results").innerHTML = results_string;

}


//function that fetches the results_list from the api and also handles exceptions 

 

// function toggle_wishlist_button(button_id,sign){ //make this reproducable by passing id's for the i element and for the specific button
//     var element = document.getElementById(button_id);
//     var symbol = element.innerHTML 
    
//     if (symbol == "+"){ // This means they want to add something to the wishlist 
//         element.innerHTML = "-";
//         document.getElementById(button_id).style.color = "black";
//         document.getElementById(button_id).className = "btn btn-outline-dark";
//         document.getElementById(sign).innerHTML = "Added!";
//         document.getElementById(sign).style.color = "green";
//          2 seconds 
//         setTimeout(function() {
//             document.getElementById(sign).innerHTML = "";
//         },1000)
        
        
//        add to array 
        
        
//     }
//     else{
//         element.innerHTML = "+";
//         document.getElementById(button_id).style.color = "white";
//         document.getElementById(button_id).className = "btn btn-dark";
//         document.getElementById(sign).innerHTML = "Removed!";
//         document.getElementById(sign).style.color = "red";

//         setTimeout(function() {
//             document.getElementById(sign).innerHTML = "";
//         },1000)
        
//        remove from array 
//     }
// }



// localStorage.setItem("user_id",10234) //just for now //make sure to remove later.Using it in the fetch() for now 
var export_dict = {}
function wishlist_button(wish_id,sign){
    var element = document.getElementById(wish_id);
    console.log(element)
    var wish_product_id = element.value; //I had an error here because I put .innerHTML instead of .value 
    console.log(wish_product_id)
    console.log(typeof(wish_product_id))
    // error handling on the backend to make sure its actually an int that was sent 
    // if not,return a message as a response "Error", else return "Added"
    // remember to add error handling for the fetch() api function itself 


    
   // fetch(`http://127.0.0.1:5001/wishlist/add/?user_id=${user_id}&product_id=${wish_product_id }`) //error handling should go on the next line
    // export_dict = {"user_id": user_id.toString() , "product_id": wish_product_id.toString()}
    // console.log(export_dict)

    // post_data = {
    //     method: 'POST',
        
    //     headers: {'Content-Type': 'application/json',},
        
    //     body: JSON.stringify(export_dict)

    // }
    var user_id = 10234;
    var product_id = wish_product_id.toString()
    fetch(`http://127.0.0.1:5001/wishlist/add/${user_id}/${product_id}`) //error handling should go on the next line
    .then( function(response){  //the above endpoint works 
        console.log(response);
        response.text().then(function(text){ 
            
            text = JSON.parse(text)
            
            if (text == "Error"){
                console.log(text)
                document.getElementById(sign).innerHTML = "Nothing added, please try again!";
                document.getElementById(sign).style.color = "red";
            } else if (text == "Added"){
                console.log(text)
                document.getElementById(sign).innerHTML = "Added!";
                document.getElementById(sign).style.color = "green";

            }
            setTimeout(function() {
                document.getElementById(sign).innerHTML = "";
            },1000)
        }); 
    }) 
    .catch((error) => {
        console.log("There is probably a network. Check that app.py is running on the backend please")
        console.log(error)
      });

}













function test_func(){
    console.log("hello");
}

//Running functions once the page opens 
//setInterval(function(){ 
//Find a more efficient way later because this would be very expensive for the AWS database 
//Make regular calls to the api to get the search results 


//Other options:
//You could write the array to a json file and the result page will pick it up 

//},10000);


//What you have is a part of this script that is constantly checking to see if the stored string == true 
// because then that means that a new set of search results have been returned to the 
// "http://127.0.0.1:5001/Search" endpoint. Then a request is sent to that endpoint to fetch 
// the new data and use it to populate the results.html page . 
// The function add_results is what makes the formating and the population of the results.html page possible 
var parsed_list = [] 
setInterval(function(){  
    if (localStorage.getItem("bool") == "true"){
        localStorage.setItem("bool",false)
        fetch("http://127.0.0.1:5001/Search")
        .then( function(response){ 
            console.log(response);
            response.text().then(function(text){ 
                //   console.log(text)
                products_list_result = text ; // remember this produces a list of a list in json format. so you need to parse it and only take the first element 
                parsed_list = JSON.parse(products_list_result)[0]
             //   console.log(parsed_list); // slows my code down 
                add_results(parsed_list);
                
               // add_results(products_list_result); there is a problem with this function 
            });
        });

        
    }
},800)



 







// results_list = [
//     {
//         "ProductID": '2', //make sure this part is hidden when I receive it 
//         "ProductName": 'Soin + - peau à boutons',
//         "Quantity": '150 ml',
//         "Brand": 'La vie est à Nous',
//         "Ingredients": "aqua, illite, propylene glycol. kaolin, montmorillonite, titanium dioxide, parfum. sodium polyacrylate, calcite, sodium acrylate / sodium acryloyldimethyl taurate copolymer, polysorbate 80, phenoxyethanol, isohexadecane, disodium cocoamphodiacetate, magnesium aluminum silicate, xanthan gum, disodium edta, citric acid, caprylyl glycol, alcohol denat,  polysorbate 20, melaleuca alternifolia leaf extract"

//     },
//     {
//         "ProductID": '4', //make sure this part is hidden when I receive it 
//         "ProductName": 'Cicaplast Baume Lèvres',
//         "Quantity": '7,5ml',
//         "Brand": 'la-roche-posay',
//         "Ingredients": "caprylic/capric triglyceride, ppg-5 pentaerythrityl ether, peg-5 pentaerythrityl ether, butyrospermum parkii butter/shea butter, cera alba/beeswax, panthenol, hydrogenated vegetable oil, ethylhexyl palmitate, silica silylate, polybutene, glycine soja/soybean stereols, aqua/water, sodium saccharin, myristyl malate phosphonic acid, pentaerythrityl tetra-di-t-butyl hydroxyhydrocinnamate,"
//     },
//     {
//         "ProductID": '5', //make sure this part is hidden when I receive it 
//         "ProductName": 'Anthelios Pocket  Dermo-Pediatrics',
//         "Quantity": '30ml',
//         "Brand": 'la-roche-posay',
//         "Ingredients": "aqua/water, c12-15 alkyl benzoate, glycerin, ethylhexyl salicylate, bis-ethylhexyloxyphenol methoxyphenyl triazine, alcohol denat, diisopropyl sebacate, butyl methoxydibenzoylmethane, drometrizole trisiloxane, propylene glycol, diethylhexyl butamido triazone, dimethicone, synthetic wax, titanium dioxide, potassium cetyl posphate, ammonium polyacryloyldimethyl taurate, caprylyl glycol, disodium edta, glyceryl stearate, hydroxypropyl methylcellulose, isopropyl lauroyl sarcosinate, palmitic acid, peg-100 stearate, pentylene glycol phenoxyethanol, stearic acid, terephthalylidene dicamphor sulfonic acid, tocopherol, triethanolamine"

//     }
    
 

// ]






