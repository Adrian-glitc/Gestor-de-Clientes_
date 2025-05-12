import unittest
from database import database as db
import sqlite3
import os
from config import DATABASE_PATH

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crear base de datos de prueba
        cls.test_db = 'gestor/tests/clientes_test.db'
        conn = sqlite3.connect(cls.test_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                telefono TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        
        # Configurar para usar la base de datos de prueba
        db.DATABASE_PATH = cls.test_db
    
    def setUp(self):
        # Limpiar y preparar la base de datos antes de cada test
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes")
        cursor.execute("INSERT INTO clientes (nombre, apellido, telefono) VALUES ('Juan', 'Perez', '123456789')")
        cursor.execute("INSERT INTO clientes (nombre, apellido, telefono) VALUES ('Maria', 'Gomez', '987654321')")
        conn.commit()
        conn.close()
        
        # Recargar datos
        db.Clientes.cargar_desde_db()
    
    def test_buscar_cliente(self):
        cliente = db.Clientes.buscar(1)
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente.nombre, "Juan")
        
        cliente_no_existente = db.Clientes.buscar(999)
        self.assertIsNone(cliente_no_existente)
    
    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear("Ana", "Lopez", "555555555")
        self.assertEqual(nuevo_cliente.nombre, "Ana")
        self.assertEqual(len(db.Clientes.lista), 3)
        
        # Verificar que se guardó en la base de datos
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id = ?", (nuevo_cliente.id,))
        fila = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(fila)
        self.assertEqual(fila[1], "Ana")
    
    def test_modificar_cliente(self):
        cliente_modificado = db.Clientes.modificar(1, "Juan Carlos", "Perez", "111111111")
        self.assertEqual(cliente_modificado.nombre, "Juan Carlos")
        
        # Verificar en la base de datos
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id = 1")
        fila = cursor.fetchone()
        conn.close()
        
        self.assertEqual(fila[1], "Juan Carlos")
    
    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar(1)
        self.assertEqual(cliente_borrado.nombre, "Juan")
        self.assertEqual(len(db.Clientes.lista), 1)
        
        # Verificar que se borró de la base de datos
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id = 1")
        fila = cursor.fetchone()
        conn.close()
        
        self.assertIsNone(fila)

if __name__ == '__main__':
    unittest.main()