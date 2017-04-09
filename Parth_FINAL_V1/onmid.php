<?php

session_start();
$piid =  $_POST['piid'];
$_SESSION['piidON'] = $piid;
$babyNames[]=array();

$babyNames[] = $piid."|".$_SESSION['email'];
echo json_encode($babyNames);

?>
