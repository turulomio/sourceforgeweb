<html>
<body>

<?php
$mysqli = new mysqli('mysql-g', 'g158664ro', 'GLSQLcom','g158664_glparchis');
if ($mysqli->connect_errno) {
    echo "Lo sentimos, no me he podido conectar a la base de datos.";
    echo "Errno: " . $mysqli->connect_errno . "\n";
    echo "Error: " . $mysqli->connect_error . "\n";

    exit;
}

echo "<h1>Installations</h1>";
echo "<ul>";
$cur=$mysqli->query("SELECT count(uuid) as count from installations");$row= $cur->fetch_row();
$totalinstallations=$row[0];
echo "<li>Total installations: " .$totalinstallations."</li>";
$cur=$mysqli->query("SELECT count(uuid) as count from installations where datetime>=DATE(NOW()) - INTERVAL 30 DAY");$row= $cur->fetch_row();
echo "<li>Number of installations in the last 30 days: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(distinct(installations_uuid)) as count from games where starts>=DATE(NOW()) - INTERVAL 30 DAY");$row=$cur->fetch_row();
echo "<li>Installations that played in the last 30 days: " . $row[0] ."</li>";
$cur=$mysqli->query("select count(installations_uuid), version from (select max(version) as version, installations_uuid from games group by installations_uuid) t group by version order by version desc limit 1");$row=$cur->fetch_row();
echo "<li>Installations which are in the last version ".$row[1].": " . $row[0] ."</li>";
echo "</ul>";

echo "<h1>Games</h1>";
echo "<ul>";
$cur=$mysqli->query("SELECT count(*) from games");$row= $cur->fetch_row();
$totalgames=$row[0];
echo "<li>Total games played: " .$totalgames."</li>";
$cur=$mysqli->query("SELECT count(*) from games where starts>=DATE(NOW()) - INTERVAL 30 DAY");$row= $cur->fetch_row();
echo "<li>Games played in the last 30 days: " .$row[0]."</li>";
echo "<li>Games per installation: ".$totalgames/$totalinstallations."</li>";
$cur=$mysqli->query("SELECT count(*) from games where ends is not null");$row= $cur->fetch_row();
$totalfinishedgames=$row[0];
echo "<li>Games finished: " . 100*$totalfinishedgames/$totalgames . " %</li>";
$cur=$mysqli->query("SELECT count(*) from games where ends is not null and human_won=1");$row= $cur->fetch_row();
echo "<li>Finished games won by humans: " . $row[0]/$totalfinishedgames*100 ." %</li>";
echo "</ul>";

echo "<h2>Game modes</h2>";
echo "<ul>";
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=3");$row= $cur->fetch_row();
echo "<li>Number of games in 3 players mode: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=4");$row= $cur->fetch_row();
echo "<li>Number of games in 4 players mode: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=6");$row= $cur->fetch_row();
echo "<li>Number of games in 6 players mode: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=8");$row= $cur->fetch_row();
echo "<li>Number of games in 8 players mode: " .$row[0]."</li>";
echo "</ul>";

echo "<ul>";
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=3 and ends is not null");$row= $cur->fetch_row();
echo "<li>Number of games finished in 3 players mode: " .$row[0]."</li>";
$totalended3=$row[0];
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=4 and ends is not null");$row= $cur->fetch_row();
echo "<li>Number of games finished in 4 players mode: " .$row[0]."</li>";
$totalended4=$row[0];
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=6 and ends is not null");$row= $cur->fetch_row();
echo "<li>Number of games finished in 6 players mode: " .$row[0]."</li>";
$totalended6=$row[0];
$cur=$mysqli->query("SELECT count(*) from games where maxplayers=8 and ends is not null");$row= $cur->fetch_row();
echo "<li>Number of games finished in 8 players mode: " .$row[0]."</li>";
$totalended8=$row[0];
echo "</ul>";

echo "<ul>";
$cur=$mysqli->query("SELECT timestampdiff(SECOND,starts,ends)/60 as duration from games where maxplayers=3 and ends is not null order by duration limit " . (ceil($totalended3/2) -1) . ", 1");$row=$cur->fetch_row();
echo "<li>Median minutes to end a 3 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT timestampdiff(SECOND,starts,ends)/60 as duration from games where maxplayers=4 and ends is not null order by duration limit " . (ceil($totalended4/2) -1) . ", 1");$row=$cur->fetch_row();
echo "<li>Median minutes to end a 4 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT timestampdiff(SECOND,starts,ends)/60 as duration from games where maxplayers=6 and ends is not null order by duration limit " . (ceil($totalended6/2) - 1) . ", 1");$row=$cur->fetch_row();
echo "<li>Median minutes to end a 6 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT timestampdiff(SECOND,starts,ends)/60 as duration from games where maxplayers=8 and ends is not null order by duration limit " . (ceil($totalended8/2) - 1) . ", 1");$row=$cur->fetch_row();
echo "<li>Median minutes to end a 8 players game: " .$row[0]."</li>";
echo "</ul>";

echo "<h2>Top players</h2>";
$cur=$mysqli->query("SELECT count(*), installations_uuid FROM games group by installations_uuid order by count(*) desc limit 10");
echo "<ul>";
while($row = $cur->fetch_array()) {
    echo "<li>" . $row[0] . " games played in installation: " . $row[1] . "</li>";
}
echo "</ul>";

echo "<h2>Top players in the last 30 days</h2>";
$cur=$mysqli->query("SELECT count(*), installations_uuid FROM games  where starts>=DATE(NOW()) - INTERVAL 30 DAY group by installations_uuid order by count(*) desc limit 10");
echo "<ul>";
while($row = $cur->fetch_array()) {
    echo "<li>" . $row[0] . " games played in installation: " . $row[1] . "</li>";
}
echo "</ul>";

echo "<h1>Victories</h1>";
echo "<ul>";
$cur=$mysqli->query("SELECT count(*) from games where ends is not null and human_won=1 and maxplayers=3");$row= $cur->fetch_row();
echo "<li>Human victories in 3 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where ends is not null and human_won=1 and maxplayers=4");$row= $cur->fetch_row();
echo "<li>Human victories in 4 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where ends is not null and human_won=1 and maxplayers=6");$row= $cur->fetch_row();
echo "<li>Human victories in 6 players game: " .$row[0]."</li>";
$cur=$mysqli->query("SELECT count(*) from games where ends is not null and human_won=1 and maxplayers=8");$row= $cur->fetch_row();
echo "<li>Human victories in 8 players game: " .$row[0]."</li>";
echo "</ul>";


$cur.close();
$mysqli->close();

?>
