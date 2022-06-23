<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
    <title>Remote Data</title>
</head>
<?php header('refresh: 5;url="http://192.168.43.160/showChart.php"') ?>
<style>
    img{
        max-width:100%;
        height:auto;
        margin:auto;
        text-align:center;
    }
</style>
<body>

<nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <!-- Brand -->
    <a class="navbar-brand">Medicine Control System</a>
    <!-- Links -->
    <ul class="navbar-nav">
        <li class="nav-item">
            <a class="nav-link">Charts</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="/showColumn.php">Columns</a>
        </li>
    </ul>
</nav>

<div class="container">
    <h1 style="text-align: center; margin-top: 1rem;">遠端資料圖表</h1>
    <div class="row">
        <img src="./outputTemp.jpg" alt="local image can't show up QAQ">
        <img src="./outputWet.jpg" alt="local image can't show up QAQ">
    </div>
    <p></p>
    <p></p>
    <p></p>
</div>

</body>
</html>
