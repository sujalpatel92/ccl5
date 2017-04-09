<?php
session_start();
$curl = curl_init();
curl_setopt_array($curl, array(
	CURLOPT_RETURNTRANSFER =>1,
	CURLOPT_URL => '35.162.32.72:8005/getlogsiot?email='.$_SESSION["email"],));
$resp = curl_exec($curl);
$rep = curl_getinfo($curl, CURLINFO_HTTP_CODE);

echo $resp;

curl_close($curl);
header("Location:" .$resp);
exit();

?>
