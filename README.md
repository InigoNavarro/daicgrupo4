# daicGrupo4

## Descripción del proyecto:

Este proyecto consistirá en ayudar a la población a hacer un uso adecuado de la mascarilla. Para ello, se utilizará una cámara con inteligencia artificial que detectara si lleva mascarilla o no. Ademas en el caso de que lleve mascarilla, indicará si esta esta bien puesta o no. En caso de que se este haciendo un buen uso de la mascarilla se encenderá una uz verde.En el caso de que no, se encenderá una luz roja y por un altavoz se hara un ruido para que el usuario se de cuenta de la situación.

# Instalación y ejecución del proyecto

## Prerequisitos

Para que esta aplicación funcione correctamente será necesario tener lo siguiente: 
- 2 luces led (una verde y una roja).
- 2 servomotores.
- 1 buzzer.
- 1 sensor ultrasonido.
- 1 Raspberry Pi.
- Tener instalado la version de Python 3.7 o mayor.

## Descarga del programa

Para descargar el programa podremos descargar el código en un zip accediendo a la url https://github.com/InigoNavarro/daicgrupo4.git y en code dandole a download zip.

Otra manera es utilizar el comando git clone para clonar el repositorio: git clone https://github.com/InigoNavarro/daicgrupo4

## Puesta en marcha del programa 
Para que los datos se suban a la base de datos de influxDB será necesario instalarlo. Para ello será necesario seguir los siguientes pasos desde el cmd:
1. wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
2. source /etc/os-release
3. echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
4. sudo apt update && sudo apt install -y influxdb
5. sudo systemctl unmask influxdb.service
6. sudo systemctl start influxdb
7. sudo systemctl enable influxdb.service
8. influx
9. create database daicgrupo4
10. use daicgrupo4
11. create user grupo4 with password 'Grupo4_' with all privileges
12. grant all privileges on daicgrupo4 to grupo4
13. exit

Instalación de grafana
1. wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
2. echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
3. sudo apt update && sudo apt install -y grafana
4. sudo systemctl unmask grafana-server.service
5. sudo systemctl start grafana-server
6. sudo systemctl enable grafana-server.service

Visualizacion de la Base de Datos
1. Acceder al link: 

Una vez tengamos los pasos anteriores realizado podremos ejecutar el program. 

Para ejecutar el programa y valido sea False (no lleva mascarilla) -->  python Grupo4.py False 

Para ejecutar el programa y valido sea True (lleva mascarilla)-->  python Grupo4.py True --

## Equipo

| **Unai** | **Iñigo** |
| :---: |:---:|
<a href="http://github.com/unai1999" target="_blank">`github.com/unai1999`</a> | <a href="https://github.com/InigoNavarro" target="_blank">`github.com/InigoNavarro`</a> 
