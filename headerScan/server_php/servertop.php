<?php

    $dbms='mysql';     //数据库类型
    $host='localhost'; //数据库主机名
    $dbName='scan_header';    //使用的数据库
    $user='scanner';      //数据库连接用户名
    $pass='scanner';          //对应的密码
    $dsn="$dbms:host=$host;dbname=$dbName";

    try {
        $dbh = new PDO($dsn, $user, $pass);
        $dbh->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

        $querySql = "SELECT count(server) as number,server FROM `info` group by server ORDER BY number desc limit 500";
        $stmt = $dbh->prepare($querySql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
        $stmt->execute();
        $index = 1;
        echo '<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><style type="text/css">a{text-decoration: none;}table{width: 100%;table-layout: fixed; border-right: #ccc 1px solid;border-top: #ccc 1px solid;}table td,table th{color: #555; text-align: left; font-size: 12px;padding: 2px 5px;border-left: #ccc 1px solid;border-bottom: #ccc 1px solid;}</style></head><body><table cellpadding="0" cellspacing="0"><tr><th width="50">编号</th><th width="80">主机数</th><th>服务器类型</th></tr>';
        while ($row = $stmt->fetch()) {
            echo '<tr><td>'.$index++.'</td><td>'.$row['number'].'</td><td>'.$row['server'].'</td></tr>';
        }
        echo '</table></body></html>';
        $stmt->closeCursor();
        $dbh = null;
    } catch (PDOException $e) {
        die ("Error!: " . $e->getMessage() . "<br/>");
    }
?>
