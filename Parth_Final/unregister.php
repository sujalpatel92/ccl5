<?php
session_start();
$location = $_POST["location"]; 
$piid = $_POST["piid"]; 
$id = $_SESSION["id"]; 
$email = $_SESSION['email'];

$curl = curl_init();
curl_setopt_array($curl, array(
	CURLOPT_RETURNTRANSFER =>1,
	CURLOPT_URL => '35.162.32.72:8000/deregisterpi?pi_id='.$piid.'|'.$_SESSION['email'],

	));
$resp = curl_exec($curl);
$rep = curl_getinfo($curl, CURLINFO_HTTP_CODE);
curl_close($curl);

if($rep == 200){

$con=mysqli_connect("localhost","root","root","cloudlab4");
if (mysqli_connect_errno())
{ 
		echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
$sql = "DELETE FROM piinfo where id = $id AND location = '$location' AND piid = '$piid'";

$result = mysqli_query($con, $sql);

header("Location: welcome.php");
}

mysqli_close($con);



?>
