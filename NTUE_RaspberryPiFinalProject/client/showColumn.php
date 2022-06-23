<?php
    $host = "192.168.43.221";
    $dbuser = "wpuser";
    $dbpasswd = "123456";
    $DBNAME = "final_data";
    $conn = mysqli_connect($host, $dbuser, $dbpasswd, $DBNAME);
    if(!$conn) {
        echo "Error: Unable to connect to MySQL." . PHP_EOL;
        echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
        echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
        die ("無法連線至資料庫");
    }
    // 設定連線編碼
    mysqli_query($conn, "SET NAMES 'utf8'");
    $sql = "SELECT * FROM final_data.log ORDER BY \"time\" DESC;";
    $ret = mysqli_query($conn, $sql);
    if(!$ret){
        echo "Error: Unable to connect to MySQL." . PHP_EOL;
        echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
        echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
        die("error");
    }
    mysqli_close($conn);
?>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
    <title>溫溼度紀錄</title>
</head>
<?php header('refresh: 5;url="http://192.168.43.160/showColumn.php"') ?>
<style>
    .table td {
        text-align: center;
    }
</style>
<body>

<nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <!-- Brand -->
    <a class="navbar-brand">Medicine Control System</a>
    <!-- Links -->
    <ul class="navbar-nav">
        <li class="nav-item">
            <a class="nav-link" href="/showChart.php">Charts</a>
        </li>
        <li class="nav-item">
            <a class="nav-link">Columns</a>
        </li>
    </ul>
</nav>

<div class="container">
    <h1 style="text-align: center; margin-top: 1rem;">遠端資料圖表</h1>
    <div class="row">
        <div class="col">
            <div class="table-responsive">
                <table class="table table-bordered">
                    <thead>
                    <tr>
                        <th>時間</th>
                        <th>溫度</th>
                        <th>濕度</th>
                        <th>燈號</th>
                    </tr>
                    </thead>
                    <tbody>
                    <?php
                        while($row = mysqli_fetch_array($ret, MYSQLI_NUM)){
                            echo "<tr>";
                            echo "<td>".$row[1] ."</td>\n";
                            echo "<td>".$row[2] ."</td>\n";
                            echo "<td>".$row[3] ."</td>\n";

                            if ($row[4]=="1"){
                                echo "<td>";
                                echo "<font color=\"red\">";
                                echo "●";
                                echo "</font>";
                                echo "</td>\n";
                            }
                            if ($row[4]=="2"){
                                echo "<td>";
                                echo "<font color=\"yellow\">";
                                echo "●";
                                echo "</font>";
                                echo "</td>\n";
                            }
                            if ($row[4]=="3"){
                                echo "<td>";
                                echo "<font color=\"green\">";
                                echo "●";
                                echo "</font>";
                                echo "</td>\n";
                            }

                            echo "</tr>";
                        }
                    ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

</body>
</html>
