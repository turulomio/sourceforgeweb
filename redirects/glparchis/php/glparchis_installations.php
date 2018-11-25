
<?php
function get_client_ip() {
    $ipaddress = '';
    if (isset($_SERVER['HTTP_CLIENT_IP']))
        $ipaddress = $_SERVER['HTTP_CLIENT_IP'];
    else if(isset($_SERVER['HTTP_X_FORWARDED_FOR']))
        $ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR'];
    else if(isset($_SERVER['HTTP_X_FORWARDED']))
        $ipaddress = $_SERVER['HTTP_X_FORWARDED'];
    else if(isset($_SERVER['HTTP_FORWARDED_FOR']))
        $ipaddress = $_SERVER['HTTP_FORWARDED_FOR'];
    else if(isset($_SERVER['HTTP_FORWARDED']))
        $ipaddress = $_SERVER['HTTP_FORWARDED'];
    else if(isset($_SERVER['REMOTE_ADDR']))
        $ipaddress = $_SERVER['REMOTE_ADDR'];
    else
        $ipaddress = 'UNKNOWN';
    return $ipaddress;
}

if (isset($_GET['uuid'])==False) {
    echo "Some parameter is missing";
    exit;
}

if (preg_match('/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/', $_GET['uuid'])==False) {
    echo "It's not an uuid";
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
$ip=$mysqli->real_escape_string(get_client_ip());

$sql = "SELECT uuid from installations where uuid='$uuid'";
if (!$resultado = $mysqli->query($sql)) {
//    echo "Lo sentimos, este sitio web está experimentando problemas.";
//    echo "Error no mostrable en producción: La ejecución de la consulta falló debido a: \n";
//    echo "Query: " . $sql . "\n";
//    echo "Errno: " . $mysqli->errno . "\n";
//    echo "Error: " . $mysqli->error . "\n";
    exit;
}

echo $resultado->num_rows;

if ($resultado->num_rows == 0){
    $sql = "INSERT INTO installations (uuid, datetime, ip4) VALUES ('$uuid', now(), '$ip')";
    if ($mysqli->query($sql)) {
        echo "Installation inserted";
    } else {
        echo "Installation not inserted";
//    echo "Query: " . $sql . "\n";
//    echo "Errno: " . $mysqli->errno . "\n";
//    echo "Error: " . $mysqli->error . "\n";
    }
}

$resultado->close();
$mysqli->close();
