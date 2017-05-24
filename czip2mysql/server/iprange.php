<?php
    Header( "Content-type:   application/octet-stream ");
    Header( "Accept-Ranges:   bytes ");
    header( "Content-Disposition:   attachment;   filename=range.txt ");
    header( "Expires:   0 ");
    header( "Cache-Control:   must-revalidate,   post-check=0,   pre-check=0 ");
    header( "Pragma:   public ");

    $db_name = 'ipdb';
    $db_user = 'ipdb';
    $db_pass = 'uJMt8LBPEImsQzaH';
    $db_host = 'localhost';

    $conn = @mysql_connect($db_host,$db_user,$db_pass);
    if (!$conn){ echo json_encode(array('code'=>88));exit;}
    mysql_select_db($db_name, $conn);
    mysql_query("set names utf8");

    $keywords = $_GET['k'];

    if(strlen($keywords)>0){
        $selectServer = sprintf(
            "select iprange from ipdb where location like '%s%s%s'",
            mysql_real_escape_string('%'),
            mysql_real_escape_string($keywords),
            mysql_real_escape_string('%')
        );

        $checkRes = mysql_query($selectServer);
        $index = 1;
        while($row = mysql_fetch_array($checkRes)){
            echo $row['iprange']."\n";
        }
    }else{
        echo '0';
    }
?>
