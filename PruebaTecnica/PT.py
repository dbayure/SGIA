#Basic imports
from ctypes import *
import sys
import random
import math
import time
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit

ipWS= '192.168.1.21'
puertoWS= 5001
puertoTemp= 2
puertoLuz= 5
puertoVent= 0
umbralTemp= 15
umbralLuz= 100
dispLuz= 3
rele=InterfaceKit()
placa= InterfaceKit()
nroSerieRele= 134980
nroSeriePlaca= 339648 
estadoVent= 0
variable= 1


def instanciarIK (nroSerie):
    ik= InterfaceKit()
    ik.setOnSensorChangeHandler(manejadorSensores)
    ik.openRemoteIP(ipWS, puertoWS, nroSerie)
    return ik

def mostrarInfoIK (ik):
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (ik.isAttached(), ik.getDeviceName(), ik.getSerialNum(), ik.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Digital Inputs: %i" % (ik.getInputCount()))
    print("Number of Digital Outputs: %i" % (ik.getOutputCount()))
    print("Number of Sensor Inputs: %i" % (ik.getSensorCount()))


def conversionTemperatura(lectura):
    convertido= (lectura * 0.2222) - 61.111
    return convertido

def conversionLuminancia(lectura):
    exponente= 0.02385 + lectura -0.56905
    convertido= math.exp(0.02385 + lectura -0.56905)
    return convertido

def encenderVentilador(ik):
    if ik.getOutputState(puertoVent) == 0:
        ik.setOutputState(puertoVent, 1) 
    
def encenderLuz(ik):
    if ik.getOutputState(dispLuz) == 0:
        ik.setOutputState(dispLuz, 1)
    
def apagarVentilador(ik):
    if ik.getOutputState(puertoVent) == 1:
        ik.setOutputState(puertoVent, 0)
        
def cambiarEstadoVentilador(i):
    variable= i

def apagarLuz(ik):
    if ik.getOutputState(dispLuz) == 1:
        ik.setOutputState(dispLuz, 0)    

def manejadorSensores(e):
    if e.index == puertoTemp:
        valor= conversionTemperatura(e.value)
        print ("Valor en C: " + str(valor))
        #if valor >= umbralTemp:
         #   encenderVentilador(rele)
        #else:
           # estadoVent= 0
    elif e.index == puertoLuz:
        valor= e.value
        #valor= conversionLuminancia(e.value)
        print('Valor en LUX: %i' %(valor,))
        if valor >= umbralLuz:
            encenderLuz(placa)
        else:
            apagarLuz(placa)
    else:
        print("Cambio en sensor:%i: Valor %i:" % (e.index, e.value))


def setPropiedadesIK (ik):
    ik.setOnSensorChangeHandler(manejadorSensores)
    
def obtenerTemperatura(ik):
    valor=ik.getSensorValue(puertoTemp)
    print ('Valor bruto: '+ str(valor))
    temp= conversionTemperatura(valor)
    return temp

placa = instanciarIK (nroSeriePlaca)
rele= instanciarIK(nroSerieRele)
placa.waitForAttach(10000)
rele.waitForAttach(10000)
mostrarInfoIK(placa)
mostrarInfoIK(rele)

while (1==1):
    temperatura= obtenerTemperatura(placa)
    print('Temperatura: '+str(temperatura))
    if temperatura >= umbralTemp:
        encenderVentilador(rele)
    else:
        apagarVentilador(rele)
    time.sleep(5)
    

#encenderVentilador(rele)
apagarVentilador(rele)

print("Ingrese nro de rele o s para salir....")
chr = sys.stdin.read(1)
while chr != 's':
    print("Ingrese nro de rele o s para salir....")
    chr = sys.stdin.read(1)


print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    rele.closePhidget()
    placa.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....4")
    exit(1)

print("Done.")
exit(0)