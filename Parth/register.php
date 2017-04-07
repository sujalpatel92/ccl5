<?php
session_start();
$location = $_POST["location"]; 
$piid = $_POST["piid"]; 
$id = $_SESSION["id"]; 
$con=mysqli_connect("localhost","root","root","cloudlab4");

if (mysqli_connect_errno())
{ 
		echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
$sql = "insert into piinfo (id,location,piid) VALUES ($id,'$location','$piid')";

$result = mysqli_query($con, $sql);

header("Location: welcome.php");
	

mysqli_close($con);

?>
