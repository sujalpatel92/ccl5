<html>
<body>
<?php
session_start();
$location = $_POST["location"]; 
$piid = $_POST["piid"]; 
$id = $_SESSION["id"]; 
$email = $_SESSION['email'];

$curl = curl_init();
curl_setopt_array($curl, array(
	CURLOPT_RETURNTRANSFER =>1,
	CURLOPT_URL => '35.162.32.72:8005/registerpi/get_pi_confirmation?pi_id='.$piid.'|'.$_SESSION['email'].'|'.$_POST['location'],

	));
$resp = curl_exec($curl);
$rep = curl_getinfo($curl, CURLINFO_HTTP_CODE);
curl_close($curl);

if($rep==200){

$con=mysqli_connect("localhost","root","root","cloudlab4");

if (mysqli_connect_errno())
{ 
		echo "Failed to connect to MySQL: " .mysqli_connect_error();
}
$sql = "insert into piinfo (id,location,piid) VALUES ($id,'$location','$piid')";

$result = mysqli_query($con, $sql);

header("Location: welcome.php");
	
}
else if($rep==403){
	echo "This Device ID is already Registered with us. Please check and Register your device again. <br><br>";
	?>
	<form action = "welcome.php" method = "post">
	<input type = "submit" value = "Back"></input>
	</form>
	<?php
}
else{
	echo "Device is not yet registered. First run script on Raspberry PI and then Register your device<br><br>";
	?>
	<form action = "welcome.php" method = "post">
	<input type = "submit" value = "Back"></input>
</form>
<?php
}
mysqli_close($con);

?>

</body>
</html>
