<?php
session_start();
$flag = 0;

$con=mysqli_connect("localhost","root","root","cloudlab4");
// Check connection
if (mysqli_connect_errno())
	{ 
		echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
$sql = "SELECT * FROM user";
$result = mysqli_query($con, $sql);
if(mysqli_num_rows($result)>0){	
	while($row = mysqli_fetch_assoc($result)){
		if($row["email"]==$_POST["email"] && $row["password"] == $_POST["password"]){
			$flag = 1;
		$_SESSION["id"] = $row["id"];
		$_SESSION["email"] = $_POST["email"];
		$_SESSION["fname"] = $row["firstname"];
		$_SESSION["password"] = $_POST["password"];
		$_SESSION["lname"] = $row["lastname"];
		}
}
}
else{
	echo "0 results";
}

if($flag == 1){
header("Location: welcome.php");
exit;
 }
else{
	header("Location: index.html");
	exit;
}

?>