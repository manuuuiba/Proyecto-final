# Chatbot IA con Flet y Groq

Aplicación de escritorio con interfaz gráfica construida en Flet que permite a múltiples usuarios iniciar sesión y mantener conversaciones independientes con un chatbot alimentado por Groq AI. Cada usuario tiene su propia memoria de conversación persistente almacenada en SQLite.

## 🚀 Características

- ✅ **Autenticación de usuarios**: Sistema completo de registro y login
- ✅ **Múltiples usuarios**: Cada usuario tiene su propia cuenta y sesión
- ✅ **Memoria persistente**: Las conversaciones se guardan en base de datos SQLite
- ✅ **IA con Groq**: Integración con modelos de Groq (LLaMA 3.1)
- ✅ **Interfaz moderna**: UI construida con Flet, tema oscuro
- ✅ **Seguridad**: Contraseñas hasheadas con bcrypt

## 📋 Requisitos

- Python 3.8 o superior
- Cuenta en [Groq](https://console.groq.com/) para obtener API key

## 🔧 Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar API key de Groq**:
   - Abre el archivo `.env`
   - Reemplaza `your_groq_api_key_here` con tu API key de Groq
   - Puedes obtener tu API key en: https://console.groq.com/keys

```env
GROQ_API_KEY=tu_api_key_real_aqui
```

4. **Inicializar la base de datos**:
```bash
python init_db.py
```

Este script creará la base de datos SQLite y opcionalmente usuarios de prueba.

## 🎯 Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Primera vez

1. **Crear una cuenta**:
   - En la pantalla de login, haz clic en "Crear cuenta nueva"
   - Ingresa un nombre de usuario (mínimo 3 caracteres)
   - Ingresa una contraseña (mínimo 6 caracteres)
   - Confirma la contraseña
   - Haz clic en "Registrar"

2. **Iniciar sesión**:
   - Ingresa tu usuario y contraseña
   - Haz clic en "Iniciar Sesión"

3. **Chat con el bot**:
   - Escribe tu mensaje en el campo de texto
   - Presiona Enter o haz clic en el ícono de enviar
   - El chatbot responderá usando Groq AI
   - Todas las conversaciones se guardan automáticamente

### Funciones adicionales

- **Limpiar historial**: Haz clic en el ícono de escoba para borrar todo tu historial de chat
- **Cerrar sesión**: Haz clic en el ícono de logout
- **Memoria persistente**: Cierra y vuelve a abrir la app, tu historial seguirá ahí

## 📁 Estructura del Proyecto

```
Proyecto Final/
├── main.py              # Aplicación principal de Flet
├── database.py          # Gestión de base de datos SQLite
├── groq_client.py       # Cliente para API de Groq
├── auth.py              # Autenticación y hash de contraseñas
├── init_db.py           # Script de inicialización de BD
├── requirements.txt     # Dependencias del proyecto
├── .env                 # Configuración de API key
├── .env.example         # Plantilla para .env
├── .gitignore          # Archivos a ignorar en git
└── chatbot.db          # Base de datos (se crea automáticamente)
```

## 🔐 Seguridad

- Las contraseñas se almacenan hasheadas usando bcrypt
- La API key se carga desde un archivo `.env` que no se sube a git
- Cada usuario solo puede ver sus propias conversaciones

## 🛠️ Tecnologías

- **Flet**: Framework para interfaces gráficas en Python
- **Groq**: API de modelos de lenguaje de IA
- **SQLite**: Base de datos embebida
- **bcrypt**: Hash seguro de contraseñas
- **python-dotenv**: Gestión de variables de entorno

## 📝 Modelos disponibles en Groq

El proyecto usa por defecto `llama-3.1-70b-versatile`, pero puedes cambiar el modelo en `groq_client.py`:

- `llama-3.1-70b-versatile`
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

## 🐛 Solución de problemas

### Error: "API key de Groq no configurada"
- Asegúrate de haber editado el archivo `.env` con tu API key real
- Verifica que el archivo `.env` esté en el mismo directorio que `main.py`

### Error al crear la base de datos
- Asegúrate de tener permisos de escritura en el directorio
- Ejecuta `python init_db.py` antes de ejecutar la aplicación

### La aplicación no se conecta a Groq
- Verifica tu conexión a Internet
- Verifica que tu API key sea válida
- Revisa los límites de uso de tu cuenta de Groq

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 👨‍💻 Autor

Proyecto creado como parte del curso de Inteligencia Artificial II.
