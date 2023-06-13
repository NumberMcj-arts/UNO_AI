<?php
	//echo 'zack</br>';
	$path = "/home/debian/database/sample.json";
	$json_str = file_get_contents($path);
	$json_data = json_decode($json_str, true);
	//$argument = $_POST['val'];
	// $_POST['b'];
	//$path = '/home/debian/Prog_austoben/KI-Projekte/UNO_AI_Web/';
	//$cmd = 'test3.py';
	//$total_cmd = 'python ' . $path . $cmd;
	
	//echo $total_cmd . '</br>';
	
	//$result = shell_exec($total_cmd);
	//echo $json_data["CurrentPlayerIndex"];
	echo $json_str;
?>