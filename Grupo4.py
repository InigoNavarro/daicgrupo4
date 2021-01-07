import RPi.GPIO as GPIO
import time
import datetime
import psutil
import sys
from influxdb import InfluxDBClient

#Para ejecutar el programa y valido sea False (no lleva mascarilla)--> sudo python Grupo4.py False 
#Para ejecutar el programa y valido sea True (lleva mascarilla)--> sudo python Grupo4.py True


def leds(valido):
    LedRoja = 5
    LedAzul = 22
    GPIO.setup(LedAzul, GPIO.OUT)
    GPIO.setup(LedRoja, GPIO.OUT)
    print(valido)
    if valido == "True":
        GPIO.output(LedAzul, False)
        GPIO.output(LedRoja, False)
    else:
        print("a")
        GPIO.output(LedAzul, True)
        GPIO.output(LedRoja, True)
    print("b")
   
def buzzer(valido):
    Buzzer = 18
    GPIO.setup(Buzzer, GPIO.OUT)
    if valido == "True":
        GPIO.output(Buzzer, False)
    else:
        GPIO.output(Buzzer, True)

def servos(valido): #Al ser un servo no puede dar más de una vuelta.
    Servo1 = 24
    Servo2 = 26
    GPIO.setup(Servo1, GPIO.OUT)
    GPIO.setup(Servo2, GPIO.OUT)
    p = GPIO.PWM(Servo1,50)
    p2 = GPIO.PWM(Servo2,50)
    p.start(2.5)
    p2.start(2.5)
    if valido == "False":        
        p.ChangeDutyCycle(22)
        p2.ChangeDutyCycle(22)
        time.sleep(1)
        p.ChangeDutyCycle(2.5)
        p2.ChangeDutyCycle(2.5)
        time.sleep(1)

# para saber cuando hay alguien con mascarilla --> SELECT max("Mascarilla puesta") FROM "autogen"."system" WHERE $timeFilter GROUP BY time($__interval) fill(null)
def SubirBaseM(mascarilla):
    ifuser = "grupo4"
    ifpass = "Grupo4_"
    ifdb   = "daicgrupo4"
    ifhost = "127.0.0.1"
    ifport = 8086
    measurement_name = "system"

    time = datetime.datetime.utcnow()

    # indicar el cuerpo de la base de datos. Importante el campo que se sube
    body = [
        {
            "measurement": measurement_name,
            "time": time,
            "fields": {
                "Mascarilla puesta": mascarilla,
            }
        }
    ]

    # conectar a la base de datos de influx
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

    # escribir en la base de datos de influx
    ifclient.write_points(body)
    
# para saber cuantos no llevaban mascarilla durante una 1 en grafana poner en el panel --> SELECT count("Mascarilla no puesta") FROM "autogen"."system" WHERE $timeFilter GROUP BY time(1h) fill(null)
# para saber cuando hay alguien sin mascarilla --> SELECT max("Mascarilla no puesta") FROM "autogen"."system" WHERE $timeFilter GROUP BY time($__interval) fill(null)
def SubirBaseNM(noMascarilla):
    ifuser = "grupo4"
    ifpass = "Grupo4_"
    ifdb   = "daicgrupo4"
    ifhost = "127.0.0.1"
    ifport = 8086
    measurement_name = "system"

    time = datetime.datetime.utcnow()

    # indicar el cuerpo de la base de datos. Importante el campo que se sube
    body = [
        {
            "measurement": measurement_name,
            "time": time,
            "fields": {
                "Mascarilla no puesta": noMascarilla,
            }
        }
    ]

    # conectar a la base de datos de influx
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

    # escribir en la base de datos de influx
    ifclient.write_points(body)
    
def sistemaEncendido(valido,mascarilla,noMascarilla):
    leds(valido)
    buzzer(valido)
    servos(valido)
    #subir un 1 al campo noMascarilla para contar que lleva no mascarilla puesta
    if(not valido):
        SubirBaseNM(noMascarilla)
    #subir un 1 al campo mascarilla para contar que lleva mascarilla puesta
    else:
        SubirBaseM(mascarilla)
    time.sleep(1)
    sys.exit()
    
def main():
    GPIO.setmode(GPIO.BCM)
    #Definicion de variables
    detectar = True
    #activar = False
    valido = sys.argv[1]
    distancia = 0
    USS1 = 16
    USS2 = 17
    noMascarilla = 1;
    mascarilla = 1;
    
    #Poner los GPIOs ready
    GPIO.setup(USS1, GPIO.OUT)
    GPIO.setup(USS2, GPIO.IN)
    
    #detectar la la distnacia para que el sistema se encienda o no
    while detectar:
        GPIO.output(USS1, True)
        time.sleep(0.00001)
        GPIO.output(USS1, False)
        
        StartTime = time.time()
        StopTime = time.time()
             
        # guardar tiempo de salida del sonido
        while GPIO.input(USS2) == 0:
            
            StartTime = time.time()
             
        # guardar el tiempo de llegada del sonido
        while GPIO.input(USS2) == 1:
            StopTime = time.time()
         
            # diferencia entre el tiempo de salida y tiempo de llegada
        TimeElapsed = StopTime - StartTime

        distance = (TimeElapsed * 34300) / 2
        print(distance)
        #si esta cerca el individuo activar el sistema
        if(distance < 200):
            sistemaEncendido(valido,mascarilla,noMascarilla)
        detectar = False

if __name__ == "__main__":
    main()