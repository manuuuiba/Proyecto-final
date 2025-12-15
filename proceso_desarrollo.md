# Bitácora de Desarrollo: Chatbot IA UDL

Este documento detalla el proceso cronológico y técnico de la construcción de la aplicación de Chatbot Institucional paso a paso.

---

## 🛠️ Herramientas y Tecnologías Utilizadas

Para llevar a cabo este proyecto se seleccionó un stack tecnológico moderno y eficiente:

*   **Lenguaje de Programación**: Python 3 (Versión 3.13)
*   **Interfaz Gráfica (Frontend)**: Flet (Framework basado en Flutter para Python)
*   **Inteligencia Artificial**: API de Groq (Modelo `llama-3.1-8b-instant`)
*   **Base de Datos**: SQLite3 (Integrada en Python, sin servidor)
*   **Editor de Código (IDE)**: Visual Studio Code
*   **Librerías Clave**:
    *   `flet`: Para la construcción de la UI.
    *   `groq`: Cliente para conectar con el modelo de lenguaje.
    *   `bcrypt`: Para el encriptado (hashing) seguro de contraseñas.
    *   `python-dotenv`: Para manejo de variables de entorno (.env).
*   **Recursos Gráficos**: Escudos y paleta de colores oficial de la Universidad de León (UDL).

---

## 📅 Fase 1: Cimientos del Proyecto

### 1.1 Configuración del Entorno
El desarrollo comenzó estableciendo un entorno de trabajo limpio en Python.
- Se creó un entorno virtual para aislar dependencias.
- Se definieron las librerías clave en `requirements.txt`: `flet` (UI), `groq` (IA), `python-dotenv` (Variables de entorno), `bcrypt` (Seguridad).
- Se configuró el archivo `.env` para almacenar de forma segura la `GROQ_API_KEY`, evitando hardcodear credenciales en el código fuente.

### 1.2 Estructura de Base de Datos (SQLite)
Se diseñó el modelo de datos relacional en `database.py`.
- **Decisión de Diseño**: Se optó por SQLite por ser serverless (archivo local `chatbot.db`), ideal para una aplicación de escritorio que no requiere instalación de servidores complejos.
- **Implementación**:
  - Se crearon las tablas `users` y `messages` con claves foráneas para vincular cada mensaje a un usuario específico.
  - Se implementó la opción `ON DELETE CASCADE` para asegurar que si un usuario se borra, sus mensajes también desaparezcan, manteniendo la integridad de la BD.

---

## 🔐 Fase 2: Lógica de Negocio y Seguridad

### 2.1 Módulo de Autenticación (`auth.py`)
Antes de crear cualquier interfaz, se aseguró la lógica de seguridad.
- Se implementaron funciones para hashear contraseñas (`hash_password`) usando `bcrypt`.
- Se creó la función de verificación (`verify_password`) para el login.

### 2.2 Cliente de Inteligencia Artificial (`groq_client.py`)
Se encapsuló la lógica de la API de Groq en una clase dedicada.
- Se configuró el modelo `llama-3.1-8b-instant` por su equilibrio entre velocidad y calidad.
- Se diseñó el método `get_chat_response` para aceptar el historial de mensajes, permitiendo que el chatbot tenga "memoria" del contexto de la conversación actual.

---

## 🖥️ Fase 3: Desarrollo de la Interfaz (UI) con Flet

Esta fue la fase más extensa e iterativa del desarrollo.

### 3.1 Prototipo Funcional (MVP)
Se creó la primera versión de `main.py` con una estructura básica:
- Una pantalla de Login sencilla.
- Una pantalla de Chat con una lista de mensajes y un campo de texto.
- **Objetivo**: Verificar que el usuario pudiera registrarse, loguearse y hablar con la IA, sin importar el diseño visual.

### 3.2 Implementación de Identidad UDL
Una vez funcional, se procedió a aplicar la identidad corporativa de la Universidad de León.
- Se sustituyeron los colores por defecto de Flet Material Design por los códigos hexadecimales oficiales:
  - `#006341` (Verde UDL) para barras y fondos de tarjetas.
  - `#A4D65E` (Verde Lima) para acentos e iconos.
- Se rediseñaron las tarjetas de usuario para ser botones grandes y accesibles en la pantalla de inicio.

### 3.3 Sistema de Temas Dinámicos
Se añadió la complejidad de soportar **Modo Claro y Oscuro**.
- Esto requirió refactorizar el código de la UI para no usar colores fijos (strings), sino variables o lógica condicional.
- **Lógica**: `color="white" if self.is_dark_mode else "#006341"`.
- Se integró el botón de "toggle" (Sol/Luna) que redibuja la interfaz al instante.

### 3.4 Marca de Agua y Recursos Gráficos
Se integró el escudo de la UDL.
- Se añadieron los archivos PNG del logo al proyecto.
- **Reto de Implementación**: Al intentar poner el logo de fondo, inicialmente bloqueaba los clics de los botones.
- **Solución**: Se utilizó un contenedor con la propiedad `image_src` y baja opacidad al fondo de la estructura principal, asegurando que fuera puramente decorativo y no interfiriera con la funcionalidad.

---

## 🛠️ Fase 4: Refinamiento y Corrección de Errores

### 4.1 Problema de Compatibilidad
Al probar la aplicación, surgió un error `AttributeError: module 'flet' has no attribute 'animation'`.
- **Diagnóstico**: La versión de Flet instalada era diferente a la documentación consultada.
- **Acción**: Se eliminaron las propiedades de animación incompatibles, optando por una interfaz más estática pero estable y funcional.

### 4.2 Legibilidad y Contraste
En el Modo Claro, se detectó que el título "Chat" desaparecía (texto blanco sobre fondo claro).
- **Acción**: Se forzó el color del título de la barra superior a Blanco siempre, ya que la barra superior mantiene el color Verde Institucional en ambos temas, garantizando la legibilidad.

---

## ✅ Fase 5: Entrega Final

El resultado es una aplicación monolítica (todo empaquetado junto) pero modular internamente:
1.  **Backend**: SQLite + Auth.
2.  **Frontend**: Flet con estilos UDL.
3.  **Servicios**: Groq AI.

La aplicación cumple con todos los requisitos de funcionalidad avanzadas (persistencia, IA contextual) bajo una capa visual estrictamente corporativa y profesional.
