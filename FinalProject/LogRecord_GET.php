<?php
    $host = "localhost";
    $dbuser = "root";
    $dbpasswd = "123456";
    $DBNAME = "final_data";

    if(isset($_GET['temp'])){
        $conn = mysqli_connect($host, $dbuser, $dbpasswd, $DBNAME);
        if(!$conn) {
            echo "Error: Unable to connect to MySQL." . PHP_EOL;
            echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
            echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;    
            die ("無法連接資料庫");
        }
        // 設定連線編碼
        mysqli_query($conn, "SET NAMES 'utf8'");

        $sql = sprintf("INSERT INTO log (`time`,`temp`,`wet`,`light`)
            VALUES (NOW(),'%s','%s','%s');",
            $_GET['temp'],$_GET['wet'],$_GET['light']
        );
        $ret = mysqli_query($conn, $sql);

        if(!$ret){
            echo "Error: Unable to connect to MySQL." . PHP_EOL;
            echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
            echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;    
            die("insert error");
        }else{
            echo "Records created successfully\n";
        }
        mysqli_close($conn);
    }else{
        die("Error");
    }
?>