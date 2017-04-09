<?php

session_start();


$piid = $_SESSION['piidON'];
$email = $_SESSION["email"];
$curl = curl_init();
curl_setopt_array($curl, array(
	CURLOPT_RETURNTRANSFER =>1,
	CURLOPT_URL => '35.162.32.72:8005/getlogs?pi_id='.$piid.'|'.$_SESSION['email'],));
$resp = curl_exec($curl);
$rep = curl_getinfo($curl, CURLINFO_HTTP_CODE);

echo $resp;

curl_close($curl);
header("Location:" .$resp);
exit();

?>
