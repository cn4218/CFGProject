<?php
// database connection code
// $con = mysqli_connect('localhost', 'database_user', 'database_password','database');

$con = mysqli_connect('localhost', 'root', 'PrinceSsFIS4','Test');

// get the post records
$txtName = $_POST['txtName'];
$txtUsername = $_POST['txtUsername'];
$txtPassword = $_POST['txtPassword'];
$txtEmail = $_POST['txtEmail'];

// database insert SQL code
$sql = "INSERT INTO `Testing` (`Name`, `Username`, `Password`, `Email`) VALUES ('0', '$txtName', '$txtUsername', '$txtPassword', '$txtEmail')";

// insert in database 
$rs = mysqli_query($con, $sql);

if($rs)
// If successful, record that the data has been added
{
	echo "Data added";
}

?>