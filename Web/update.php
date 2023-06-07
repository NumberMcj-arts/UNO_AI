<?php
	//echo 'zack</br>';
	$argument = $_POST['val'];
	// $_POST['b'];
	$path = '/home/debian/Prog_austoben/KI-Projekte/UNO_AI_Web/';
	$cmd = 'test3.py';
	$total_cmd = 'python ' . $path . $cmd;
	
	//echo $total_cmd . '</br>';
	
	$result = shell_exec($total_cmd);
	echo $result . "Fettsack";
?>