<?php

    $db_name = 'scan_header';
    $db_user = 'ipdb';
    $db_pass = 'uJMt8LBPEImsQzaH';
    $db_host = 'localhost';

    $conn = @mysql_connect($db_host,$db_user,$db_pass);
    if (!$conn){ echo json_encode(array('code'=>88));exit;}
    mysql_select_db($db_name, $conn);
    mysql_query("set names utf8");

    $keywords = $_GET['k'];
    $port = $_GET['p'];
    $server = $_GET['s'];
    $ip = $_GET['ip'];
    $kw = $_GET['kw'];

    if(strlen($kw)>0){
        $selectServer = sprintf("select ip,port,server,title from info where title='%s' order by createtime desc",mysql_real_escape_string($kw));
    }else{
        if (strlen($keywords)<1 && strlen($port)<1 && strlen($server)<1 && strlen($ip)<1){
            echo '<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><body>至少得有一个查询条件</body></html>';
            exit();
        }

        $selectServer = sprintf(
            "select ip,port,server,title from info where title like '%s%s%s' and port like '%s%s%s' and server like '%s%s%s' and ip like '%s%s%s' order by createtime desc",
            mysql_real_escape_string('%'),
            mysql_real_escape_string($keywords),
            mysql_real_escape_string('%'),
            mysql_real_escape_string('%'),
            mysql_real_escape_string($port),
            mysql_real_escape_string('%'),
            mysql_real_escape_string('%'),
            mysql_real_escape_string($server),
            mysql_real_escape_string('%'),
            mysql_real_escape_string('%'),
            mysql_real_escape_string($ip),
            mysql_real_escape_string('%')
        );
    }

    $checkRes = mysql_query($selectServer);
    $index = 1;
    echo '<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><body>';
    while($row = mysql_fetch_array($checkRes)){
        echo '<p style="font-size:12px;padding:0;margin:0;">['.$index++.'] 链接：<a target="_blank" href="http://'.$row['ip'].':'.$row['port'].'">http://'.$row['ip'].':'.$row['port'].'</a> 服务器：'.$row['server'].' 标题：'.$row['title'].'</p>';
    }
?>
