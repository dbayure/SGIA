from ctypes import *
import sys
import random
import math
import time
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit

ipWS= '192.168.1.21'
puertoWS= 5001
puertoTemp= 2
puertoLuz= 5
puertoVent= 0
dispLuz= 3
rele=InterfaceKit()
placa= InterfaceKit()
nroSerieRele= 134980
nroSeriePlaca= 339648 

def instanciarIK (nroSerie):
    ik= InterfaceKit()
    ik.openRemoteIP(ipWS, puertoWS, nroSerie)
    return ik

def mostrarInfoIK (ik):
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (ik.isAttached(), ik.getDeviceName(), ik.getSerialNum(), ik.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Numero de entradas digitales: %i" % (ik.getInputCount()))
    print("Numero de salidas digitales: %i" % (ik.getOutputCount()))
    print("Numero de entradas analogicas: %i" % (ik.getSensorCount()))

def conversionTemperatura(lectura):
    convertido= (lectura * 0.2222) - 61.111
    return convertido

def encenderVentilador(ik):
    if ik.getOutputState(puertoVent) == 0:
        ik.setOutputState(puertoVent, 1) 
    
def encenderLuz(ik):
    if ik.getOutputState(dispLuz) == 1:
        ik.setOutputState(dispLuz, 0)
    
def apagarVentilador(ik):
    if ik.getOutputState(puertoVent) == 1:
        ik.setOutputState(puertoVent, 0)
        
def apagarLuz(ik):
    if ik.getOutputState(dispLuz) == 0:
        ik.setOutputState(dispLuz, 1)    
        
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
   
print("""Comandos...
         1. Obtener lectura de temperatura
         2. Encender ventilador
         3. Encender luz
         4. Apagar ventilador
         5. Apagar luz
         6. Salir
         
Ingrese nro de comando...""")

chr = '\n'
while chr != '6':
    if chr == '1':
        temp= obtenerTemperatura(placa)
        print('Temperatura actual: ' +str(temp))
    elif chr == '2':
        encenderVentilador(rele)
    elif chr == '3':
        encenderLuz(placa)
    elif chr == '4':
        apagarVentilador(rele)
    elif chr == '5':
        apagarLuz(placa)
    elif chr == '6':
        print('Saliendo del sistema....')
    else:
        if chr != '\n':
            print ('Comando no valido.')
            print("Ingrese nro de comando...")
    chr = sys.stdin.read(1)
    
try:
    rele.closePhidget()
    placa.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....4")
    exit(1)

print("Done.")
exit(0)
