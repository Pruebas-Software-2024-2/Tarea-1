import json
import os
import logging
from datetime import datetime

TASKS_FILE = 'tasks.json'

# Función para cargar tareas desde el archivo para un usuario específico
def load_tasks(username):
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    return tasks.get(username, [])

# Función para guardar tareas de un usuario específico en el archivo
def save_tasks(username, tasks):
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            all_tasks = json.load(f)
    else:
        all_tasks = {}

    all_tasks[username] = tasks
    with open(TASKS_FILE, 'w') as f:
        json.dump(all_tasks, f, indent=4)

# Función para crear una nueva tarea
def create_task(username, title, description, due_date, label):
    tasks = load_tasks(username)
    try:
        due_date_obj = datetime.strptime(due_date, "%d-%m-%Y")
    except ValueError:
        logging.error("Error en el formato de la fecha. Use DD-MM-YYYY.")
        raise ValueError("La fecha está incorrecta. Por favor ingrese una fecha válida.")
    
    current_date = datetime.now()

    # Comparar la fecha de vencimiento con la fecha actual
    if due_date_obj < current_date:
        status = "Atrasado"
    else:
        status = "Pendiente"

    task = {
        'title': title,
        'description': description,
        'due_date': due_date,
        'label': label,
        'status': status
    }
    tasks.append(task)
    save_tasks(username, tasks)
    print(f"Tarea '{title}' creada correctamente.")
    logging.info(f"Tarea creada para {username}: {title}")

# Función para mostrar todas las tareas de un usuario
def list_tasks(username):
    tasks = load_tasks(username)
    if not tasks:
        print(f"{username} no tiene tareas registradas.")
        logging.info(f"Listado de tareas consultado para {username} (sin tareas).")
        return
    logging.info(f"Listado de tareas consultado para {username}.")
    
    for task in tasks:
        print(f"Título: {task['title']}, Estado: {task['status']}, Fecha de vencimiento: {task['due_date']}, Etiqueta: {task['label']}")

# Función para buscar tareas por etiqueta, fecha de vencimiento o estado para un usuario específico
def search_tasks(username, filter_dict):
    tasks = load_tasks(username)
    filtered_tasks = tasks

    if 'titulo' in filter_dict:
        filtered_tasks = [task for task in filtered_tasks if task['title'].lower() == filter_dict['titulo'].lower()]

    if 'fecha' in filter_dict:
        try:
            filter_date = datetime.strptime(filter_dict['fecha'], "%d-%m-%Y")
            filtered_tasks = [task for task in filtered_tasks if datetime.strptime(task['due_date'], "%d-%m-%Y") == filter_date]
        except ValueError:
            print("Formato de fecha incorrecto. Use DD-MM-YYYY.")
            logging.error(f"Error en el formato de la fecha de búsqueda para {username}.")
            return

    if 'etiqueta' in filter_dict:
        filtered_tasks = [task for task in filtered_tasks if task['label'].lower() == filter_dict['etiqueta'].lower()]

    if 'estado' in filter_dict:
        filtered_tasks = [task for task in filtered_tasks if task['status'].lower() == filter_dict['estado'].lower()]

    if not filtered_tasks:
        print(f"No se encontraron tareas con los filtros aplicados para {username}.")
        logging.info(f"No se encontraron tareas con los filtros aplicados para {username}.")
        return

    logging.info(f"Filtros aplicados para {username}: " + ", ".join([f"{k} = {v}" for k, v in filter_dict.items()]))
    for task in filtered_tasks:
        print(f"Título: {task['title']}, Estado: {task['status']}, Fecha de vencimiento: {task['due_date']}, Etiqueta: {task['label']}")

# Función para actualizar el estado de una tarea de un usuario específico
def update_task_status(username, title, new_status):
    tasks = load_tasks(username)
    for task in tasks:
        if task['title'] == title:
            if new_status == "Completada":
                print(f"Tarea '{task['title']}' completada")
                delete = input("Desea eliminarla?\n(1) Si\n(2) No\n")
                if delete == "1":
                    delete_task(username, title)
                return
            task['status'] = new_status
            save_tasks(username, tasks)
            logging.info(f"Estado de la tarea '{title}' actualizado a '{new_status}' para {username}.")
            print(f"Estado de la tarea '{title}' actualizado a {new_status} para {username}.")
            return
    print(f"No se encontró la tarea con el título '{title}' para {username}.")

# Función para eliminar una tarea de un usuario
def delete_task(username, title):
    tasks = load_tasks(username)
    tasks = [task for task in tasks if task['title'] != title]
    save_tasks(username, tasks)
    print(f"Tarea '{title}' eliminada correctamente.")
    logging.info(f"Tarea '{title}' eliminada para {username}.")
