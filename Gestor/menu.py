import helpers
import database as db

def iniciar():
    db.Clientes.inicializar_db()
    db.Clientes.cargar_desde_db()
    
    while True:
        helpers.limpiar_pantalla()
        
        print("====================")
        print(" GESTOR DE CLIENTES ")
        print("====================")
        print("[1] Listar clientes")
        print("[2] Buscar cliente")
        print("[3] Añadir cliente")
        print("[4] Modificar cliente")
        print("[5] Borrar cliente")
        print("[6] Salir")
        print("====================")
        
        opcion = input("> ")
        helpers.limpiar_pantalla()
        
        if opcion == '1':
            print("Listando clientes...\n")
            for cliente in db.Clientes.lista:
                print(cliente)
        
        elif opcion == '2':
            print("Buscando cliente...\n")
            id_str = helpers.leer_texto(1, 10, "ID del cliente:")
            try:
                id_cliente = int(id_str)
                cliente = db.Clientes.buscar(id_cliente)
                print(cliente) if cliente else print("Cliente no encontrado.")
            except ValueError:
                print("ID debe ser un número.")
        
        elif opcion == '3':
            print("Añadiendo cliente...\n")
            nombre = helpers.leer_texto(2, 30, "Nombre:").capitalize()
            apellido = helpers.leer_texto(2, 30, "Apellido:").capitalize()
            telefono = helpers.leer_texto(9, 15, "Teléfono:")
            
            if not helpers.validar_telefono(telefono):
                print("Teléfono no válido. Debe tener entre 9 y 15 dígitos.")
            else:
                db.Clientes.crear(nombre, apellido, telefono)
                print("Cliente añadido correctamente.")
        
        elif opcion == '4':
            print("Modificando cliente...\n")
            id_str = helpers.leer_texto(1, 10, "ID del cliente a modificar:")
            try:
                id_cliente = int(id_str)
                cliente = db.Clientes.buscar(id_cliente)
                if cliente:
                    nombre = helpers.leer_texto(2, 30, f"Nuevo nombre [{cliente.nombre}]:").capitalize() or cliente.nombre
                    apellido = helpers.leer_texto(2, 30, f"Nuevo apellido [{cliente.apellido}]:").capitalize() or cliente.apellido
                    telefono = helpers.leer_texto(9, 15, f"Nuevo teléfono [{cliente.telefono}]:") or cliente.telefono
                    
                    if not helpers.validar_telefono(telefono):
                        print("Teléfono no válido. Debe tener entre 9 y 15 dígitos.")
                    else:
                        db.Clientes.modificar(id_cliente, nombre, apellido, telefono)
                        print("Cliente modificado correctamente.")
                else:
                    print("Cliente no encontrado.")
            except ValueError:
                print("ID debe ser un número.")
        
        elif opcion == '5':
            print("Borrando cliente...\n")
            id_str = helpers.leer_texto(1, 10, "ID del cliente a borrar:")
            try:
                id_cliente = int(id_str)
                cliente = db.Clientes.borrar(id_cliente)
                print(f"Cliente {cliente.nombre} {cliente.apellido} borrado.") if cliente else print("Cliente no encontrado.")
            except ValueError:
                print("ID debe ser un número.")
        
        elif opcion == '6':
            print("Saliendo...")
            break
        
        input("\nPresiona ENTER para continuar...")