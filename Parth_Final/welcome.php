<html>
<link rel="stylesheet" href="style.css">
<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
  <script type="text/javascript">
$(document).ready(function(){
    $(".onBtn").click(function(e){
        e.preventDefault();
        var piid = ($(this).attr('id'));
        $.ajax({
      
         url:"onmid.php",
         type: "POST",
         cache: false,
        dataType: 'json',
        data : {'piid':piid},
        success: function(data){        
        $(".target").append(data); 
        window.location.href = 'on.php';         
        }
        

        });
      });

     $(".offBtn").click(function(e){
        e.preventDefault();
        var piid = ($(this).attr('id'));
        $.ajax({
      
         url:"onmid.php",
         type: "POST",
         cache: false,
        dataType: 'json',
        data : {'piid':piid},
        success: function(data){        
        $(".target").append(data); 
        window.location.href = 'off.php';         
        }
        

        });
      });
});
</script>
<body>
<?php
session_start();
$id = $_SESSION["id"];
echo "<h3>Welcome " .$_SESSION["fname"]." ".$_SESSION["lname"].",</h3>";
?>
<form action = "logout.php" method = "post">
  <input type="submit" value="Logout"></input>

</form>
<?php

$con=mysqli_connect("localhost","root","root","cloudlab4");
if (mysqli_connect_errno())
	{ 
		echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}

$sql = "SELECT * FROM piinfo where id = $id ";

$result = mysqli_query($con, $sql);


if(mysqli_num_rows($result)>0){	
	echo "<h2>Your Registered Devices are:</h2>";
	echo "<table><tr><th>Location</th><th>Device ID</th><th>Registration Status</th><th>ON Switch</th><th>OFF Switch</th></tr>";
	while($row = mysqli_fetch_assoc($result)){
	echo "<tr><td>".$row['location']."</td><td>".$row['piid'].
  "</td><td>".$row['status'].
  "</td><td><button type='button' class='onBtn' id = ".$row['piid']." value = 'Turn ON'>Turn on</button></td><td><button type='button' class='offBtn' id = ".$row['piid']." value = 'Turn OFF'>Turn OFF</button></td>
  </tr>";

}
echo "</table>";
}
else{
	echo "You do not have any device registered with us. Please Register a device<br>";
}

mysqli_close($con);
?>


<button onclick="document.getElementById('id01').style.display='block'" style="width:auto;">Register</button>
<button onclick="document.getElementById('id02').style.display='block'" style="width:auto;">UnRegister</button>
<div id="id02" class="modal">
  
  <form class="modal-content animate" action="unregister.php" method = "post">
      <span onclick="document.getElementById('id02').style.display='none'" class="close" title="Close Modal">&times;</span>

    <div class="container">
      <label><b>Location</b></label>
      <input type="text" placeholder="Enter Location (home or office)" name="location" required>

      <label><b>Raspberry PI ID </b></label>
      <input type="text" placeholder="ID of PI (CLOUDXXX)" name="piid" required>
        
    </div>

    <div class="clearfix">
      <button type="button" onclick="document.getElementById('id02').style.display='none'" class="cancelbtn">Cancel</button>
       <button type="submit" class ="signupbtn">UnRegister a Device</button>
    </div>
  </form>
</div>

<div id="id01" class="modal" >
  <span onclick="document.getElementById('id01').style.display='none'" class="close" title="Close Modal">×</span>
 <form action = "check.php" method = "get">
    <input type="submit" value="check"></input>
  </form>
  <form class="modal-content animate" action="register.php" method = "post">
    <div class="container">
      <label><b>Location</b></label>
      <input type="text" placeholder="Location" name="location" required>
       <label><b>Raspberry PI ID</b></label>
      <input type="" value ="<?php session_start(); echo $_SESSION['check']; ?>" name="piid" required>
      <div class="clearfix">  
        <button type="button" onclick="document.getElementById('id01').style.display='none'" class="cancelbtn">Cancel</button>
        <button type="submit" class="signupbtn">Register a Device</button>
      </div>
    </div>
  </form>
</div>


<script>
var modal = document.getElementById('id01');
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

var modal1 = document.getElementById('id01');
window.onclick = function(event) {
    if (event.target == modal1) {
        modal.style.display = "none";
    }
}
</script>
<div class = "target"></div>
</body>	
</html>
