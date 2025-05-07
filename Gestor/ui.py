import tkinter as tk
from tkinter import ttk, messagebox
import database as db

class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws/2) - (w/2))
        y = int((hs/2) - (h/2))
        self.geometry(f"{w}x{h}+{x}+{y}")

class MainWindow(tk.Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Clientes")
        self.build()
        self.center()
        db.Clientes.inicializar_db()
        db.Clientes.cargar_desde_db()
    
    def build(self):
        # Crear pestañas
        self.pestanas = ttk.Notebook(self)
        self.pestanas.pack(fill='both', expand=True)
        
        # Crear frames para pestañas
        self.pestana_formulario = ttk.Frame(self.pestanas)
        self.pestana_busqueda = ttk.Frame(self.pestanas)
        
        # Añadir pestañas
        self.pestanas.add(self.pestana_formulario, text="Formulario")
        self.pestanas.add(self.pestana_busqueda, text="Buscar")
        
        # Construir contenido de las pestañas
        self._build_formulario()
        self._build_busqueda()
    
    def _build_formulario(self):
        # Etiquetas y campos
        ttk.Label(self.pestana_formulario, text="Nombre:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_nombre = ttk.Entry(self.pestana_formulario)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(self.pestana_formulario, text="Apellido:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_apellido = ttk.Entry(self.pestana_formulario)
        self.entry_apellido.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(self.pestana_formulario, text="Teléfono:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_telefono = ttk.Entry(self.pestana_formulario)
        self.entry_telefono.grid(row=2, column=1, padx=10, pady=10)
        
        # Botón guardar
        ttk.Button(self.pestana_formulario, text="Guardar", command=self._guardar_cliente).grid(row=3, column=0, columnspan=2, pady=20)
    
    def _build_busqueda(self):
        # Campo de búsqueda
        ttk.Label(self.pestana_busqueda, text="Buscar:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_busqueda = ttk.Entry(self.pestana_busqueda)
        self.entry_busqueda.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Button(self.pestana_busqueda, text="Buscar", command=self._buscar_clientes).grid(row=0, column=2, padx=10, pady=10)
        
        # Tabla de resultados
        self.tree = ttk.Treeview(self.pestana_busqueda, columns=("ID", "Nombre", "Apellido", "Teléfono"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.pestana_busqueda, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Botones de acción
        ttk.Button(self.pestana_busqueda, text="Eliminar", command=self._eliminar_cliente).grid(row=2, column=0, pady=10)
        ttk.Button(self.pestana_busqueda, text="Actualizar", command=self._actualizar_cliente).grid(row=2, column=1, pady=10)
        
        # Cargar datos iniciales
        self._cargar_clientes()
    
    def _guardar_cliente(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        telefono = self.entry_telefono.get()
        
        if nombre and apellido and telefono:
            db.Clientes.crear(nombre, apellido, telefono)
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            
            # Limpiar campos
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)
            
            # Actualizar lista
            self._cargar_clientes()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
    
    def _cargar_clientes(self, filtro=""):
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Cargar clientes desde la base de datos
        db.Clientes.cargar_desde_db()
        
        # Filtrar si es necesario
        clientes_filtrados = db.Clientes.lista
        if filtro:
            clientes_filtrados = [
                c for c in db.Clientes.lista 
                if filtro.lower() in c.nombre.lower() or 
                   filtro.lower() in c.apellido.lower()
            ]
        
        # Insertar en la tabla
        for cliente in clientes_filtrados:
            self.tree.insert("", tk.END, values=(cliente.id, cliente.nombre, cliente.apellido, cliente.telefono))
    
    def _buscar_clientes(self):
        filtro = self.entry_busqueda.get()
        self._cargar_clientes(filtro)
    
    def _eliminar_cliente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Selecciona un cliente para eliminar")
            return
        
        cliente = self.tree.item(seleccionado)["values"]
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar a {cliente[1]} {cliente[2]}?")
        
        if confirmar:
            db.Clientes.borrar(cliente[0])
            self._cargar_clientes()
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
    
    def _actualizar_cliente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Selecciona un cliente para actualizar")
            return
        
        cliente = self.tree.item(seleccionado)["values"]
        
        # Crear ventana de edición
        ventana_edicion = tk.Toplevel(self)
        ventana_edicion.title("Editar Cliente")
        
        # Campos de edición
        ttk.Label(ventana_edicion, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
        entry_nombre = ttk.Entry(ventana_edicion)
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)
        entry_nombre.insert(0, cliente[1])
        
        ttk.Label(ventana_edicion, text="Apellido:").grid(row=1, column=0, padx=10, pady=5)
        entry_apellido = ttk.Entry(ventana_edicion)
        entry_apellido.grid(row=1, column=1, padx=10, pady=5)
        entry_apellido.insert(0, cliente[2])
        
        ttk.Label(ventana_edicion, text="Teléfono:").grid(row=2, column=0, padx=10, pady=5)
        entry_telefono = ttk.Entry(ventana_edicion)
        entry_telefono.grid(row=2, column=1, padx=10, pady=5)
        entry_telefono.insert(0, cliente[3])
        
        # Botón guardar
        def guardar_cambios():
            nuevo_nombre = entry_nombre.get()
            nuevo_apellido = entry_apellido.get()
            nuevo_telefono = entry_telefono.get()
            
            if nuevo_nombre and nuevo_apellido and nuevo_telefono:
                db.Clientes.modificar(cliente[0], nuevo_nombre, nuevo_apellido, nuevo_telefono)
                self._cargar_clientes()
                ventana_edicion.destroy()
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
        
        ttk.Button(ventana_edicion, text="Guardar", command=guardar_cambios).grid(row=3, column=0, columnspan=2, pady=10)