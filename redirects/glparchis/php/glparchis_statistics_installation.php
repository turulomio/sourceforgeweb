<?php
if (isset($_GET['installations_uuid'])==False){
    echo "NO PRODUCCION No están todas las variables";
    exit;
}

if (is_string($_GET['installations_uuid']) && preg_match('/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/', $_GET['installations_uuid'])==False) {
    echo "Don't play with my installations_uuid";
    exit;
}


$mysqli = new mysqli('mysql-g', 'g158664rw', 'SQLGLcom','g158664_glparchis');
if ($mysqli->connect_errno) {
    echo "Lo sentimos, no me he podido conectar a la base de datos.";
//    echo "Error no mostrable en producción: Fallo al conectarse a MySQL debido a: \n";
//    echo "Errno: " . $mysqli->connect_errno . "\n";
//    echo "Error: " . $mysqli->connect_error . "\n";
    exit;
}

 $installations_uuid=$mysqli->real_escape_string($_GET['installations_uuid']);

 $cur=$mysqli->query("SELECT count(uuid) from installations where uuid='$installations_uuid'");$row= $cur->fetch_row();
 if($row[0]==0){
 	echo "Installation $installations_uuid not found";
 	exit;
}

echo "<html>";
echo "<body>";

echo "<h1>Games</h1>";
echo "<ul>";
$cur=$mysqli->query("SELECT count(*) from games where installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
$totalgames=$row[0];
echo "<li>Total games played: " .$totalgames."</li>";

$cur=$mysqli->query("SELECT count(*) from games where starts>=DATE(NOW()) - INTERVAL 30 DAY and installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
echo "<li>Games played in the last 30 days: " .$row[0]."</li>";

$cur=$mysqli->query("SELECT count(*) from games where ends is not null  and installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
$totalfinishedgames=$row[0];
echo "<li>Games finished: " . 100*$totalfinishedgames/$totalgames . " %</li>";

$cur=$mysqli->query("SELECT count(*) from games where ends is not null and human_won=1 and installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
echo "<li>Finished games won by humans: " . $row[0]/$totalfinishedgames*100 ." %</li>";
echo "</ul>";

echo "<h1>Game modes</h1>";
echo "<ul>";
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=3 and installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
echo "<li>Number of games in 3 players mode: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=4 and installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
echo "<li>Number of games in 4 players mode: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=6 and installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
echo "<li>Number of games in 6 players mode: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=8 and installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
echo "<li>Number of games in 8 players mode: " .$row[0]."</li>";
echo "</ul>";

echo "<ul>";
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=3 and ends is not null and installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
echo "<li>Number of games finished in 3 players mode: " .$row[0]."</li>";
$totalended3=$row[0];
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=4 and ends is not null and installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
echo "<li>Number of games finished in 4 players mode: " .$row[0]."</li>";
$totalended4=$row[0];
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=6 and ends is not null and installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
echo "<li>Number of games finished in 6 players mode: " .$row[0]."</li>";
$totalended6=$row[0];
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=8 and ends is not null and installations_uuid='$installations_uuid'");$row= $cur->fetch_row();
echo "<li>Number of games finished in 8 players mode: " .$row[0]."</li>";
$totalended8=$row[0];
echo "</ul>";

echo "<ul>";
$cur=$mysqli->query("SELECT timestampdiff(SECOND,starts,ends)/60 as duration from games where maxplayers=3 and ends is not null and installations_uuid='$installations_uuid' order by duration limit " . (ceil($totalended3/2) -1) . ", 1");$row=$cur->fetch_row();
echo "<li>Median minutes to end a 3 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT timestampdiff(SECOND,starts,ends)/60 as duration from games where maxplayers=4 and ends is not null and installations_uuid='$installations_uuid' order by duration limit " . (ceil($totalended4/2) -1) . ", 1");$row=$cur->fetch_row();
echo "<li>Median minutes to end a 4 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT timestampdiff(SECOND,starts,ends)/60 as duration from games where maxplayers=6 and ends is not null and installations_uuid='$installations_uuid' order by duration limit " . (ceil($totalended6/2) - 1) . ", 1");$row=$cur->fetch_row();
echo "<li>Median minutes to end a 6 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT timestampdiff(SECOND,starts,ends)/60 as duration from games where maxplayers=8 and ends is not null and installations_uuid='$installations_uuid' order by duration limit " . (ceil($totalended8/2) - 1) . ", 1");$row=$cur->fetch_row();
echo "<li>Median minutes to end a 8 players game: " .$row[0]."</li>";
echo "</ul>";

echo "<h1>Victories</h1>";
echo "<ul>";
$cur=$mysqli->query("SELECT count(*) from games where ends is not null and human_won=1 and installations_uuid='$installations_uuid' and maxplayers=3");$row= $cur->fetch_row();
echo "<li>Human victories in 3 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where ends is not null and human_won=1 and installations_uuid='$installations_uuid' and maxplayers=4");$row= $cur->fetch_row();
echo "<li>Human victories in 4 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where ends is not null and human_won=1 and installations_uuid='$installations_uuid' and maxplayers=6");$row= $cur->fetch_row();
echo "<li>Human victories in 6 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where ends is not null and human_won=1 and installations_uuid='$installations_uuid' and maxplayers=8");$row= $cur->fetch_row();
echo "<li>Human victories in 8 players game: " .$row[0]."</li>";
echo "</ul>";


 $cur.close();
 $mysqli->close();


echo "</html>";
echo "</body>";
?>
