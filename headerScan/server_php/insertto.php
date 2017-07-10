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

        $server_ip = addslashes($_POST['ip']);
        $server_port = addslashes($_POST['port']);
        $server_server = addslashes($_POST['server']);
        $server_title = addslashes($_POST['title']);

        if(strlen($server_ip) < 1){
            echo json_encode(array('code'=>-1,"msg"=>"IP can not be empty."));
            exit;
        }

        $hash = md5($server_ip.$server_port.$server_server.$server_title);
        $checkSql = "SELECT id FROM info where hash = :hash";
        $stmt = $dbh->prepare($checkSql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
        $stmt->bindValue(':hash',$hash);
        $stmt->execute();
        if (count($stmt->fetchAll()) > 0){
            echo json_encode(array('code'=>-1,"msg"=>"IP has been exist."));
            $stmt->closeCursor();
		    exit;
        }else{
            $remote_host = $_SERVER["REMOTE_ADDR"];
            $querySql = "INSERT INTO info(ip,port,server,title,client,hash) VALUES(:ip,:port,:server,:title,:client,:hash)";
			$stmt_insert = $dbh->prepare($querySql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
            $stmt_insert->bindValue(':ip',$server_ip);
            $stmt_insert->bindValue(':port',$server_port);
            $stmt_insert->bindValue(':server',$server_server);
            $stmt_insert->bindValue(':title',$server_title);
            $stmt_insert->bindValue(':client',$remote_host);
            $stmt_insert->bindValue(':hash',$hash);
            $stmt_insert->execute();
            $stmt->closeCursor();
            echo json_encode(array("code"=>0));
        }
		$dbh = null;
	} catch (PDOException $e) {
		die ("Error!: " . $e->getMessage() . "<br/>");
	}
?>
