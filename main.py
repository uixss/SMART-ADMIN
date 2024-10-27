import requests
import json
import time
import threading
from datetime import datetime

TOKEN = "7255534026:AAHKeYg1eLBgSXrXipLTudvpC8F6OudKeSA"

GROUP_CHAT_ID = "-1002065237818" 
ADMIN_ID = "7139918953"  

AUTO_DELETE_DELAY = 5  



BOT_URL = f"https://api.telegram.org/bot{TOKEN}/"
START_LOG_FILE = "start_log.json"  
MESSAGE_LOG_FILE = "message_log.json"
responding_to_user = False

def send_message(chat_id, text, should_auto_delete=True):
    url = BOT_URL + "sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=payload).json()
    if 'ok' in response and response['ok']:
        message_id = response['result']['message_id']
        log_message(chat_id, message_id, text)
        if should_auto_delete and str(chat_id) != ADMIN_ID:
            threading.Thread(target=auto_delete_message, args=(chat_id, message_id)).start()
    else:
        print(f"Error al enviar mensaje: {response}")
def forward_message(user_id, from_chat_id, message_id):
    url = f"https://api.telegram.org/bot{TOKEN}/forwardMessage"
    payload = {
        'chat_id': user_id,
        'from_chat_id': from_chat_id,
        'message_id': message_id
    }
    response = requests.post(url, data=payload).json()
    
    if 'ok' in response and response['ok']:
        forwarded_message_id = response['result']['message_id']
        log_message(user_id, forwarded_message_id, f"Reenviado de {from_chat_id}, ID: {message_id}")
        threading.Thread(target=auto_delete_message, args=(user_id, forwarded_message_id)).start()
    else:
        print(f"Error al reenviar mensaje a {user_id}: {response.get('description', 'Desconocido')}")

def log_message(chat_id, message_id, text):
    try:
        with open(MESSAGE_LOG_FILE, 'r') as file:
            message_log = json.load(file)
    except FileNotFoundError:
        message_log = []

    message_entry = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    message_log.append(message_entry)
    with open(MESSAGE_LOG_FILE, 'w') as file:
        json.dump(message_log, file, indent=4)

def auto_delete_message(chat_id, message_id):
    time.sleep(AUTO_DELETE_DELAY)  
    url = BOT_URL + "deleteMessage"
    payload = {'chat_id': chat_id, 'message_id': message_id}
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print(f"Mensaje con ID {message_id} eliminado correctamente.")
    else:
        print(f"Error al eliminar mensaje {message_id}: {response.text}")

def process_update(update):
    global responding_to_user  

    if 'message' in update:
        message = update['message']
        user_id = message['from']['id']
        text = message.get('text', 'Archivo o contenido multimedia')

        if str(user_id) == ADMIN_ID:
            if text.startswith('/chat'):
                responding_to_user = True  #
                process_chat_command(user_id, text)
            elif text.startswith('/resend'):
                process_resend_command(user_id, text)
            elif text.startswith('/list'):
                send_user_list(user_id)
            return  

        if not responding_to_user:
            username = message['from'].get('username', 'N/A')

            if text == "/start":
                log_start_command(user_id, username)
            
            formatted_message = f"Usuario: @{username}\nID: {user_id}\nMensaje: {text}"
            
            send_message(GROUP_CHAT_ID, formatted_message, should_auto_delete=False)
        else:
            send_message(user_id, text, should_auto_delete=True)


def process_chat_command(admin_id, text):
    global responding_to_user
    parts = text.split(' ', 2)
    if len(parts) < 3:
        send_message(admin_id, "/chat <user_id> <mensaje>")
        responding_to_user = False 
        return

    user_id_to_reply = parts[1]
    reply_message = parts[2]
    send_message(user_id_to_reply, reply_message)
    responding_to_user = False

def process_resend_command(admin_id, text):
    parts = text.split(' ', 3)
    if len(parts) < 4:
        send_message(admin_id, "/resend <user_id> <from_chat_id> <message_id>")
        return

    user_id_to_resend = parts[1]
    from_chat_id = parts[2]
    message_id = parts[3]
    forward_message(user_id_to_resend, from_chat_id, message_id)

def send_user_list(admin_id):
    try:
        with open(START_LOG_FILE, 'r') as file:
            start_log = json.load(file)

        if not start_log:
            return
        user_list = "\n".join([f"@{entry.get('username', 'Desconocido')} (ID: {entry['user_id']})" for entry in start_log])
        send_message(admin_id, f"\n{user_list}")
    
    except FileNotFoundError:
        send_message(admin_id, "No se ha encontrado registro.")

def log_start_command(user_id, username):

    try:
        with open(START_LOG_FILE, 'r') as file:
            start_log = json.load(file)
    except FileNotFoundError:
        start_log = []
    start_entry = {
        'user_id': user_id,
        'username': username,
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    start_log.append(start_entry)

    with open(START_LOG_FILE, 'w') as file:
        json.dump(start_log, file, indent=4)

def get_updates(offset=None):
    url = BOT_URL + "getUpdates"
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if 'result' in updates:
            for update in updates['result']:
                process_update(update)
                offset = update['update_id'] + 1

if __name__ == '__main__':
    main()
