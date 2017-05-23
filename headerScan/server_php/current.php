<?php

    $db_name = 'scan_header';
    $db_user = 'ipdb';
    $db_pass = 'uJMt8LBPEImsQzaH';
    $db_host = 'localhost';

    $conn = @mysql_connect($db_host,$db_user,$db_pass);
    if (!$conn){ echo json_encode(array('code'=>88));exit;}
    mysql_select_db($db_name, $conn);
    mysql_query("set names utf8");

    $limit = $_GET['limit'];

    if(empty($limit)){
        $limit = 100;
    }

    if($limit > 100){
        echo '<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><body>请付费</body></html>';
        exit();
    }

    $selectServer = sprintf(
        "select ip,port,server,title,createtime from info order by createtime desc limit %s",
        mysql_real_escape_string($limit)
    );
    $checkRes = mysql_query($selectServer);
    $index = 1;
    echo '<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><body><b>本次查询设置为最多返回'.$limit.'条结果</b>';
    while($row = mysql_fetch_array($checkRes)){
        echo '<p style="font-size:12px;padding:0;margin:0;">['.$index++.']['. $row['createtime'] .'] 链接：<a target="_blank" href="http://'.$row['ip'].':'.$row['port'].'">http://'.$row['ip'].':'.$row['port'].'</a> 服务器：'.$row['server'].' 标题：'.$row['title'].'</p>';
    }
    echo '</body></html>';
?>
