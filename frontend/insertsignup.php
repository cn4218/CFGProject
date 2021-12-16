//php version inserting data

<?php
// Use post method to insert data into db
    if($_SERVER['REQUEST_METHOD'] == 'POST') {
        // name of values to be inserted
        $name = $_POST["name"];
        $address = $_POST["username"];
        $address = $_POST["password"];
        $age = $_POST["email"];


        $dbhost = "localhost"; // insert host name for sql ('localhost')
        $username = "root"; // insert username for sql ('root')
        $password = "yourpassword"; //password for sql
        $dbname = "Test"; //db name ('user_info' most likely)

        $mysql = mysqli_connect($dbhost, $username, $password, $dbname); //It connects
        // insert into 'table name' 'table columns' ... the following values
        $query = "INSERT INTO Testing (name,username,password,email) VALUES $name, $username, $password, $email";
        mysqli_query($mysql, $query);
    }
?>
<!DOCTYPE html>
<html>
<head>.......
 <!-- set characters to utf-8 which means code can be read by a computer
    (turns it into a binary)-->
    <meta charset="utf-8">
    <title>Create an Account</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
    <style>
        html, body {
            display: flex;
            justify-content: center;
            font-family: Roboto, Arial, sans-serif;
            font-size: 15px;
        }
        form {
            border: 5px solid #f1f1f1;
        }
        input[type=text], input[type=password] {
            width: 100%;
            padding: 16px 8px;
            margin: 8px 0;
            display: inline-block;
            border: 1px solid #ccc;
            box-sizing: border-box;
        }
        button {
            background-color: seagreen;
            color: white;
            padding: 14px 0;
            margin: 10px 0;
            border: none;
            cursor: grabbing;
            width:  100%
        }
        h1 {
            text-align: center;
            font-size: 20px
        }
        .formcontainer {
            text-align: left;
            margin: 25px 50px 12px;
        }
        .container {
            padding: 16px 0;
            text-align: left;
        }
    </style>
    </head>
    <body>
    <form method="post">
    <div class="container">
            <div class="row">
              <div class="column">
                <h1>Sign Up Form</h1>
              </div>
            </div>
            <div class="row">
              <div class="column">
                <form>
                <label for="nameField">Name</label>
                <input
                    name="name"
                    type="text"
                    autofocus placeholder="Insert first and last name"
                    id="nameField"
                    class = "form-control"
                />
                <label for="emailField">Email Address</label>
                <input
                    name="email"
                    type="text"
                    autofocus placeholder="Insert email address"
                    id="emailField"
                    class = "form-control"
                />
                <label for="passwordField">Password</label>
                <input
                    name="password"
                    autofocus placeholder="Create a password"
                    type="text"
                    id="passwordField"
                    class = "form-control"
                />
                <input class="button-primary" type="submit" value="Signup"/>
    </form>
    </body>
</html>
