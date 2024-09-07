import json
import os
import logging

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
    task = {
        'title': title,
        'description': description,
        'due_date': due_date,
        'label': label,
        'status': 'pendiente'  # Estado inicial de la tarea
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
        print(f"Título: {task['title']}, Estado: {task['status']}")

# Función para actualizar el estado de una tarea
def update_task_status(title, new_status):
    tasks = load_tasks()
    for task in tasks:
        if task['title'] == title:
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
