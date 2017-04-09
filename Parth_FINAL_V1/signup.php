<?php
session_start();
$fname = $_POST["fname"]; 
$lname = $_POST["lname"]; 
$email = $_POST["email"]; 
$flag = 0;
$password = $_POST["password"]; 
$con=mysqli_connect("localhost","root","root","cloudlab4");

if (mysqli_connect_errno())
	{ 
		echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
$sql = "insert into user (id,firstname,lastname,email,password) VALUES (NULL,'$fname','$lname','$email','$password')";

$result = mysqli_query($con, $sql);

header("Location: index.html");
	

mysqli_close($con);

?>
