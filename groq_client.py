"""
Cliente para interactuar con la API de Groq.
Maneja las conversaciones con el modelo de IA.
"""
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from groq import Groq


class GroqClient:
    """Cliente para gestionar conversaciones con Groq AI."""
    
    def __init__(self):
        """Inicializa el cliente de Groq con la API key del archivo .env."""
        load_dotenv()
        api_key = os.getenv('GROQ_API_KEY')
        
        if not api_key or api_key == 'your_groq_api_key_here':
            raise ValueError(
                "API key de Groq no configurada. "
                "Por favor configura GROQ_API_KEY en el archivo .env"
            )
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"  # Modelo por defecto
    
    def chat(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Envía mensajes al modelo y obtiene una respuesta.
        
        Args:
            messages: Lista de mensajes en formato [{"role": "user/assistant", "content": "..."}]
            system_prompt: Prompt del sistema opcional
            
        Returns:
            Respuesta del modelo como string
        """
        try:
            # Preparar mensajes
            chat_messages = []
            
            # Agregar system prompt si existe
            if system_prompt:
                chat_messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Agregar mensajes de conversación
            chat_messages.extend(messages)
            
            # Hacer la petición a Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            
            # Extraer y retornar la respuesta
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error al comunicarse con Groq: {str(e)}"
    
    def chat_with_context(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Envía un mensaje con contexto de conversación completo.
        
        Args:
            user_message: Mensaje del usuario
            conversation_history: Historial previo de la conversación
            system_prompt: Prompt del sistema opcional
            
        Returns:
            Respuesta del modelo
        """
        # Agregar el nuevo mensaje del usuario al historial
        messages = conversation_history.copy()
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Obtener respuesta
        return self.chat(messages, system_prompt)
    
    def set_model(self, model_name: str):
        """
        Cambia el modelo de IA a utilizar.
        
        Args:
            model_name: Nombre del modelo (ej: llama-3.1-70b-versatile, mixtral-8x7b-32768)
        """
        self.model = model_name


# System prompt por defecto para el chatbot
DEFAULT_SYSTEM_PROMPT = """Eres un asistente virtual amigable y útil. 
Respondes de manera clara, concisa y profesional. 
Ayudas a los usuarios con sus preguntas y tareas de la mejor manera posible.
Mantén un tono conversacional y empático."""
