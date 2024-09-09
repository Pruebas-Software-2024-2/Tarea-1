import auth
import task_manager
import logging

logging.basicConfig(
    filename='task_manager.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)

def main():
    print("Bienvenido a la aplicación de gestión de tareas")
    
    while True:
        action = input("¿Deseas (r)egistrarte, (i)niciar sesión, o (s)alir?: ").lower()
        if action == 'r':
            username = input("Introduce tu nombre de usuario: ")
            password = input("Introduce tu contraseña: ")
            try:
                auth.register_user(username, password)
                logging.info(f"Nuevo usuario registrado: {username}")
            except ValueError as e:
                print(e)
                logging.error(f"Error en autenticación: {str(e)}")
        
        elif action == 'i':
            username = input("Introduce tu nombre de usuario: ")
            password = input("Introduce tu contraseña: ")
            if auth.login_user(username, password):
                print(f"Bienvenido {username}!")
                logging.info(f"Usuario '{username}' ha iniciado sesión.")
                task_management_menu(username)  # Pasar el nombre del usuario a las funciones
            else:
                print("Nombre de usuario o contraseña incorrectos.")
        
        elif action == 's':
            print("Adiós!")
            logging.info(f"Se ha cerrado sesión.")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

def task_management_menu(username):
    while True:
        print("\n--- Gestión de Tareas ---")
        print(f"(1) Crear tarea para {username}")
        print(f"(2) Listar tareas de {username}")
        print("(3) Buscar tarea")
        print("(4) Actualizar tarea")
        print("(5) Eliminar tarea")
        print("(6) Salir")

        choice = input("Selecciona una opción: ")
        
        if choice == '1':
            title = input("Título: ")
            description = input("Descripción: ")
            due_date = input("Fecha de vencimiento (DD-MM-YYYY): ")
            label = input("Etiqueta (por ejemplo, Urgente, Trabajo, Personal): ")
            task_manager.create_task(username, title, description, due_date, label)
        
        elif choice == '2':
            task_manager.list_tasks(username)
        
        elif choice == '3':
            filter_dict = {}
            titulo = input("Ingrese el titulo o deje en blanco para omitir: ")
            if titulo:
                filter_dict['titulo'] = titulo
            fecha = input("Ingrese la fecha (DD-MM-YYYY) o deje en blanco para omitir: ")
            if fecha:
                filter_dict['fecha'] = fecha
            etiqueta = input("Ingrese la etiqueta o deje en blanco para omitir: ")
            if etiqueta:
                filter_dict['etiqueta'] = etiqueta
            estado = input("Ingrese el estado (Pendiente, En progreso, Completada) o deje en blanco para omitir: ")
            if estado:
                filter_dict['estado'] = estado

            task_manager.search_tasks(username, filter_dict)
        
        elif choice == '4':
            title = input("Título de la tarea a actualizar: ")
            new_status = input("Nuevo estado (Pendiente, En progreso, Completada): ")
            task_manager.update_task_status(username, title, new_status)
        
        elif choice == '5':
            title = input("Título de la tarea a eliminar: ")
            task_manager.delete_task(username, title)
        
        elif choice == '6':
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()
