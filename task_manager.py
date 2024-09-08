import json
import os
import logging
from datetime import datetime

TASKS_FILE = 'tasks.json'

# Función para cargar tareas desde el archivo
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

# Función para guardar tareas en el archivo
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Función para crear una nueva tarea
def create_task(title, description, due_date, label):
    tasks = load_tasks()
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
        status = "Pendiente"  # Estado inicial: pendiente

    task = {
        'title': title,
        'description': description,
        'due_date': due_date,
        'label': label,
        'status': status # Estado inicial de la tarea
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Tarea '{title}' creada correctamente.")
    logging.info(f"Tarea creada: {title}")

# Función para mostrar todas las tareas
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No hay tareas registradas.")
        logging.info("Listado de tareas consultado (sin tareas).")
        return
    else:
        logging.info("Listado de tareas consultado.")
    
    for task in tasks:
        print(f"Título: {task['title']}, Estado: {task['status']}, Fecha de vencimiento: {task['due_date']}, Etiqueta: {task['label']}")

# Función para actualizar el estado de una tarea
def update_task_status(title, new_status):
    tasks = load_tasks()
    for task in tasks:
        if task['title'] == title:
            if new_status == "Completada":
                print(f"Tarea '{task['title']}' completada")
                delete = input("Desea eliminarla?\n(1) Si\n(2)No\n")
                if delete == "1":
                    delete_task(title)
                return 
            task['status'] = new_status
            save_tasks(tasks)
            logging.info(f"Estado de la tarea '{title}' actualizado a '{new_status}'.")
            print(f"Estado de la tarea '{title}' actualizado a {new_status}.")
            return
    print(f"No se encontró la tarea con el título '{title}'.")

# Función para eliminar una tarea
def delete_task(title):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['title'] != title]
    save_tasks(tasks)
    print(f"Tarea '{title}' eliminada correctamente.")
    logging.info(f"Tarea eliminada: {title}")

# Función para buscar tareas por etiqueta, fecha de vencimiento o estado
def search_tasks(filter_type, filter_value):
    tasks = load_tasks()
    filtered_tasks = []

    if filter_type == "fecha":
        try:
            filter_date = datetime.strptime(filter_value, "%d-%m-%Y")
        except ValueError:
            print("Formato de fecha incorrecto. Use DD-MM-YYYY.")
            logging.error("Error en el formato de la fecha de búsqueda.")
            return
        
        filtered_tasks = [task for task in tasks if datetime.strptime(task['due_date'], "%d-%m-%Y") == filter_date]

    elif filter_type == "etiqueta":
        filtered_tasks = [task for task in tasks if task['label'].lower() == filter_value.lower()]

    elif filter_type == "estado":
        filtered_tasks = [task for task in tasks if task['status'].lower() == filter_value.lower()]

    if not filtered_tasks:
        print(f"No se encontraron tareas para el filtro: {filter_type} = {filter_value}")
        logging.info(f"No se encontraron tareas para el filtro: {filter_type} = {filter_value}")
        return

    logging.info(f"Filtro aplicado: {filter_type} = {filter_value}")
    for task in filtered_tasks:
        print(f"Título: {task['title']}, Estado: {task['status']}, Fecha de vencimiento: {task['due_date']}, Etiqueta: {task['label']}")
