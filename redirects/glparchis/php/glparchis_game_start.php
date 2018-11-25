<?php
//`uuid`, `installations_uuid`,  `maxplayers`, `numplayers`, `version`

if (isset($_GET['uuid'],$_GET['installations_uuid'],$_GET['maxplayers'],$_GET['numplayers'],$_GET['version'])==False){
    echo "NO PRODUCCION No están todas las variables";
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


if (is_int($_GET['maxplayers'])) {
    echo "Don't play with me maxplayers";
    exit;
}


if (is_int($_GET['numplayers'])) {
    echo "Don't play with me numplayers";
    exit;
}


if (is_int($_GET['version'])) {
    echo "Don't play with me version";
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
$maxplayers=$mysqli->real_escape_string($_GET['maxplayers']);
$numplayers=$mysqli->real_escape_string($_GET['numplayers']);
$version=$mysqli->real_escape_string($_GET['version']);


//Checks installation
$sql = "SELECT uuid from installations where uuid='$uuid'";
$resultado = $mysqli->query($sql);
if ($resultado==0) {
    echo "Installation doesn't exist";
    exit;
}


$sql = "SELECT uuid, installations_uuid from games where uuid='$uuid' and installations_uuid='$installations_uuid'";
if (!$resultado = $mysqli->query($sql)) {
    echo "Lo sentimos, este sitio web está experimentando problemas.";
    echo "Error no mostrable en producción: La ejecución de la consulta falló debido a: \n";
    echo "Query: " . $sql . "\n";
    echo "Errno: " . $mysqli->errno . "\n";
    echo "Error: " . $mysqli->error . "\n";
    exit;
}

if ($resultado->num_rows == 0){
    $sql = "INSERT INTO games (uuid, installations_uuid, starts, maxplayers, numplayers, version) VALUES ('$uuid', '$installations_uuid', now(), $maxplayers,$numplayers,$version)";
    if ($mysqli->query($sql)) {
        echo "Game inserted";
    } else {
        echo "Game not inserted";
        echo "Query: " . $sql . "\n";
        echo "Errno: " . $mysqli->errno . "\n";
        echo "Error: " . $mysqli->error . "\n";
    }
} else { //Ya existe el registro
    echo "Ya existe el registro";
    exit;
}

$resultado->close();
$mysqli->close();
