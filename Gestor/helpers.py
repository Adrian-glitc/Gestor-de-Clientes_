import os
import platform
import re

def limpiar_pantalla():
    os.system('cls') if platform.system() == "Windows" else os.system('clear')

def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto

def validar_telefono(telefono):
    return re.match(r'^[0-9]{9,15}$', telefono) is not None