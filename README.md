# SMART-ADMIN


# 🤖 Telegram Bot con Auto-Respuesta y Gestión de Mensajes

Este proyecto es un bot de Telegram diseñado para automatizar la gestión de mensajes en grupos o chats individuales. Cuenta con características especiales que lo hacen útil para administradores y moderadores.

## 🚀 Características principales

| Característica        | Descripción                                                                                                                                 |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| 📩 **Envío de mensajes** | El bot puede enviar mensajes a usuarios o grupos y puede eliminarlos automáticamente tras un período de tiempo definido.                   |
| 🔄 **Reenvío de mensajes** | Permite reenviar mensajes desde un chat a otro, manteniendo un registro de cada operación.                                                 |
| 🗑️ **Eliminación automática** | Elimina los mensajes enviados automáticamente después de un tiempo configurable.                                                        |
| 📜 **Registro de mensajes** | Mantiene un registro detallado de todos los mensajes enviados y reenviados, almacenados en archivos JSON para referencia futura.         |
| 👮‍♂️ **Comandos del administrador** | Los administradores pueden enviar mensajes a usuarios específicos, reenviar mensajes y ver una lista de usuarios que han interactuado con el bot. |

## 🛠️ Comandos del bot

- `/start`: Comienza la interacción con el bot y registra al usuario en el sistema.
- `/chat <user_id> <mensaje>`: Envía un mensaje directo a un usuario específico.
- `/resend <user_id> <from_chat_id> <message_id>`: Reenvía un mensaje desde un chat de origen a un usuario.
- `/list`: Muestra una lista de usuarios que han enviado el comando `/start`.

## 📝 Requisitos

- Python 3.x
- Bibliotecas:
  - `requests`
  - `json`
  - `threading`

## ⚙️ Configuración

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/telegram-bot-mensajes.git
   ```

2. Instala las dependencias:
   ```bash
   pip install requests
   ```

3. Configura tu token de Telegram y los IDs de administrador en el archivo principal del bot.

4. ¡Ejecuta el bot!
   ```bash
   python bot.py
   ```

## 📂 Archivos importantes

- `start_log.json`: Registro de usuarios que han ejecutado el comando `/start`.
- `message_log.json`: Registro de mensajes enviados y reenviados por el bot.

---

¡Disfruta automatizando tus chats con este bot de Telegram! 😎
