<?php

    $db_name = 'scan_header';
    $db_user = 'ipdb';
    $db_pass = 'uJMt8LBPEImsQzaH';
    $db_host = 'localhost';

    $conn = @mysql_connect($db_host,$db_user,$db_pass);
    if (!$conn){ echo json_encode(array('code'=>88));exit;}
    mysql_select_db($db_name, $conn);
    mysql_query("set names utf8");
    $selectServer = 'SELECT count(server) as number,server FROM `info` group by server ORDER BY number desc limit 500';
    $checkRes = mysql_query($selectServer);
    $index = 1;
    echo '<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><body>';
    while($row = mysql_fetch_array($checkRes)){
        echo '<p style="font-size:12px;padding:0;margin:0;">['.$index++.'] 主机数：'.$row['number'].' 服务器：'.$row['server'].'</p>';
    }
?>
