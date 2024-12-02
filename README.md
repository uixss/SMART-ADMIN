# 🎫 Coding Services SEND DM 🎫

---

🖥️ New GUI Features

    Token Configuration: Easily set up your bot's TOKEN, GROUP_CHAT_ID, and ADMIN_ID through the graphical interface.
    Start/Stop Control: Use intuitive buttons to start and stop the bot without needing to interrupt the script manually.
    Real-Time Logs: Monitor bot activities in a dedicated console window within the GUI.
    Customizable Settings: Adjust message auto-deletion time and other parameters from the GUI.

---

# 🤖 SMART-ADMIN

This project is a Telegram bot designed to automate message management in groups or individual chats. It comes with special features that make it useful for administrators and moderators.

## 🚀 Key Features

| Feature               | Description                                                                                                                                 |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| 📩 **Message Sending**  | The bot can send messages to users or groups and delete them automatically after a defined period.                                          |
| 🔄 **Message Forwarding** | Allows forwarding messages from one chat to another, while keeping a log of each operation.                                                |
| 🗑️ **Auto Deletion**     | Automatically deletes sent messages after a configurable time.                                                                             |
| 📜 **Message Logging**   | Keeps a detailed log of all sent and forwarded messages, stored in JSON files for future reference.                                        |
| 👮‍♂️ **Admin Commands**   | Administrators can send messages to specific users, forward messages, and see a list of users who have interacted with the bot.             |

## 🛠️ Bot Commands

- `/start`: Start interacting with the bot and register the user in the system.
- `/chat <user_id> <message>`: Send a direct message to a specific user.
- `/resend <user_id> <from_chat_id> <message_id>`: Forward a message from a source chat to a user.
- `/list`: Show a list of users who have sent the `/start` command.

## 📝 Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `json`
  - `threading`

## ⚙️ Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/youruser/telegram-message-bot.git
   ```

2. Install the dependencies:
   ```bash
   pip install requests
   ```

3. Configure your Telegram token and admin IDs in the bot's main file.

4. Run the bot!
   ```bash
   python bot.py
   ```

## 📂 Important Files

- `start_log.json`: Log of users who have executed the `/start` command.
- `message_log.json`: Log of messages sent and forwarded by the bot.

---

Enjoy automating your chats with this Telegram bot! 😎
