"""
Módulo de gestión de base de datos SQLite.
Maneja usuarios, mensajes y conversaciones.
"""
import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple, Dict
from auth import hash_password, verify_password


class Database:
    """Clase para gestionar la base de datos SQLite."""
    
    def __init__(self, db_path: str = "chatbot.db"):
        """
        Inicializa la conexión a la base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos
        """
        self.db_path = db_path
        self.create_tables()
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una nueva conexión a la base de datos."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_tables(self):
        """Crea las tablas necesarias si no existen."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de mensajes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla de perfiles de usuario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                avatar_id INTEGER DEFAULT 1,
                theme_preference TEXT DEFAULT 'dark',
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla de estadísticas de usuario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id INTEGER PRIMARY KEY,
                total_messages INTEGER DEFAULT 0,
                total_chats INTEGER DEFAULT 0,
                last_login TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Crea un nuevo usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano
            
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                conn.close()
                return False, "El usuario ya existe"
            
            # Hash de la contraseña
            password_hash = hash_password(password)
            
            # Insertar usuario
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
            conn.close()
            
            return True, "Usuario creado exitosamente"
        
        except Exception as e:
            return False, f"Error al crear usuario: {str(e)}"
    
    def delete_user(self, user_id: int) -> Tuple[bool, str]:
        """
        Elimina un usuario y todos sus mensajes.
        
        Args:
            user_id: ID del usuario a eliminar
            
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Verificar si el usuario existe
            cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
            if not cursor.fetchone():
                conn.close()
                return False, "El usuario no existe"
            
            # Eliminar primero todos los mensajes del usuario (por integridad referencial)
            cursor.execute('DELETE FROM messages WHERE user_id = ?', (user_id,))
            
            # Luego eliminar el usuario
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            
            conn.commit()
            conn.close()
            
            return True, "Usuario eliminado exitosamente"
        
        except Exception as e:
            return False, f"Error al eliminar usuario: {str(e)}"
    
    def get_all_users(self) -> List[Dict[str, any]]:
        """
        Obtiene la lista de todos los usuarios registrados.
        
        Returns:
            Lista de diccionarios con información de usuarios
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT id, username, created_at FROM users ORDER BY username ASC'
            )
            rows = cursor.fetchall()
            conn.close()
            
            users = [
                {
                    'id': row['id'],
                    'username': row['username'],
                    'created_at': row['created_at']
                }
                for row in rows
            ]
            
            return users
        
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
    
    def validate_user(self, username: str, password: str) -> Tuple[bool, Optional[int]]:
        """
        Valida las credenciales del usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano
            
        Returns:
            Tupla (válido, user_id o None)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT id, password_hash FROM users WHERE username = ?',
                (username,)
            )
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return False, None
            
            user_id = row['id']
            password_hash = row['password_hash']
            
            if verify_password(password, password_hash):
                return True, user_id
            
            return False, None
        
        except Exception as e:
            print(f"Error al validar usuario: {e}")
            return False, None
    
    def save_message(self, user_id: int, role: str, content: str) -> bool:
        """
        Guarda un mensaje en la base de datos.
        
        Args:
            user_id: ID del usuario
            role: Rol del mensaje ('user' o 'assistant')
            content: Contenido del mensaje
            
        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)',
                (user_id, role, content)
            )
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Error al guardar mensaje: {e}")
            return False
    
    def get_user_messages(self, user_id: int, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Obtiene los mensajes de un usuario.
        
        Args:
            user_id: ID del usuario
            limit: Límite de mensajes a recuperar (None para todos)
            
        Returns:
            Lista de diccionarios con los mensajes
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if limit:
                cursor.execute(
                    '''SELECT role, content, timestamp 
                       FROM messages 
                       WHERE user_id = ? 
                       ORDER BY timestamp DESC 
                       LIMIT ?''',
                    (user_id, limit)
                )
            else:
                cursor.execute(
                    '''SELECT role, content, timestamp 
                       FROM messages 
                       WHERE user_id = ? 
                       ORDER BY timestamp ASC''',
                    (user_id,)
                )
            
            rows = cursor.fetchall()
            conn.close()
            
            messages = [
                {
                    'role': row['role'],
                    'content': row['content'],
                    'timestamp': row['timestamp']
                }
                for row in rows
            ]
            
            # Si usamos LIMIT, los mensajes vienen en orden descendente
            if limit:
                messages.reverse()
            
            return messages
        
        except Exception as e:
            print(f"Error al obtener mensajes: {e}")
            return []
    
    def clear_user_messages(self, user_id: int) -> bool:
        """
        Elimina todos los mensajes de un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            True si se eliminaron correctamente, False en caso contrario
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM messages WHERE user_id = ?', (user_id,))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Error al eliminar mensajes: {e}")
            return False
    
    def get_username(self, user_id: int) -> Optional[str]:
        """
        Obtiene el nombre de usuario por ID.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Nombre de usuario o None si no existe
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            return row['username'] if row else None
        
        except Exception as e:
            print(f"Error al obtener nombre de usuario: {e}")
            return None
    
    # ===============================
    # Funciones para Perfiles de Usuario
    # ===============================
    
    def initialize_user_profile(self, user_id: int) -> bool:
        """Inicializa el perfil de un usuario recién creado."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('INSERT OR IGNORE INTO user_profiles (user_id) VALUES (?)', (user_id,))
            cursor.execute('INSERT OR IGNORE INTO user_stats (user_id, last_login) VALUES (?, CURRENT_TIMESTAMP)', (user_id,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al inicializar perfil: {e}")
            return False
    
    def get_user_avatar(self, user_id: int) -> int:
        """Obtiene el ID del avatar del usuario."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT avatar_id FROM user_profiles WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result['avatar_id']
            else:
                self.initialize_user_profile(user_id)
                return 1
        except sqlite3.Error:
            return 1
    
    def set_user_avatar(self, user_id: int, avatar_id: int) -> bool:
        """Establece el avatar del usuario."""
        if avatar_id < 1 or avatar_id > 10:
            return False
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE user_profiles SET avatar_id = ? WHERE user_id = ?', (avatar_id, user_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False
    
    def get_user_theme(self, user_id: int) -> str:
        """Obtiene la preferencia de tema del usuario."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT theme_preference FROM user_profiles WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            conn.close()
            return result['theme_preference'] if result else 'dark'
        except sqlite3.Error:
            return 'dark'
    
    def set_user_theme(self, user_id: int, theme: str) -> bool:
        """Establece la preferencia de tema del usuario."""
        if theme not in ['dark', 'light']:
            return False
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE user_profiles SET theme_preference = ? WHERE user_id = ?', (theme, user_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False
    
    def update_last_login(self, user_id: int) -> bool:
        """Actualiza la fecha/hora del último login."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE user_stats SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False
    
    def increment_message_count(self, user_id: int) -> bool:
        """Incrementa el contador de mensajes del usuario."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE user_stats SET total_messages = total_messages + 1 WHERE user_id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Obtiene las estadísticas del usuario."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT total_messages, total_chats, last_login FROM user_stats WHERE user_id = ?', (user_id,))
            stats_row = cursor.fetchone()
            cursor.execute('SELECT created_at FROM users WHERE id = ?', (user_id,))
            user_row = cursor.fetchone()
            conn.close()
            
            if stats_row and user_row:
                created_at = datetime.strptime(user_row['created_at'], '%Y-%m-%d %H:%M:%S')
                days_active = (datetime.now() - created_at).days + 1
                return {
                    'total_messages': stats_row['total_messages'],
                    'total_chats': stats_row['total_chats'],
                    'last_login': stats_row['last_login'],
                    'days_active': days_active,
                    'avg_messages_per_day': round(stats_row['total_messages'] / days_active, 1) if days_active > 0 else 0
                }
            else:
                self.initialize_user_profile(user_id)
                return {'total_messages': 0, 'total_chats': 0, 'last_login': None, 'days_active': 1, 'avg_messages_per_day': 0}
        except Exception:
            return {'total_messages': 0, 'total_chats': 0, 'last_login': None, 'days_active': 1, 'avg_messages_per_day': 0}
