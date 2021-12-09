function show_active(item_id){
    document.getElementById("Home").className = "nav-link";
    document.getElementById("Results").className = "nav-link";
    document.getElementById("Wishlist").className = "nav-link";
    document.getElementById("Profile").className = "nav-link";
    document.getElementById("Log-out").className = "nav-link";
    


    document.getElementById(item_id).className = "nav-link active";

   
}