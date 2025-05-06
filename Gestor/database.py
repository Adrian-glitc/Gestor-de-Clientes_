import sqlite3
import csv
from config import DATABASE_PATH

class Cliente:
    def __init__(self, id, nombre, apellido, telefono):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
    
    def __str__(self):
        return f"{self.id}: {self.nombre} {self.apellido} - {self.telefono}"

class Clientes:
    # Lista de clientes
    lista = []
    
    @staticmethod
    def cargar_desde_db():
        Clientes.lista = []
        conexion = sqlite3.connect(DATABASE_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes")
        
        for fila in cursor.fetchall():
            cliente = Cliente(fila[0], fila[1], fila[2], fila[3])
            Clientes.lista.append(cliente)
        
        conexion.close()
    
    @staticmethod
    def buscar(id):
        for cliente in Clientes.lista:
            if cliente.id == id:
                return cliente
        return None
    
    @staticmethod
    def crear(nombre, apellido, telefono):
        conexion = sqlite3.connect(DATABASE_PATH)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO clientes (nombre, apellido, telefono) VALUES (?, ?, ?)",
                      (nombre, apellido, telefono))
        id_cliente = cursor.lastrowid
        conexion.commit()
        conexion.close()
        
        cliente = Cliente(id_cliente, nombre, apellido, telefono)
        Clientes.lista.append(cliente)
        return cliente
    
    @staticmethod
    def modificar(id, nombre, apellido, telefono):
        conexion = sqlite3.connect(DATABASE_PATH)
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE clientes 
            SET nombre = ?, apellido = ?, telefono = ?
            WHERE id = ?
        """, (nombre, apellido, telefono, id))
        conexion.commit()
        conexion.close()
        
        for cliente in Clientes.lista:
            if cliente.id == id:
                cliente.nombre = nombre
                cliente.apellido = apellido
                cliente.telefono = telefono
                return cliente
        return None
    
    @staticmethod
    def borrar(id):
        conexion = sqlite3.connect(DATABASE_PATH)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
        conexion.commit()
        conexion.close()
        
        for i, cliente in enumerate(Clientes.lista):
            if cliente.id == id:
                return Clientes.lista.pop(i)
        return None
    
    @staticmethod
    def inicializar_db():
        conexion = sqlite3.connect(DATABASE_PATH)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                telefono TEXT NOT NULL
            )
        ''')
        conexion.commit()
        conexion.close()