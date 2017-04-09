<?php
session_start();

$data = array("pi_id" => $_SESSION['piidON'], "light" => "on", "Email" => $_SESSION['email']);                                                                    
$data_string = json_encode($data);                                                                                   
                                                                                                                     
$ch = curl_init('35.162.32.72:8005/light/status');                                                                      
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");                                                                     
curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);                                                                  
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);                                                                      
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));                                                                                                                   
                                                                                                                     
$result = curl_exec($ch);
$rep = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if($rep == 200){

header("Location: welcome.php");

}
else{
	echo "Error Turning On the light<br><br>";
	?>
	<form action = "welcome.php" method = "post">
	<input type = "submit" value = "Back"></input>
</form>
<?php

}

?>
