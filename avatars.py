"""
Sistema de Avatares para Chatbot IA.
Proporciona avatares predefinidos para personalización de usuarios.
"""
import flet as ft

# Colección de avatares disponibles
AVATARS = {
    1: {
        "icon": ft.Icons.PERSON,
        "color": "#00A859",
        "name": "Profesional"
    },
    2: {
        "icon": ft.Icons.FACE,
        "color": "#A4D65E",
        "name": "Sonriente"
    },
    3: {
        "icon": ft.Icons.ACCOUNT_CIRCLE,
        "color": "#006341",
        "name": "Clásico"
    },
    4: {
        "icon": ft.Icons.EMOJI_PEOPLE,
        "color": "#52B788",
        "name": "Amigable"
    },
    5: {
        "icon": ft.Icons.SENTIMENT_SATISFIED,
        "color": "#74C69D",
        "name": "Feliz"
    },
    6: {
        "icon": ft.Icons.TAG_FACES,
        "color": "#95D5B2",
        "name": "Etiqueta"
    },
    7: {
        "icon": ft.Icons.PSYCHOLOGY,
        "color": "#B7E4C7",
        "name": "Pensador"
    },
    8: {
        "icon": ft.Icons.WORKSPACE_PREMIUM,
        "color": "#D8F3DC",
        "name": "Premium"
    },
    9: {
        "icon": ft.Icons.STAR,
        "color": "#FBBF24",
        "name": "Estrella"
    },
    10: {
        "icon": ft.Icons.FAVORITE,
        "color": "#F87171",
        "name": "Favorito"
    },
}

def get_avatar_icon(avatar_id: int) -> ft.Icons:
    """
    Obtiene el ícono del avatar.
    
    Args:
        avatar_id: ID del avatar (1-10)
        
    Returns:
        Ícono de Flet correspondiente al avatar
    """
    avatar = AVATARS.get(avatar_id, AVATARS[1])
    return avatar["icon"]

def get_avatar_color(avatar_id: int) -> str:
    """
    Obtiene el color del avatar.
    
    Args:
        avatar_id: ID del avatar (1-10)
        
    Returns:
        Color hex del avatar
    """
    avatar = AVATARS.get(avatar_id, AVATARS[1])
    return avatar["color"]

def get_avatar_name(avatar_id: int) -> str:
    """
    Obtiene el nombre descriptivo del avatar.
    
    Args:
        avatar_id: ID del avatar (1-10)
        
    Returns:
        Nombre descriptivo del avatar
    """
    avatar = AVATARS.get(avatar_id, AVATARS[1])
    return avatar["name"]

def create_avatar_widget(avatar_id: int, size: int = 40) -> ft.Container:
    """
    Crea un widget de avatar con el ícono y color correspondiente.
    
    Args:
        avatar_id: ID del avatar (1-10)
        size: Tamaño del avatar en píxeles
        
    Returns:
        Container con el avatar renderizado
    """
    icon = get_avatar_icon(avatar_id)
    color = get_avatar_color(avatar_id)
    
    return ft.Container(
        content=ft.Icon(
            icon,
            size=size,
            color=color,
        ),
        width=size + 10,
        height=size + 10,
        border_radius=(size + 10) // 2,
        bgcolor="#2a2a2a",
        alignment=ft.alignment.center,
    )

def get_all_avatars() -> dict:
    """
    Retorna todos los avatares disponibles.
    
    Returns:
        Diccionario con todos los avatares
    """
    return AVATARS
