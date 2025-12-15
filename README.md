Chatbot Multi-Usuario con Flet y Groq

Este proyecto es una aplicación de escritorio (GUI) desarrollada en Python utilizando el framework Flet. Implementa un chatbot de Inteligencia Artificial potenciado por la API de Groq (modelos LLaMA 3.1), diseñado para soportar múltiples usuarios.
La funcionalidad central es un sistema robusto de autenticación de usuarios que garantiza que cada usuario tenga una sesión y un historial de conversación completamente independientes, con memoria persistente gestionada por SQLite.
Características Principales
Soporte Multi-Usuario: Sistema completo de registro y login. Permite sesiones individuales y segregación de datos.
Memoria Persistente: Las conversaciones se almacenan en una base de datos SQLite, manteniendo el contexto del chat a través de múltiples sesiones.
Integración con IA de Alto Rendimiento: Utiliza la API de Groq para obtener respuestas rápidas y avanzadas de modelos como LLaMA 3.1.
Seguridad: Implementación de hashing de contraseñas mediante bcrypt para una autenticación segura.
Interfaz de Usuario: Interfaz gráfica de escritorio moderna y funcional construida con Flet.
Tecnologías Clave
Componente
Tecnología
Descripción
GUI
Flet
Framework Python para interfaces de usuario.
Backend AI
Groq API (LLaMA 3.1)
Proporciona el modelo de lenguaje para las respuestas del chatbot.
Persistencia
SQLite
Base de datos embebida para almacenar usuarios e historial.
Seguridad
bcrypt
Módulo para el hashing seguro de contraseñas.

Pasos para el Uso
Instalar dependencias: pip install -r requirements.txt.
Configurar la clave API de Groq en el archivo .env.
Inicializar la base de datos: python init_db.py.
Ejecutar la aplicación: python main.py.
El proyecto destaca la integración efectiva de herramientas de Python para crear una aplicación de escritorio segura, escalable para múltiples usuarios y potenciada por tecnología de IA de vanguardia.
