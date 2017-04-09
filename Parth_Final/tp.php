<?php

session_start();

$location = $_POST["location"]; 
$piid = $_POST["piid"]; 
$id = $_SESSION["id"]; 
$email = $_SESSION["email"];
$curl = curl_init();
curl_setopt_array($curl, array(
	CURLOPT_RETURNTRANSFER =>1,
	CURLOPT_URL => '35.162.32.72:8000/getlogip?pi_id='.$piid.'|'.$_SESSION['email'],));
$resp = curl_exec($curl);
$rep = curl_getinfo($curl, CURLINFO_HTTP_CODE);
//$op = var_dump(json_decode($resp));
//$op1 = var_dump(json_decode($resp, true)[0]);
//$op2 = json_decode($resp)
/*foreach ($op as $a) 
{ 
	echo $a[0];
}
*/

echo $resp;

curl_close($curl);
header("Location:" .$resp);
exit();