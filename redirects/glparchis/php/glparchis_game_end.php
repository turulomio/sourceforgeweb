
<?php

//`uuid`, `installations_uuid`, `human_won`




if (isset($_GET['uuid'],$_GET['installations_uuid'],$_GET['human_won'])==False){
    echo "Not all variables";
    exit;
}


if (is_string($_GET['uuid']) && preg_match('/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/', $_GET['uuid'])==False) {
    echo "Don't play with me uuid";
    exit;
}

if (is_string($_GET['installations_uuid']) && preg_match('/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/', $_GET['installations_uuid'])==False) {
    echo "Don't play with me installations_uuid";
    exit;
}

if (is_int($_GET['human_won'])) {
    echo "Don't play with me human_won";
    exit;
}


$mysqli = new mysqli('mysql-g', 'g158664rw', 'SQLGLcom','g158664_glparchis');
if ($mysqli->connect_errno) {
//    echo "Lo sentimos, no me he podido conectar a la base de datos.";
//    echo "Error no mostrable en producción: Fallo al conectarse a MySQL debido a: \n";
//    echo "Errno: " . $mysqli->connect_errno . "\n";
//    echo "Error: " . $mysqli->connect_error . "\n";
    exit;
}

$uuid=$mysqli->real_escape_string($_GET['uuid']);
$installations_uuid=$mysqli->real_escape_string($_GET['installations_uuid']);
$human_won=$mysqli->real_escape_string($_GET['human_won']);

$sql = "SELECT uuid, installations_uuid from games where uuid='$uuid' and installations_uuid='$installations_uuid' and ends is null";
if (!$resultado = $mysqli->query($sql)) {
    echo "Lo sentimos, este sitio web está experimentando problemas.";
    echo "Error no mostrable en producción: La ejecución de la consulta falló debido a: \n";
    echo "Query: " . $sql . "\n";
    echo "Errno: " . $mysqli->errno . "\n";
    echo "Error: " . $mysqli->error . "\n";
    exit;
}

if ($resultado->num_rows == 0){
   echo "Game doesn't exist";
} else {
    $sql = "UPDATE games set ends=now(), human_won=$human_won  where uuid='$uuid' and installations_uuid='$installations_uuid'";
    if ($mysqli->query($sql)) {
        echo "Game ended";
    } else {
        echo "Game failed to end";
        echo "Query: " . $sql . "\n";
        echo "Errno: " . $mysqli->errno . "\n";
        echo "Error: " . $mysqli->error . "\n";
    }
}

$resultado->close();
$mysqli->close();
