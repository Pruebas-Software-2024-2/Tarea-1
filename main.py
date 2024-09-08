import auth
import task_manager
import logging

logging.basicConfig(
    filename='task_manager.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

def main():
    print("Bienvenido a la aplicación de gestión de tareas")
    
    while True:
        action = input("¿Deseas (r)egistrar, (i)niciar sesión, o (s)alir?: ").lower()
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
                task_management_menu()
            else:
                print("Nombre de usuario o contraseña incorrectos.")
        
        elif action == 's':
            print("Adiós!")
            logging.info(f"Se ha cerrado sesión.")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

def task_management_menu():
    while True:
        print("\n--- Gestión de Tareas ---")
        print("(1) Crear tarea")
        print("(2) Listar tareas")
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
            task_manager.create_task(title, description, due_date, label)
        
        elif choice == '2':
            task_manager.list_tasks()
        
        elif choice == '3':
            # Se permite ingresar múltiples filtros opcionales
            filter_dict = {}
            fecha = input("Ingrese la fecha (DD-MM-YYYY) o deje en blanco para omitir: ")
            if fecha:
                filter_dict['fecha'] = fecha
            etiqueta = input("Ingrese la etiqueta o deje en blanco para omitir: ")
            if etiqueta:
                filter_dict['etiqueta'] = etiqueta
            estado = input("Ingrese el estado (Pendiente, En progreso, Completada) o deje en blanco para omitir: ")
            if estado:
                filter_dict['estado'] = estado

            if filter_dict:
                task_manager.search_tasks(filter_dict)  # Se realiza la búsqueda con filtros
            else:
                task_manager.list_tasks()
        
        elif choice == '4':
            title = input("Título de la tarea a actualizar: ")
            new_status = input("Nuevo estado (Pendiente, En progreso, Completada): ")
            task_manager.update_task_status(title, new_status)
        
        elif choice == '5':
            title = input("Título de la tarea a eliminar: ")
            task_manager.delete_task(title)
        
        elif choice == '6':
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()
