# Memoria Técnica: Desarrollo de Chatbot IA Institucional
## Universidad de León (UDL)

**Autor:** Manu Ibarra  
**Fecha:** Diciembre 2024  
**Asignatura:** Inteligencia Artificial II  

---

## 1. Introducción y Objetivos

### 1.1 Definición del Proyecto
El objetivo principal de este proyecto ha sido desarrollar una aplicación de escritorio multiplataforma que actúe como un **Asistente Virtual Inteligente (Chatbot)**, integrando la identidad corporativa de la Universidad de León. La aplicación permite a los usuarios interactuar con un modelo de lenguaje avanzado (LLM) en un entorno seguro, persistente y visualmente alineado con la institución.

### 1.2 Objetivos Específicos
- **Integración de IA**: Implementar modelos de lenguaje actuales (Llama 3 vía Groq) para respuestas rápidas y coherentes.
- **Identidad Institucional**: Aplicar rigurosamente la paleta de colores y logotipos de la UDL.
- **Seguridad**: Sistema robusto de registro y autenticación de usuarios.
- **Persistencia**: Almacenamiento local de historiales de conversación y preferencias.
- **Experiencia de Usuario (UX)**: Interfaz moderna, adaptativa (Modo Claro/Oscuro) y responsiva.

---

## 2. Stack Tecnológico

Para el desarrollo se han seleccionado tecnologías modernas y eficientes:

| Componente | Tecnología | Justificación |
|------------|------------|---------------|
| **Lenguaje** | **Python 3.13** | Estándar en IA, gran ecosistema de librerías. |
| **Interfaz (UI)** | **Flet** | Framework basado en Flutter que permite crear UIs nativas con Python. |
| **IA Engine** | **Groq API** | Proveedor de inferencia de ultra-baja latencia para Llama 3. |
| **Base de Datos** | **SQLite** | Base de datos relacional ligera, serverless y local. |
| **Seguridad** | **bcrypt** | Estándar industrial para el hashing seguro de contraseñas. |

---

## 3. Arquitectura del Sistema

El proyecto sigue una estructura modular para facilitar el mantenimiento y la escalabilidad:

### 3.1 Estructura de Archivos
- `main.py`: Punto de entrada y gestión de la interfaz gráfica (UI). Mantiene el estado de la aplicación.
- `database.py`: Capa de persistencia. Maneja todas las conexiones y consultas SQL.
- `auth.py`: Lógica de seguridad (hash y verificación de passwords).
- `groq_client.py`: Cliente encapsulado para la comunicación con la API de Groq.
- `avatars.py`: Configuración del sistema de personalización visual.
- `chatbot.db`: Archivo de base de datos SQLite.

### 3.2 Diagrama de Flujo de Datos
1. **Usuario** ingresa credenciales en UI.
2. **Auth** verifica contra `chatbot.db`.
3. Al iniciar sesión, se carga el perfil y tema desde `user_profiles`.
4. **Usuario** envía mensaje.
5. **UI** envía prompt a `groq_client.py`.
6. **IA** responde y ambos mensajes se guardan en `database.py`.

---

## 4. Desarrollo e Implementación

### 4.1 Base de Datos Relacional
Se diseñó un esquema relacional para soportar las funcionalidades avanzadas:

- **Tabla `users`**: Credenciales y fecha de registro.
- **Tabla `messages`**: Historial de chat vinculado por `user_id`. Contenido, rol (user/assistant) y timestamp.
- **Tabla `user_profiles`**: Preferencias visuales (tema claro/oscuro) y avatar seleccionado.
- **Tabla `user_stats`**: Telemetría de uso (total de mensajes, logins, días activo).

*Código destacado (database.py):*
```python
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id INTEGER PRIMARY KEY,
    theme_preference TEXT DEFAULT 'dark',
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

### 4.2 Interfaz Gráfica (Flet)
La UI fue el foco principal de personalización para cumplir con el branding UDL.

#### Identidad Visual UDL
Se implementaron constantes de color para asegurar consistencia:
- **Verde Institucional**: `#006341` (Fondos principales, sidebar)
- **Verde Brillante**: `#00A859` (Botones de acción, burbujas de IA)
- **Verde Lima**: `#A4D65E` (Acentos, íconos, bordes activos)
- **Azul Corporativo**: `#003B5C` (Variantes de texto/fondo)

#### Sistema de Temas (Dark/Light Mode)
Se implementó un sistema dinámico que cambia no solo el color de fondo, sino la paleta de colores de texto y los assets de imagen (logotipo) en tiempo real.
- **Modo Oscuro**: Fondo `#1a1a1a`, Texto Blanco, Logo monocromo negativo.
- **Modo Claro**: Fondo Blanco, Texto `#006341`, Logo original.

### 4.3 Integración de Inteligencia Artificial
Se configuro `GroqClient` para mantener el contexto de la conversación.
- **System Prompt**: Se definió una personalidad base para el asistente ("Eres un asistente útil y amigable...").
- **Memoria**: Se envía el historial reciente al modelo para mantener la coherencia en la charla.

---

## 5. Retos Técnicos y Soluciones

Durante el desarrollo surgieron desafíos específicos relacionados con la librería gráfica y la compatibilidad:

### 5.1 Compatibilidad de Flet
**Problema**: La versión instalada de Flet no soportaba ciertas propiedades de animación (`animate_scale`) ni propiedades de imagen en Contenedores (`image_src`), causando errores en tiempo de ejecución (`AttributeError`).
**Solución**: 
- Se refactorizó el código para utilizar un diseño de `Stack` para el fondo con marca de agua en lugar de propiedades directas del contenedor.
- Se eliminaron las animaciones no soportadas, manteniendo la interactividad mediante estados de hover y cambios de color.

### 5.2 Visibilidad y Contraste
**Problema**: Al cambiar entre modos Claro y Oscuro, ciertos textos (como títulos o inputs) se volvían invisibles (blanco sobre blanco o verde sobre verde).
**Solución**: Se implementó lógica condicional en la propiedad `color` de los textos. Ejemplo: `color="white" if self.is_dark_mode else "#006341"`. En la Barra Superior, se forzó el color blanco ya que el fondo de la barra se mantiene verde institucional en ambos temas.

### 5.3 Bloqueo de Interacción (Click-Through)
**Problema**: El uso inicial de un `Stack` para poner el logo de fondo bloqueaba los clics en los botones de "Login" y "Registro".
**Solución**: Se reestructuró el layout para usar el logo como una imagen con baja opacidad dentro de un contenedor dedicado que no interfiere con el z-index de los controles interactivos, o se ajustó la estructura para que los controles estuvieran "encima" explícitamente.

---

## 6. Manual de Usuario Rápido

1. **Inicio**: Ejecutar `python main.py`.
2. **Registro**: Clic en tarjeta "Nuevo Usuario (+)". Ingresar usuario y contraseña.
3. **Login**: Seleccionar tarjeta de usuario. Ingresar contraseña.
4. **Chat**: Escribir en la barra inferior.
    - **Cambiar Tema**: Clic en el sol/luna superior derecha.
    - **Limpiar Chat**: Clic en icono de basura.
    - **Cerrar Sesión**: Clic en icono de salida.

---

## 7. Conclusión

El proyecto ha resultado en una aplicación robusta que cumple con los requerimientos funcionales de un sistema de chat con IA, a la vez que respeta estrictamente la identidad visual de la Universidad de León. La arquitectura modular permite futuras expansiones, como la implementación de un dashboard de estadísticas visual o nuevos modelos de IA, sin reescribir el núcleo del sistema.
