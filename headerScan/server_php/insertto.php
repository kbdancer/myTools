<?php

    $db_name = 'scan_header';
    $db_user = 'ipdb';
    $db_pass = 'uJMt8LBPEImsQzaH';
    $db_host = 'localhost';

	$conn = @mysql_connect($db_host,$db_user,$db_pass);
	if (!$conn){ echo json_encode(array('code'=>88));exit;}
	mysql_select_db($db_name, $conn);
	mysql_query("set names utf8");

	$server_ip = addslashes($_POST['ip']);
	$server_port = addslashes($_POST['port']);
	$server_server = addslashes($_POST['server']);
	$server_title = addslashes($_POST['title']);

	if(strlen($server_ip) < 1){
		echo json_encode(array('code'=>-1,"msg"=>"IP can not be empty."));
		exit;
	}

	$hash = md5($server_ip.$server_port.$server_server.$server_title);
	$check = sprintf("SELECT id FROM info where hash='%s'", $hash);
	$checkRes = mysql_query($check);

	if(mysql_fetch_array($checkRes)[0] > 0){
		echo json_encode(array('code'=>-1,"msg"=>"IP has been exist."));
		exit;
	}else{
		$remote_host = $_SERVER["REMOTE_ADDR"];
		$insertServer = sprintf(
			"INSERT INTO info(ip,port,server,title,client,hash) VALUES('%s','%s','%s','%s','%s','%s')",
			mysql_real_escape_string($server_ip),
			mysql_real_escape_string($server_port),
			mysql_real_escape_string($server_server),
			mysql_real_escape_string($server_title),
			mysql_real_escape_string($remote_host),
			mysql_real_escape_string($hash)
		);

		$saveRes = mysql_query($insertServer);

		if($saveRes){
			echo json_encode(array("code"=>0));
		}else{
			echo json_encode(array("code"=>-1,"msg"=>"Save Failed."));
		}
		exit;
	}
?>
