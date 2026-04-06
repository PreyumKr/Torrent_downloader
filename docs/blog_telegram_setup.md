# Automating Your Media: How to Create a Telegram Bot and Get Your API Token

In this guide, we'll walk through the process of setting up a Telegram bot from scratch. This is a critical step for the **Torrent Downloader** project, enabling remote control of your downloads directly from your phone.

---

## <a id="index"></a>Index
1. <a href="#step1">Step 1: Meet the BotFather</a>
2. <a href="#step2">Step 2: Creating a New Bot</a>
3. <a href="#step3">Step 3: Naming Your Bot</a>
4. <a href="#step4">Step 4: Securing Your API Token</a>
5. <a href="#step5">Step 5: Customizing the Bot (Optional)</a>
6. <a href="#step6">Step 6: Integrating with the Torrent Downloader</a>

---

## <a id="step1"></a>1. Step 1: Meet the BotFather
The "BotFather" is the one bot to rule them all. It is the official Telegram tool for creating and managing all other bots.

- Open your Telegram app.
- Search for `@BotFather` in the search bar.
- Ensure it has the **blue checkmark** next to its name to verify it's the official account.
- Click **Start** or type `/start`.

---

## <a id="step2"></a>2. Step 2: Creating a New Bot
Once you've initiated a conversation with BotFather, you need to issue the command to create a new entity.

- Type or select the command `/newbot`.
- BotFather will respond, asking you to choose a name for your bot.

---

## <a id="step3"></a>3. Step 3: Naming Your Bot
There are two distinct "names" you need to provide:

1.  **Display Name:** This is the name people see in their chat list (e.g., "My Media Manager"). It can be anything.
2.  **Username:** This is the unique identifier used to find your bot via search. It **must** end in the word `bot` (e.g., `my_cool_downloader_bot`). 
    - *Note: Usernames must be unique globally. If your choice is taken, BotFather will ask for another.*

---

## <a id="step4"></a>4. Step 4: Securing Your API Token
After successfully choosing a username, BotFather will provide you with a long alphanumeric string. This is your **HTTP API Token**.

- **Copy this token immediately.**
- **CRITICAL SECURITY WARNING:** Never share this token publicly. Anyone with this token can control your bot and access your messages. 
- In our project, this token stays strictly in your `.env` file and is never committed to Git.

---

## <a id="step5"></a>5. Step 5: Customizing the Bot (Optional)
To make your bot feel more professional, you can add a description and commands:

- `/setdescription`: Change the text users see when they first find your bot.
- `/setuserpic`: Upload a profile picture for your bot.
- `/setcommands`: Define the list of commands (like `/movie` or `/series`) so they appear in the auto-complete menu.

---

## <a id="step6"></a>6. Step 6: Integrating with the Torrent Downloader
Now that you have your token, you need to tell the application how to use it.

1.  Open your project directory.
2.  Locate your `.env` file (if it doesn't exist, copy `.env.example` to `.env`).
3.  Find the line `TELEGRAM_BOT_TOKEN=`.
4.  Paste your token there:
    ```bash
    TELEGRAM_BOT_TOKEN=123456789:ABCdefGHiJKLMNOPqrstuvwxyz
    ```
5.  Restart your bot process using `python run_telegrambot.py`.

Your bot is now live and ready to take commands!
