import requests
import json
import time
import threading
import customtkinter as ctk
from tkinter import scrolledtext
from datetime import datetime

TOKEN = ""
GROUP_CHAT_ID = ""
ADMIN_ID = ""
AUTO_DELETE_DELAY = 5
BOT_URL = ""
is_running = False
offset = None
responding_to_user = False

START_LOG_FILE = "start_log.json"
MESSAGE_LOG_FILE = "message_log.json"


def send_message(chat_id, text, should_auto_delete=True):
    url = BOT_URL + "sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=payload).json()
    if 'ok' in response and response['ok']:
        log(f"Mensaje enviado a {chat_id}: {text}")
        if should_auto_delete and str(chat_id) != ADMIN_ID:
            threading.Thread(target=auto_delete_message, args=(chat_id, response['result']['message_id'])).start()
    else:
        log(f"Error al enviar mensaje: {response}")

def auto_delete_message(chat_id, message_id):
    time.sleep(AUTO_DELETE_DELAY)
    url = BOT_URL + "deleteMessage"
    payload = {'chat_id': chat_id, 'message_id': message_id}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        log(f"Mensaje {message_id} eliminado correctamente.")
    else:
        log(f"Error al eliminar mensaje {message_id}: {response.text}")

def forward_message(user_id, from_chat_id, message_id):
    url = f"{BOT_URL}forwardMessage"
    payload = {'chat_id': user_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
    response = requests.post(url, data=payload).json()
    if 'ok' in response and response['ok']:
        log(f"Mensaje reenviado a {user_id} desde {from_chat_id}, ID: {message_id}")
    else:
        log(f"Error al reenviar mensaje a {user_id}: {response.get('description', 'Desconocido')}")

def process_update(update):
    global responding_to_user
    if 'message' in update:
        message = update['message']
        user_id = message['from']['id']
        text = message.get('text', '')
        username = message['from'].get('username', 'N/A')

        if str(user_id) == ADMIN_ID:
            if text.startswith('/chat'):
                responding_to_user = True
                process_chat_command(user_id, text)
            elif text.startswith('/resend'):
                process_resend_command(user_id, text)
            elif text.startswith('/list'):
                send_user_list(user_id)
            return

        if not responding_to_user:
            if text == "/start":
                log_start_command(user_id, username)
                send_message(GROUP_CHAT_ID, f"Usuario: @{username}\nID: {user_id}\nMensaje: {text}")
            else:
                send_message(user_id, "Mensaje recibido.", should_auto_delete=True)

def process_chat_command(admin_id, text):
    global responding_to_user
    parts = text.split(' ', 2)
    if len(parts) < 3:
        send_message(admin_id, "Uso: /chat <user_id> <mensaje>")
        responding_to_user = False
        return
    user_id_to_reply, reply_message = parts[1], parts[2]
    send_message(user_id_to_reply, reply_message)
    responding_to_user = False

def process_resend_command(admin_id, text):
    parts = text.split(' ', 3)
    if len(parts) < 4:
        send_message(admin_id, "Uso: /resend <user_id> <from_chat_id> <message_id>")
        return
    user_id_to_resend, from_chat_id, message_id = parts[1], parts[2], parts[3]
    forward_message(user_id_to_resend, from_chat_id, message_id)

def send_user_list(admin_id):
    try:
        with open(START_LOG_FILE, 'r') as file:
            start_log = json.load(file)
        user_list = "\n".join([f"@{entry['username']} (ID: {entry['user_id']})" for entry in start_log])
        send_message(admin_id, user_list)
    except FileNotFoundError:
        send_message(admin_id, "No se encontraron usuarios registrados.")

def log_start_command(user_id, username):
    try:
        with open(START_LOG_FILE, 'r') as file:
            start_log = json.load(file)
    except FileNotFoundError:
        start_log = []
    start_log.append({'user_id': user_id, 'username': username, 'datetime': datetime.now().isoformat()})
    with open(START_LOG_FILE, 'w') as file:
        json.dump(start_log, file, indent=4)

def get_updates():
    global offset
    url = f"{BOT_URL}getUpdates"
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params).json()
    if 'result' in response:
        for update in response['result']:
            process_update(update)
            offset = update['update_id'] + 1

def bot_loop():
    while is_running:
        try:
            get_updates()
            time.sleep(1)
        except Exception as e:
            log(f"Error: {e}")

def iniciar_bot():
    global is_running, TOKEN, GROUP_CHAT_ID, ADMIN_ID, BOT_URL
    TOKEN, GROUP_CHAT_ID, ADMIN_ID = entry_token.get(), entry_group_id.get(), entry_admin_id.get()
    BOT_URL = f"https://api.telegram.org/bot{TOKEN}/"
    if not TOKEN or not GROUP_CHAT_ID or not ADMIN_ID:
        log("Por favor, completa todos los campos antes de iniciar.")
        return
    is_running = True
    threading.Thread(target=bot_loop).start()
    log("Bot iniciado.")

def detener_bot():
    global is_running
    is_running = False
    log("Bot detenido.")

def log(message):
    console.insert(ctk.END, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    console.see(ctk.END)

# Interfaz gráfica con customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("600x500")
root.title("Telegram Bot GUI")

frame_config = ctk.CTkFrame(root)
frame_config.pack(pady=10, padx=10, fill="x")

ctk.CTkLabel(frame_config, text="TOKEN:").grid(row=0, column=0, padx=5, pady=5)
entry_token = ctk.CTkEntry(frame_config, width=400)
entry_token.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_config, text="Group Chat ID:").grid(row=1, column=0, padx=5, pady=5)
entry_group_id = ctk.CTkEntry(frame_config, width=400)
entry_group_id.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_config, text="Admin ID:").grid(row=2, column=0, padx=5, pady=5)
entry_admin_id = ctk.CTkEntry(frame_config, width=400)
entry_admin_id.grid(row=2, column=1, padx=5, pady=5)

frame_buttons = ctk.CTkFrame(root)
frame_buttons.pack(pady=10)

btn_start = ctk.CTkButton(frame_buttons, text="Iniciar Bot", command=iniciar_bot, fg_color="green")
btn_start.pack(side="left", padx=5)

btn_stop = ctk.CTkButton(frame_buttons, text="Detener Bot", command=detener_bot, fg_color="red")
btn_stop.pack(side="left", padx=5)

frame_console = ctk.CTkFrame(root)
frame_console.pack(pady=10, fill="both", expand=True)

console = ctk.CTkTextbox(frame_console, wrap="word")
console.pack(fill="both", expand=True)

root.mainloop()
