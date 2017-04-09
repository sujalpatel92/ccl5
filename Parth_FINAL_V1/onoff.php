<html>
<body>
<script>
$("#onbutton").on('click', function() {
 <?php echo "ON";?>
});
$("#offbutton").on('click', function() {
  <?php echo "OFF";?>
});
</script>
<form method = "post">

  <input id = "DeviceID" type = "text" placeholder="Enter Device ID"><br><br>

  <button id = "onbutton" type = "submit">On</button>
  <button id = "offbutton" type = "submit">OFF</button>

</form>
</body>
</html>