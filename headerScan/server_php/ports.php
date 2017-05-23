<?php

    $db_name = 'scan_header';
    $db_user = 'ipdb';
    $db_pass = 'uJMt8LBPEImsQzaH';
    $db_host = 'localhost';


    $conn = @mysql_connect($db_host,$db_user,$db_pass);
    if (!$conn){ echo json_encode(array('code'=>88));exit;}
    mysql_select_db($db_name, $conn);
    mysql_query("set names utf8");

    $selectServer = "select port from ports where enable = 1 order by port";
    $checkRes = mysql_query($selectServer);
    $res = array();
    while($row = mysql_fetch_array($checkRes)){
        array_push($res,(int)$row['port']);
    }
    echo json_encode(array("data"=>$res));
?>
