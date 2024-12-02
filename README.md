# 🎫 Coding Services SEND DM 🎫

# 🤖 SMART-ADMIN

This project is a Telegram bot designed to automate message management in groups or individual chats. It comes with special features that make it useful for administrators and moderators.
 
 <img src="./gui.png" alt="ig">
 
---

## 🖥️ **New GUI Features**
      - 🔧 Token Configuration:  
         Easily set up your bot's **`TOKEN`**, **`GROUP_CHAT_ID`**, and **`ADMIN_ID`** directly through the graphical interface.
        
      - ▶️ Start/Stop Control:  
         Intuitive buttons to **start** and **stop** the bot without manual interruptions.
        
      - 📡 Real-Time Logs:  
         Monitor bot activities such as sent messages, forwarded messages, and errors in a **dedicated console** within the GUI.
        
      - ⚙️ Customizable Settings:  
         Adjust parameters like **auto-deletion time** and manage configurations through the GUI.

## ⚙️ Workflow
```mermaid
graph TD;
    A[Start Bot] --> B[Load GUI];
    B --> C[Set TOKEN, GROUP_CHAT_ID, ADMIN_ID];
    C --> D[Click Start];
    D --> E{Is BOT Running?};
    E -- Yes --> F[Fetch Updates from Telegram API];
    F --> G[Process Incoming Messages];
    G -->|Admin Commands| H[Execute Admin Commands];
    G -->|User Messages| I[Log and Respond to Users];
    H --> F;
    I --> F;
    E -- No --> J[Stop Bot and Logs];
```
---

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
