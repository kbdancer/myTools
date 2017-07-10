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

        $querySql = "select port from ports where enable = 1 order by port";
        $stmt = $dbh->prepare($querySql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
        $stmt->execute();
        $res = array();
        while ($row = $stmt->fetch()) {
            array_push($res,(int)$row['port']);
        }
        echo json_encode(array("data"=>$res));
        $stmt->closeCursor();
        $dbh = null;
    } catch (PDOException $e) {
        die ("Error!: " . $e->getMessage() . "<br/>");
    }
?>
