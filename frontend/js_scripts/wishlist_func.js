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
    ingredient_list = result["ingredients_text"];
   
    



   div_string = `
    <div class="float-container" id='wish-${num}'>
        <div class="float-child first-box">
            <div class="product-item">
            
            <br>
            <h4 style="color:rgb(245,49,99,0.7)"> ${product_name}</h4>
            <span style="color:rgb(245,49,99,0.6)"><b>ProductID:</b></span>
            <span id='product-${num}'>${product_id}</span> 
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
        <div class="float-child second-box" id='remove-box-${num}'>
            <button type="button" class="btn btn-dark" id="btn-${num}" style="font-size:25px" onclick="remove_wishlist_item(product='product-${num}',button_id='btn-${num}',sign='sign-${num}',wish='wish-${num}',remove_box='remove-box-${num}')">-</button>
            <p style="font-size:12px" >remove from wishlist</p>
            <p style="font-size:12px" id="sign-${num}"></p>
    
        </div>
    </div>
    
    `
   // console.log(div_string);
    return div_string 


}

function add_wishlist(wishlist_list){
    len = wishlist_list.length;
    wishlist_string = "";
    for (let i = 0; i < len; i++) {
        product_dict = wishlist_list[i];
        wishlist_string += format_div(product_dict,i+1);
    }
  //  console.log(results_string)
    console.log(wishlist_string)
    document.getElementById("wishlist-items").innerHTML = wishlist_string;

}

function remove_wishlist_item(product,button_id,sign,wish,remove_box){ //idk if I need the variables button-id and sign yet
    // works well with multiple wishlist items 
    
    // console.log("Removed function not impelmented yet");
    var element1= document.getElementById(wish);
    var element2= document.getElementById(remove_box);
    var pro = document.getElementById(product);
    console.log(pro)
    element1.remove();
    element2.remove();
    var userid = parseInt(localStorage.getItem("user_id"))
    var productid = parseInt(pro.innerHTML)
    console.log(typeof(pro.innerHTML))
    fetch(`http://127.0.0.1:5001/wishlist/delete/${userid}/${productid}`) //error handling should go on the next line
    .then( function(response){  //the above endpoint works 
        console.log(response);
        
    }) 
    .catch((error) => {
        console.log("There is probably a network. Check that app.py is running on the backend please")
        console.log(error)
      });


}

//  setInterval(function(){  
    // post_data = {
    //     method: 'POST',
        
    //     headers: {'Content-Type': 'application/json',},
        
    //     body: JSON.stringify({"user_id": '10234'}) // temporary, need real one from user_info side 

    // }

    
    // fetch("http://127.0.0.1:5001/wishlist",post_data) //remember to add error handling for rejected promises etc 
    // .then( function(response){ 
    //         console.log(response);
    //         response.text().then(function(text){ 
    //             console.log(text)
    //             wishlist_result = text ;
    //             parsed_list = JSON.parse(wishlist_result)
              
    //             add_wishlist(parsed_list);
               
    //         });
    // })
    // .catch((error) => {
    //     console.log("There is probably a network. Check that app.py is running on the backend please")
    //     console.log(error)
    // })
   
    var user_id = parseInt(localStorage.getItem("user_id"))
    fetch(`http://127.0.0.1:5001/wishlist/${user_id}`) //this style works 
    .then( function(response){ 
        console.log(response);
        response.text().then(function(text){ 
            console.log(text)
            wishlist_result = text ;
            parsed_list = JSON.parse(wishlist_result)
            
            add_wishlist(parsed_list);
            
        });
    })
    .catch((error) => {
        console.log("There is probably a network. Check that app.py is running on the backend please")
        console.log(error)
    })


        
    
// },1000)