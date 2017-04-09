<?php
session_start();
$check = 'tanpa';
$_SESSION['check'] = $check;
header("Location: welcome.php");

?>