<?php
session_start();
$piid =  $_POST['piid'];
$_SESSION['piidON'] = $piid;
$babyNames[]=array();

$babyNames[] = $piid."|".$_SESSION['email'];
echo json_encode($babyNames);



/*
$id = $_POST["id"];
$email = $_SESSION["email"];
$piid = $_POST[]

if($rep==200){

$con=mysqli_connect("localhost","root","root","cloudlab4");

if (mysqli_connect_errno())
{ 
		echo "Failed to connect to MySQL: " .mysqli_connect_error();
}
$sql = "update table ";

$result = mysqli_query($con, $sql);

header("Location: welcome.php");
	
}
*/
?>