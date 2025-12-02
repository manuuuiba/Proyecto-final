"""
Script de inicialización de la base de datos.
Crea las tablas y opcionalmente usuarios de prueba.
"""
from database import Database


def init_database():
    """Inicializa la base de datos creando las tablas necesarias."""
    print("Inicializando base de datos...")
    
    db = Database()
    print("✓ Base de datos creada exitosamente")
    print("✓ Tablas creadas: users, messages")
    
    # Preguntar si se desean crear usuarios de prueba
    crear_usuarios = input("\n¿Deseas crear usuarios de prueba? (s/n): ").lower()
    
    if crear_usuarios == 's':
        # Crear usuarios de prueba
        usuarios_prueba = [
            ("admin", "admin123"),
            ("usuario1", "password1"),
            ("usuario2", "password2")
        ]
        
        print("\nCreando usuarios de prueba...")
        for username, password in usuarios_prueba:
            success, message = db.create_user(username, password)
            if success:
                print(f"✓ Usuario '{username}' creado (contraseña: {password})")
            else:
                print(f"✗ Error con usuario '{username}': {message}")
    
    print("\n¡Inicialización completada!")
    print("Puedes ejecutar la aplicación con: python main.py")


if __name__ == "__main__":
    init_database()
