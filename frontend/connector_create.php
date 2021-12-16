
<?php
    //Connecting to sql db - host name, user name, password and database name
    $servername='localhost';
    $username='root';
    $password='PrineSsFIS4';
    $dbname = "Test";
    // Open connection 
    // Insert localhost, username, password and db name
    $conn=mysqli_connect("localhost","root","PrinceSsFIS4","Test");
    // Check it works
      if(!$conn){
          die('Connection has failed, ' .mysql_error());
        }