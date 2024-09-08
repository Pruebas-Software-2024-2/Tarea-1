import bcrypt
import os
import json

# Archivo donde se almacenarán los usuarios registrados (puede ser un sistema de base de datos en proyectos más grandes)
USERS_FILE = 'users.json'

# Función para cargar los usuarios desde el archivo
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Función para guardar los usuarios en el archivo
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Función para registrar un nuevo usuario
def register_user(username, password):
    users = load_users()
    
    if username in users:
        raise ValueError("El usuario ya está registrado")
    
    # Hash de la contraseña
    hashed_password = hash_password(password)
    
    # Almacenar el nuevo usuario
    users[username] = hashed_password
    save_users(users)
    
    print(f"Usuario {username} registrado correctamente.")

# Función para iniciar sesión (verificar credenciales)
def login_user(username, password):
    users = load_users()
    
    if username not in users:
        return False
    
    # Verificar contraseña
    stored_hash = users[username]
    if verify_password(stored_hash, password):
        print("Inicio de sesión exitoso.")
        return True
    else:
        print("Contraseña incorrecta.")
        return False

# Función para hacer hash de la contraseña
def hash_password(password):
    salt = bcrypt.gensalt()  # Genera un salt aleatorio
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# Función para verificar una contraseña comparando con el hash almacenado
def verify_password(stored_hash, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))
