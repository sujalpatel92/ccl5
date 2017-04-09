<?php
session_start();

$data = array("pi_id" => $_SESSION['piidON'], "light" => "off", "Email" => $_SESSION['email']);                                                                    
$data_string = json_encode($data);                                                                                   
                                                                                                                     
$ch = curl_init('35.162.32.72:8000/light/status');                                                                      
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");                                                                     
curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);                                                                  
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);                                                                      
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));                                                                                                                   
                                                                                                                     
$result = curl_exec($ch);
curl_close($ch);
header("Location: welcome.php");
?>