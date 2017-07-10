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

        $keywords = $_GET['k'];
        $port = $_GET['p'];
        $server = $_GET['s'];
        $ip = $_GET['ip'];
        $kw = $_GET['kw'];

        if(strlen($kw)>0){
            $querySql = "select ip,port,server,title,createtime from info where title = :title order by createtime desc";
            $stmt = $dbh->prepare($querySql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
            $stmt->bindValue(':title',$kw);
        } else{
            if (strlen($keywords)<1 && strlen($port)<1 && strlen($server)<1 && strlen($ip)<1){
                echo '<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><body>至少得有一个查询条件</body></html>';
                exit();
            }
            $querySql = "select ip,port,server,title,createtime from info where title like :title and port like :port and server like :server and ip like :ip order by createtime desc";
            $stmt = $dbh->prepare($querySql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
            $stmt->bindValue(':title','%'.$keywords.'%');
            $stmt->bindValue(':port','%'.$port.'%');
            $stmt->bindValue(':server','%'.$server.'%');
            $stmt->bindValue(':ip','%'.$ip.'%');
        }

        $stmt->execute();
        $index = 1;
        echo '<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><style type="text/css">a{text-decoration: none;}table{width: 100%;table-layout: fixed; border-right: #ccc 1px solid;border-top: #ccc 1px solid;}table td,table th{color: #555; text-align: left; font-size: 12px;padding: 2px 5px;border-left: #ccc 1px solid;border-bottom: #ccc 1px solid;}</style></head><body><table cellpadding="0" cellspacing="0"><tr><th width="50">编号</th><th width="180">主机</th><th>服务器</th><th>标题</th><th width="130">入库时间</th></tr>';
        while ($row = $stmt->fetch()) {
            echo '<tr><td>'.$index++.'</td><td><a target="_blank" href="'. ($row['port'] == 443 ? 'https':'http') .'://'.$row['ip'].':'.$row['port'].'">'. ($row['port'] == 443 ? 'https':'http') .'://'.$row['ip'].':'.$row['port'].'</a></td><td>'.$row['server'].'</td><td>'.$row['title'].'</td><td>'.$row['createtime'].'</td></tr>';
        }
        echo '</table></body></html>';
        $stmt->closeCursor();
        $dbh = null;
    } catch (PDOException $e) {
        die ("Error!: " . $e->getMessage() . "<br/>");
    }
?>
