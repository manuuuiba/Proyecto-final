"""
Módulo de gestión de autenticación de usuarios.
Maneja el hash de contraseñas y validación de credenciales.
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Genera un hash seguro de la contraseña usando bcrypt.
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Hash de la contraseña como string
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.
    
    Args:
        password: Contraseña en texto plano a verificar
        hashed_password: Hash almacenado de la contraseña
        
    Returns:
        True si la contraseña es correcta, False en caso contrario
    """
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
