"""
Aplicación de Chatbot con Flet.
Interfaz gráfica con autenticación y conversaciones persistentes por usuario.
"""
import flet as ft
from database import Database
from groq_client import GroqClient, DEFAULT_SYSTEM_PROMPT
from typing import Optional


class ChatbotApp:
    """Clase principal de la aplicación de chatbot."""
    
    def __init__(self, page: ft.Page):
        """
        Inicializa la aplicación.
        
        Args:
            page: Página principal de Flet
        """
        self.page = page
        self.db = Database()
        self.groq_client = None
        self.groq_error = None
        self.current_user_id: Optional[int] = None
        self.current_username: Optional[str] = None
        self.is_dark_mode = True  # Estado del tema
        
        # Configurar página
        self.page.title = "Chatbot IA"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#1a1a1a"  # Gris oscuro para modo oscuro
        self.page.padding = 0
        self.page.window_width = 900
        self.page.window_height = 700
        self.page.window_resizable = True
        
        # Intentar inicializar Groq client
        try:
            self.groq_client = GroqClient()
        except ValueError as e:
            # Guardar el error para mostrarlo después
            self.groq_error = str(e)
        
        # Mostrar pantalla de login
        self.show_login_screen()
    
    def show_error_dialog(self, message: str):
        """Muestra un diálogo de error."""
        dlg = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.page.close(dlg))
            ]
        )
        self.page.open(dlg)
    
    def show_info_dialog(self, title: str, message: str):
        """Muestra un diálogo de información."""
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.page.close(dlg))
            ]
        )
        self.page.open(dlg)
    
    def toggle_theme(self, e=None):
        """Cambia entre modo claro y oscuro."""
        self.is_dark_mode = not self.is_dark_mode
        
        if self.is_dark_mode:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.page.bgcolor = "#1a1a1a"
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.page.bgcolor = "white"
        
        # Recargar la pantalla actual
        if self.current_user_id is None:
            self.show_login_screen()
        else:
            self.show_chat_screen()
    
    def show_login_screen(self):
        """Muestra la pantalla de selección de usuarios."""
        # Obtener todos los usuarios
        users = self.db.get_all_users()
        
        # Si no hay usuarios, mostrar pantalla de registro directamente
        if not users:
            self.show_register_screen(first_user=True)
            return
        
        # Mensaje de advertencia sobre Groq API
        groq_warning = ft.Container(visible=False)
        if self.groq_error:
            groq_warning = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.WARNING_ROUNDED, color="#FBBF24", size=16),
                        ft.Text(
                            "API Key de Groq no configurada",
                            size=11,
                            color="#FBBF24",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=8,
                border_radius=8,
                bgcolor="#006341",
                border=ft.border.all(1, "#FBBF24"),
                visible=True,
            )
        
        def on_user_click(username: str):
            """Maneja el clic en una tarjeta de usuario."""
            self.show_password_screen(username)
        
        # Crear tarjetas de usuario
        user_cards = []
        for user in users:
            username = user['username']
            
            # Usar diferentes colores para cada usuario (tonos verdes institucionales)
            colors = ["#A4D65E", "#00A859", "#A4D65E", "#00A859", "#A4D65E"]
            color = colors[user['id'] % len(colors)]
            
            user_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=50, color=color),
                        ft.Text(
                            username,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=20,
                border_radius=12,
                bgcolor="#006341",
                border=ft.border.all(2, "#00A859"),
                width=140,
                height=140,
                on_click=lambda e, u=username: on_user_click(u),
                ink=True,
            )
            user_cards.append(user_card)
        
        # Botón para agregar nuevo usuario
        add_user_card = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, size=50, color="#A4D65E"),
                    ft.Text(
                        "Nuevo",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="#A4D65E",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=20,
            border_radius=12,
            bgcolor="#006341",
            border=ft.border.all(2, "#00A859"),
            width=140,
            height=140,
            on_click=lambda e: self.show_register_screen(),
            ink=True,
        )
        user_cards.append(add_user_card)
        
        # Grid de usuarios (máximo 4 por fila)
        user_grid = ft.Row(
            controls=user_cards,
            wrap=True,
            spacing=15,
            run_spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        # Botón de cambio de tema
        theme_button = ft.IconButton(
            icon=ft.Icons.LIGHT_MODE if self.is_dark_mode else ft.Icons.DARK_MODE,
            icon_color="#A4D65E",
            tooltip="Cambiar tema",
            on_click=self.toggle_theme,
        )
        
        # Logo como marca de agua
        logo_path = "logo_udl_dark.png" if self.is_dark_mode else "logo_udl.png"
        
        # Layout principal
        login_container = ft.Container(
            content=ft.Column(
                [
                    # Botón de tema alineado a la derecha
                    ft.Row(
                        [
                            ft.Container(expand=True),
                            theme_button,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Container(height=20),
                    ft.Icon(ft.Icons.SMART_TOY_ROUNDED, size=80, color="#A4D65E"),
                    ft.Text(
                        "Chatbot IA",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color="white" if self.is_dark_mode else "#006341",
                    ),
                    ft.Text(
                        "Universidad de León",
                        size=14,
                        color="#A4D65E",
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Text(
                        "Selecciona tu usuario",
                        size=13,
                        color="#00A859",
                    ),
                    ft.Container(height=10),
                    groq_warning,
                    ft.Container(height=20),
                    ft.Container(
                        content=user_grid,
                        padding=10,
                    ),
                    ft.Container(height=30),
                    ft.Text(
                        "Powered by Manu",
                        size=12,
                        color="#006341" if not self.is_dark_mode else "#A4D65E",
                        weight=ft.FontWeight.W_500,
                        italic=True,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            alignment=ft.alignment.center,
            expand=True,
        )
        
        self.page.clean()
        self.page.add(login_container)
        self.page.update()
    
    def show_password_screen(self, username: str):
        """Muestra la pantalla para ingresar contraseña de un usuario específico."""
        # Campo de contraseña
        password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            autofocus=True,
            bgcolor="#006341",
            border_color="#00A859",
            focused_border_color="#A4D65E",
            border_radius=10,
            text_size=14,
            color="white",
            label_style=ft.TextStyle(color="white"),
        )
        
        # Mensaje de error
        error_text = ft.Text("", color="#F87171", size=12)
        
        def on_login_click(e):
            """Maneja el inicio de sesión."""
            password = password_field.value
            
            if not password:
                error_text.value = "Por favor ingresa tu contraseña"
                self.page.update()
                return
            
            # Validar usuario
            valid, user_id = self.db.validate_user(username, password)
            
            if valid:
                self.current_user_id = user_id
                self.current_username = username
                self.show_chat_screen()
            else:
                error_text.value = "Contraseña incorrecta"
                password_field.value = ""
                self.page.update()
        
        def on_back_click(e):
            """Vuelve a la selección de usuarios."""
            self.show_login_screen()
        
        # Botones
        login_button = ft.ElevatedButton(
            "Iniciar Sesión",
            on_click=on_login_click,
            width=300,
            height=45,
            bgcolor="#00A859",
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            )
        )
        
        back_button = ft.TextButton(
            "← Cambiar usuario",
            on_click=on_back_click,
            style=ft.ButtonStyle(color="#A4D65E"),
        )
        
        # Layout
        password_container = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=80, color="#A4D65E"),
                    ft.Text(
                        username,
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                    ),
                    ft.Text(
                        "Ingresa tu contraseña",
                        size=14,
                        color="#A4D65E",
                    ),
                    ft.Container(height=30),
                    password_field,
                    error_text,
                    ft.Container(height=10),
                    login_button,
                    back_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=40,
            alignment=ft.alignment.center,
            expand=True,
        )
        
        # Manejar Enter para enviar
        password_field.on_submit = on_login_click
        
        self.page.clean()
        self.page.add(password_container)
        self.page.update()
    
    def show_register_screen(self, first_user: bool = False):
        """Muestra la pantalla de registro."""
        # Campos de entrada
        username_field = ft.TextField(
            label="Nuevo Usuario",
            width=300,
            autofocus=True,
            bgcolor="#006341",
            border_color="#00A859",
            focused_border_color="#A4D65E",
            border_radius=10,
            text_size=14,
            color="white",
            label_style=ft.TextStyle(color="white"),
        )
        
        password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            bgcolor="#006341",
            border_color="#00A859",
            focused_border_color="#A4D65E",
            border_radius=10,
            text_size=14,
            color="white",
            label_style=ft.TextStyle(color="white"),
        )
        
        confirm_password_field = ft.TextField(
            label="Confirmar Contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            bgcolor="#006341",
            border_color="#00A859",
            focused_border_color="#A4D65E",
            border_radius=10,
            text_size=14,
            color="white",
            label_style=ft.TextStyle(color="white"),
        )
        
        # Mensajes
        message_text = ft.Text("", size=12)
        
        def on_register_click(e):
            """Maneja el clic en el botón de registro."""
            username = username_field.value
            password = password_field.value
            confirm_password = confirm_password_field.value
            
            # Validaciones
            if not username or not password or not confirm_password:
                message_text.value = "Por favor completa todos los campos"
                message_text.color = "#F87171"
                self.page.update()
                return
            
            if len(username) < 3:
                message_text.value = "El usuario debe tener al menos 3 caracteres"
                message_text.color = "#F87171"
                self.page.update()
                return
            
            if len(password) < 6:
                message_text.value = "La contraseña debe tener al menos 6 caracteres"
                message_text.color = "#F87171"
                self.page.update()
                return
            
            if password != confirm_password:
                message_text.value = "Las contraseñas no coinciden"
                message_text.color = "#F87171"
                self.page.update()
                return
            
            # Crear usuario
            success, msg = self.db.create_user(username, password)
            
            if success:
                message_text.value = "¡Usuario creado! Redirigiendo..."
                message_text.color = "#10B981"
                self.page.update()
                
                # Esperar un momento y volver al login
                import time
                time.sleep(1.5)
                self.show_login_screen()
            else:
                message_text.value = msg
                message_text.color = "#F87171"
                self.page.update()
        
        def on_back_click(e):
            """Vuelve a la pantalla de login."""
            self.show_login_screen()
        
        # Botones
        register_button = ft.ElevatedButton(
            "Registrar",
            on_click=on_register_click,
            width=300,
            height=45,
            bgcolor="#00A859",
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            )
        )
        
        # Solo mostrar botón de volver si no es el primer usuario
        back_button = None if first_user else ft.TextButton(
            "← Volver",
            on_click=on_back_click,
            style=ft.ButtonStyle(color="#A4D65E"),
        )
        
        # Construir lista de elementos
        elements = [
            ft.Icon(ft.Icons.SMART_TOY_ROUNDED, size=80, color="#A4D65E"),  # Robot icon
            ft.Text(
                "Primer Usuario" if first_user else "Crear Cuenta",
                size=32,
                weight=ft.FontWeight.BOLD,
                color="white",
            ),
        ]
        
        if first_user:
            elements.append(
                ft.Text(
                    "Crea tu primer usuario para comenzar",
                    size=14,
                    color="#A4D65E",
                )
            )
        
        elements.extend([
            ft.Container(height=30),
            username_field,
            password_field,
            confirm_password_field,
            message_text,
            ft.Container(height=10),
            register_button,
        ])
        
        if back_button:
            elements.append(back_button)
        
        # Layout de registro
        register_container = ft.Container(
            content=ft.Column(
                elements,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=40,
            alignment=ft.alignment.center,
            expand=True,
        )
        
        self.page.clean()
        self.page.add(register_container)
        self.page.update()
    
    def show_chat_screen(self):
        """Muestra la pantalla de chat."""
        # Lista de mensajes
        message_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=True,
        )
        
        # Cargar historial de mensajes
        self.load_chat_history(message_list)
        
        # Campo de entrada
        message_input = ft.TextField(
            hint_text="Escribe tu mensaje aquí...",
            expand=True,
            multiline=True,
            min_lines=1,
            max_lines=3,
            shift_enter=True,
            border_radius=25,
            bgcolor="#006341",
            border_color="#00A859",
            focused_border_color="#A4D65E",
            text_size=14,
            color="white",
            hint_style=ft.TextStyle(color="#A4D65E"),
        )
        
        # Indicador de carga
        loading_indicator = ft.ProgressRing(visible=False, width=20, height=20, color="#A4D65E")
        
        def send_message(e):
            """Envía un mensaje al chatbot."""
            user_message = message_input.value.strip()
            
            if not user_message:
                return
            
            if not self.groq_client:
                self.show_error_dialog("Cliente de Groq no inicializado. Verifica tu API key.")
                return
            
            # Limpiar campo de entrada
            message_input.value = ""
            message_input.disabled = True
            loading_indicator.visible = True
            self.page.update()
            
            # Mostrar mensaje del usuario
            self.add_message_to_ui(message_list, "user", user_message)
            
            # Guardar mensaje del usuario en BD
            self.db.save_message(self.current_user_id, "user", user_message)
            
            # Obtener historial de conversación
            history = self.db.get_user_messages(self.current_user_id)
            conversation_history = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in history[:-1]  # Excluir el último mensaje que acabamos de agregar
            ]
            
            # Obtener respuesta del chatbot
            try:
                assistant_response = self.groq_client.chat_with_context(
                    user_message,
                    conversation_history,
                    DEFAULT_SYSTEM_PROMPT
                )
                
                # Mostrar respuesta del asistente
                self.add_message_to_ui(message_list, "assistant", assistant_response)
                
                # Guardar respuesta en BD
                self.db.save_message(self.current_user_id, "assistant", assistant_response)
            
            except Exception as ex:
                error_msg = f"Error al obtener respuesta: {str(ex)}"
                self.add_message_to_ui(message_list, "assistant", error_msg)
            
            finally:
                # Rehabilitar entrada
                message_input.disabled = False
                loading_indicator.visible = False
                message_input.focus()
                self.page.update()
        
        # Botón enviar
        send_button = ft.IconButton(
            icon=ft.Icons.SEND_ROUNDED,
            on_click=send_message,
            tooltip="Enviar mensaje",
            icon_color="#A4D65E",
            bgcolor="#006341",
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
            )
        )
        
        # Manejar Enter para enviar
        def on_message_submit(e):
            send_message(e)
        
        message_input.on_submit = on_message_submit
        
        def on_logout_click(e):
            """Cierra sesión y vuelve al login."""
            self.current_user_id = None
            self.current_username = None
            self.show_login_screen()
        
        def on_clear_chat_click(e):
            """Limpia el historial de chat."""
            def confirm_clear(e):
                self.db.clear_user_messages(self.current_user_id)
                message_list.controls.clear()
                self.page.close(confirm_dialog)
                self.page.update()
            
            confirm_dialog = ft.AlertDialog(
                title=ft.Text("Confirmar", color="white"),
                content=ft.Text("¿Estás seguro de que deseas limpiar todo el historial de chat?", color="white"),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.page.close(confirm_dialog)),
                    ft.TextButton("Limpiar", on_click=confirm_clear, style=ft.ButtonStyle(color="#A4D65E")),
                ],
                bgcolor="#006341",
            )
            self.page.open(confirm_dialog)
        
        def on_delete_account_click(e):
            """Elimina la cuenta del usuario actual."""
            def confirm_delete(e):
                # Eliminar el usuario
                success, message = self.db.delete_user(self.current_user_id)
                
                self.page.close(confirm_dialog)
                
                if success:
                    # Mostrar mensaje de éxito y volver al login
                    self.show_info_dialog("Cuenta Eliminada", "Tu cuenta y todos tus datos han sido eliminados.")
                    self.current_user_id = None
                    self.current_username = None
                    self.show_login_screen()
                else:
                    self.show_error_dialog(f"Error al eliminar cuenta: {message}")
            
            confirm_dialog = ft.AlertDialog(
                title=ft.Text("⚠️ Eliminar Cuenta", color="#F87171"),
                content=ft.Text(
                    "¿Estás seguro de que deseas eliminar tu cuenta?\n\n"
                    "Esta acción es IRREVERSIBLE y eliminará:\n"
                    "• Tu usuario\n"
                    "• Todo tu historial de conversaciones\n\n"
                    "No podrás recuperar esta información.",
                    size=14,
                    color="white"
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.page.close(confirm_dialog)),
                    ft.TextButton(
                        "Eliminar Cuenta", 
                        on_click=confirm_delete,
                        style=ft.ButtonStyle(color="#F87171")
                    ),
                ],
                bgcolor="#2D6A4F",
            )
            self.page.open(confirm_dialog)
        
        # Barra superior con diseño elegante
        top_bar = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.SMART_TOY_ROUNDED, color="#A4D65E", size=28),
                            ft.Column(
                                [
                                    ft.Text(
                                        f"Chat - {self.current_username}",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color="white",
                                    ),
                                    ft.Text(
                                        "Universidad de León",
                                        size=11,
                                        color="#A4D65E",
                                    ),
                                ],
                                spacing=0,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.LIGHT_MODE if self.is_dark_mode else ft.Icons.DARK_MODE,
                                on_click=self.toggle_theme,
                                tooltip="Cambiar tema",
                                icon_color="#A4D65E",
                                icon_size=20,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_SWEEP_ROUNDED,
                                on_click=on_clear_chat_click,
                                tooltip="Limpiar historial",
                                icon_color="#A4D65E",
                                icon_size=20,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.PERSON_REMOVE_ROUNDED,
                                on_click=on_delete_account_click,
                                tooltip="Eliminar cuenta",
                                icon_color="#F87171",
                                icon_size=20,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.LOGOUT_ROUNDED,
                                on_click=on_logout_click,
                                tooltip="Cerrar sesión",
                                icon_color="#A4D65E",
                                icon_size=20,
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.only(left=20, right=15, top=15, bottom=15),
            bgcolor="#006341",
            border=ft.border.only(bottom=ft.BorderSide(2, "#00A859")),
        )
        
        # Barra inferior con input elegante
        bottom_bar = ft.Container(
            content=ft.Row(
                [
                    message_input,
                    loading_indicator,
                    send_button,
                ],
                spacing=10,
            ),
            padding=ft.padding.only(left=20, right=20, top=15, bottom=15),
            bgcolor="#006341",
            border=ft.border.only(top=ft.BorderSide(2, "#00A859")),
        )
        
        # Layout del chat
        chat_layout = ft.Column(
            [
                top_bar,
                ft.Container(
                    content=message_list,
                    expand=True,
                    bgcolor="white" if not self.is_dark_mode else "#1a1a1a",
                ),
                bottom_bar,
            ],
            spacing=0,
            expand=True,
        )
        
        self.page.clean()
        self.page.add(chat_layout)
        message_input.focus()
        self.page.update()
    
    def load_chat_history(self, message_list: ft.ListView):
        """
        Carga el historial de chat del usuario.
        
        Args:
            message_list: ListView donde mostrar los mensajes
        """
        messages = self.db.get_user_messages(self.current_user_id)
        
        for msg in messages:
            self.add_message_to_ui(
                message_list,
                msg["role"],
                msg["content"],
                update_page=False
            )
    
    def add_message_to_ui(
        self,
        message_list: ft.ListView,
        role: str,
        content: str,
        update_page: bool = True
    ):
        """
        Agrega un mensaje a la interfaz de usuario.
        
        Args:
            message_list: ListView donde agregar el mensaje
            role: Rol del mensaje ('user' o 'assistant')
            content: Contenido del mensaje
            update_page: Si se debe actualizar la página
        """
        is_user = role == "user"
        
        message_bubble = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Tú" if is_user else "Asistente IA",
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        color="#A4D65E",
                    ),
                    ft.Text(
                        content,
                        size=14,
                        selectable=True,
                        color="white",
                    ),
                ],
                spacing=5,
            ),
            padding=15,
            border_radius=15,
            bgcolor="#006341" if is_user else "#00A859",  # Verde oscuro para usuario, verde brillante para asistente
            border=ft.border.all(1, "#00A859" if is_user else "#A4D65E"),
            margin=ft.margin.only(
                left=100 if is_user else 0,
                right=0 if is_user else 100,
            ),
        )
        
        message_list.controls.append(message_bubble)
        
        if update_page:
            self.page.update()


def main(page: ft.Page):
    """Función principal que inicia la aplicación."""
    ChatbotApp(page)


if __name__ == "__main__":
    ft.app(target=main)
